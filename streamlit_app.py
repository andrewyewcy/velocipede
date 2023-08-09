#################
# IMPORT PACKAGES
#################
import joblib
import numpy as np
import pandas as pd
import datetime as dt
import streamlit as st
import plotly.graph_objects as go
import plotly.express as px

##########################
# CONFIGURE STREAMLIT PAGE
##########################
st.set_page_config(
    page_title            = "Velocipede, a bike-share dashboard",
    page_icon             = "bicycle",
    initial_sidebar_state = "collapsed",
    layout                = "wide",
    menu_items            = {
        "Get help"     : None,
        "Report a Bug" : None,
        "About"        : None
    }
)

#########################
# Filters for Dashboard #
#########################

df = pd.read_csv(
    'analysis_data/location.csv',
    dtype = {"start_stn_code": "object"}
)

with st.sidebar:
    selected_year = st.multiselect(
        "Select Year",
        options = ['Select All Years'] + df['yyyy'].unique().tolist(),
        default = [2014,2015,2016,2017]
    )

    selected_stations = st.radio(
        "Select Stations",
        options = ["All Stations", "Top 10 Stations"]
    )

if selected_stations == "All Stations":
    df = df
else:
    df['grouped_rides'] = df.groupby(
        by = ['yyyy', 'start_stn_code'])['rides'].transform('sum')

    df['rank'] = df.groupby(
        by = ['yyyy'])['grouped_rides'].rank("dense", ascending = False)

    df = df.loc[df['rank'] <= 10]

    
if "Select All Years" in selected_year:
    df = df
else:
    cond = df['yyyy'].isin(selected_year)
    df = df.loc[cond]

col1, col2 = st.columns(2, gap = "small")

###########################
#PLOT 1: Annual Ridership #
###########################

## Create plotting dataframe from base dataframe
# Group by year
plot_df = df.groupby(
    by = ['yyyy','is_member'],
    as_index = False
).agg(
    rides = ('rides','sum')
)

# Pivot by is member or not
plot_df = plot_df.pivot(columns = 'is_member',
                  index = 'yyyy',
                  values = 'rides')

# Create new columns to calculate total rides and % membership
plot_df['total'] = plot_df[0] + plot_df[1]
plot_df['membership_pct'] = plot_df[1] / plot_df['total']


## Create plotly figure
# Initiate figure object
fig = go.Figure()

# Specify common x axis values for traces
x = plot_df.index.values

# Trace 1: Total rides, create hover template and bar chart
hovertemplate = "<br>".join(
    [
        "Total trips: %{y:.2f} M",
        "<extra></extra>"
    ]
)

fig.add_trace(
        go.Bar(
            name = "Total trips",
            x = x,
            y = plot_df['total'] / 1_000_000, # Numbers in millions of rides
            hovertemplate = hovertemplate,
            marker_color = "cornflowerblue"
        )
)

# Trace 2: Member rides, create hover template and bar chart
# Create customdata to store % values for display
customdata = np.transpose([x,plot_df['membership_pct'].tolist()])
hovertemplate = "<br>".join(
    [
        "by Members: %{y:.2f} M",
        "% of total: %{customdata[1]:.2%}",
        "<extra></extra>"
    ]
)

fig.add_trace(
        go.Bar(
            name = "by Members",
            x = x,
            y = plot_df[1]/ 1_000_000,
            customdata = customdata,
            hovertemplate = hovertemplate,
            marker_color = "cornflowerblue",
            marker_pattern_shape = "/"
        )
)

# Trace 3: Non-member rides, create hover template and bar chart
customdata = np.transpose([x,[1 - val for val in plot_df['membership_pct'].tolist()]])
hovertemplate = "<br>".join(
    [
        "by Non-members: %{y:.2f} M",
        "% of total: %{customdata[1]:.2%}",
        "<extra></extra>"
    ]
)

fig.add_trace(
        go.Bar(
            name = "by Non-members",
            x = x,
            y = plot_df[0]/ 1_000_000,
            customdata = customdata,
            hovertemplate = hovertemplate,
            marker_color = "cornflowerblue",
            marker_pattern_shape = "+"
        )
)

## Format x, y axis titles, title
fig.update_layout(
    barmode = 'group',
    hovermode = "x unified",
    
    # Set uniform minimum textsize and force show
    # For max size, refer to textfont_size in update_traces
    uniformtext = dict(
        minsize = 9,
        mode = 'show'
    ),

    # Set title properties
     title = dict(
         text = f"Number of Bixi Trips by Year",
         x = 0.5,
         y = 0.85,
         xanchor = 'center',
         yanchor = 'top'
     ),

    # Set xaxis properties
    xaxis = dict(
        title = "Year",
        #titlefont_size = 14,
        tickfont_size = 12,
        #tickangle = -90,
        tickvals = x
    ),
    # Set yaxis properties
    yaxis = dict(
        title = f"Number of Bixi Trips (millions)",
        titlefont_size = 14,
        tickfont_size = 12
    )
    
)

#################
# END OF PLOT 1 #
#################

col1.plotly_chart(
    fig,
    use_container_width = True,
    sharing = "streamlit"
)

############################
# PLOT 2 Monthly Ridership #
############################

plot_df = df.groupby(
    by = ['yyyymm','yyyy','mmm'],
    as_index = False).agg(
    rides = ('rides','sum'))

## Initiate plotly graph object
fig = go.Figure()

x = plot_df['mmm'].unique()

# Add a line for each year 
for year in plot_df['yyyy'].unique():

    x = plot_df.loc[plot_df['yyyy'] == year, "mmm"].unique()
    y = plot_df.loc[plot_df['yyyy'] == year, "rides"]/1_000
    pct_yr_total = [val/y.sum() for val in y]
    customdata = np.transpose([x,pct_yr_total])
    
    hovertemplate = "<b>%{text} </b>" + "Trips: %{y:,.0f} K" + ",  % of year: %{customdata[1]:.2%}" + "<extra></extra>"
        

    fig.add_trace(
        go.Scatter(
            name = str(year), 
            x = x, 
            y = y,
            hovertemplate = hovertemplate,
            customdata = customdata,
            text = [year] * len(x)
        )
    )

fig.update_layout(
    barmode = 'group',
    hovermode = "x unified",
    
    # Set uniform minimum textsize and force show
    # For max size, refer to textfont_size in update_traces
    uniformtext = dict(
        minsize = 9,
        mode = 'show'
    ),

    # Set title properties
     title = dict(
         text = f"Number of Bixi Trips by Month",
         x = 0.5,
         y = 0.85,
         xanchor = 'center',
         yanchor = 'top'
     ),

    # Set xaxis properties
    xaxis = dict(
        title = "Month",
        #titlefont_size = 14,
        tickfont_size = 12,
        #tickangle = -90,
        tickvals = x,
        side = 'bottom'
    ),
    # Set yaxis properties
    yaxis = dict(
        title = f"Number of Bixi Trips (thousands)",
        titlefont_size = 14,
        tickfont_size = 12
    )
)

#################
# END OF PLOT 2 #
#################

col2.plotly_chart(
    fig,
    use_container_width = True,
    sharing = "streamlit"
)

########################
# PLOT 3 Trip Duration #
########################

# df = pd.read_csv('analysis_data/ride_length.csv')

plot_df = df.groupby(
    by = ['yyyy','trip_length'],
    as_index = False).agg(
        rides = ('rides','sum')
)

# Initiate plotly graph object
fig = go.Figure()

# Define trip duration groups for x axis
x = plot_df['trip_length'].unique()

# Add a bar for each year
for year in plot_df['yyyy'].unique():

    x = plot_df.loc[plot_df['yyyy'] == year, "trip_length"].unique()
    y = plot_df.loc[plot_df['yyyy'] == year, "rides"]/1_000_000
    pct_yr_total = [val/y.sum() for val in y]
    customdata = np.transpose([x,pct_yr_total])

    hovertemplate = "<b>%{text} </b>" + "Trips: %{y:,.2f} M" + ",  % of year: %{customdata[1]:.2%}" + "<extra></extra>"
    
    fig.add_trace(
            go.Bar(
                name = str(year),
                x = x,
                y = y, # Numbers in millions of rides,
                hovertemplate = hovertemplate,
                customdata = customdata,
                text = [year] * len(x)
            )
    )


fig.update_layout(
    barmode = 'group',
    hovermode = 'x unified',

    # Set uniform minimum textsize and force show
    # For max size, refer to textfont_size in update_traces
    uniformtext = dict(
        minsize = 9,
        mode = 'show'
    ),

    # Set title properties
     title = dict(
         text = f"Trip Duration",
         x = 0.5,
         y = 0.85,
         xanchor = 'center',
         yanchor = 'top'
     ),

    # Set xaxis properties
    xaxis = dict(
        title = "Trip duration (min)",
        #titlefont_size = 14,
        tickfont_size = 12,
        #tickangle = -90,
        tickvals = x,
        side = 'bottom'
    ),
    # Set yaxis properties
    yaxis = dict(
        title = f"Number of Bixi Trips (millions)",
        titlefont_size = 14,
        tickfont_size = 12
    )
)

#################
# END OF PLOT 3 #
#################

col1.plotly_chart(
    fig,
    use_container_width = True,
    sharing = "streamlit"
)

####################
# Plot 4: Location #
####################

groupby_clause = ['yyyy','start_stn_code','stn_lat','stn_lon']

plot_df = df.groupby(
    by = groupby_clause).agg(     
        rides = ('rides','sum'),
        # stn_lat = ('stn_lat','mean'),
        # stn_lon = ('stn_lon','mean'),
        stn_name = ('stn_name', lambda x: x.iloc[-1])
    )    

plot_df['avg_dur_sec'] = df.groupby(
    by = groupby_clause).apply(lambda x: np.average(x.avg_dur_sec, weights = x.rides))

plot_df.reset_index(inplace = True)

plot_df.rename(
    columns = 
    {
        "yyyy"        : "Year",
        "stn_lat"     : "Lat",
        "stn_lon"     : "Lon",
        "rides"       : "Trips",
        "stn_name"    : "Station Name",
        "avg_dur_sec" : "Avg. Trip Duration"
    },
    inplace = True
)

px.set_mapbox_access_token(open(".mapbox_token").read())

fig = px.scatter_mapbox(
    plot_df,
    lat = "Lat",
    lon = "Lon",
    text = "Station Name",
    hover_name = "Station Name",
    hover_data = {
        "Trips"              : ":,",
        "Lat"                : ":.3f",
        "Lon"                : ":.3f",
        "Avg. Trip Duration" : ":,.0f"
    },
    size = "Trips",
    size_max = 15,
    color = "Avg. Trip Duration",
    zoom = 12,
    mapbox_style = 'light',
    animation_frame = 'Year')
        
col2.plotly_chart(
    fig,
    use_container_width = True,
    sharing = "streamlit"
)