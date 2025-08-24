# This Python script is used to generate the Velocipede dashboard on http://3.96.175.190:8501/
# Author: Andrew Yew
# Date: 2023-08-21
# Contact: andrewyewcy@gmail.com

###################
# IMPORT PACKAGES #
###################
import numpy as np
import pandas as pd
import datetime as dt
import streamlit as st

import plotly.graph_objects as go
import plotly.express as px

############################
# CONFIGURE STREAMLIT PAGE #
############################
st.set_page_config(
    page_title            = "Velocipede, a bike-share dashboard",
    page_icon             = "bicycle",
    initial_sidebar_state = "expanded",
    layout                = "wide",
    menu_items            = {
        "Get help"     : None,
        "Report a Bug" : None,
        "About"        : None
    }
)

# Reduce white space at top of dashboard
st.markdown(
    """
        <style>
            .appview-container .main .block-container {{
                padding-top: {padding_top}rem;
                padding-bottom: {padding_bottom}rem;
                }}

        </style>""".format(
        padding_top=1, padding_bottom=1
    ),
    unsafe_allow_html=True,
)

###############
# IMPORT DATA #
###############

# Notes, data is a csv file generated from a MySQL query
df = pd.read_csv(
    '12_processed_data/location.csv',
    dtype = {"start_stn_code": "object"}
)

####################################
# FILTERS FOR DASHBOARD IN SIDEBAR #
####################################

# To create a reset filter button, define a function that sets the value in state back to defined values for each key
def clear_multi():
    st.session_state.year = [2014,2015,2016,2017] # key_name is "year"
    st.session_state.station = "All Stations"     # key_name is "station"
    return

# Define a sidebar to store all the filters
with st.sidebar:

    # Create a button to reset all filters.
    st.button(
        "Reset filters", 
        on_click = clear_multi # when button is click, reset session state to values defined in clear multi
    )

    # Create a multi-select tool for years
    selected_year = st.multiselect(
        "Select Year",
        options = ['All Years'] + df['yyyy'].unique().tolist(),
        default = [2014, 2015, 2016, 2017],
        key = "year"
    )

    # Create a radio for stations
    selected_stations = st.radio(
        "Select Stations",
        options = ["All Stations", "Top 10 Stations"],
        key = "station"
    )

    # Below section contains description of dashboard, contact info and links to creator profile
    st.write("**About this dashboard:**")
    st.write("This dashboard analyzes 35 million Bixi bicycle rental trips from 2014 to 2021 and is hosted on AWS as a Docker containerized application.")
    st.write("The data for the dashboard was obtained from [Bixi](https://bixi.com/en/open-data-2/).")
    st.write("For comments and documentation, the creator, **Andrew Yew**, can be contacted via the below channels:")
    st.write("[LinkedIn](https://www.linkedin.com/in/andrewyewcy)")
    st.write("[GitHub](https://github.com/andrewyewcy)")
    st.write("[Project Specific GitHub](https://github.com/andrewyewcy/velocipede)")
    st.write("[Website/Blog](https://andrewyewcy.com)")

####################
# APPLYING FILTERS #    
####################

# For stations
if selected_stations == "All Stations":
    df = df
else:
    # If not all stations selected, rank stations by sum of trips started for each year.
    df['grouped_rides'] = df.groupby(
        by = ['yyyy', 'start_stn_code'])['rides'].transform('sum')

    df['rank'] = df.groupby(
        by = ['yyyy'])['grouped_rides'].rank("dense", ascending = False)

    # Keep only the stations that are the top 10 stations for each year
    df = df.loc[df['rank'] <= 10]

# For year, if no stations were selected, generate a message that tells user to select at least 1 year
if len(selected_year) == 0:
    st.subheader(
        body = "Please select at least 1 year.",
        anchor = False)
else:
    # If all years selected, then do not filter, else filter by selected years.
    if "All Years" in selected_year:
        df = df.loc[:,:]
    else:
        cond = df['yyyy'].isin(selected_year)
        df = df.loc[cond]
    
    ####################
    # DASHBOARD HEADER #
    ####################

    # Define base body for title
    body = "Showing Bixi Bicycle Rental Trips for Years: "

    # Define how many years to display in dashboard header
    if "Select All Years" in selected_year:
        body += "2014 - 2021"
    else:
        for index, year in enumerate(selected_year):
            if index == len(selected_year) - 1:
                body += "and " + str(year)
            else:
                body += str(year) + ', '

    # Define which stations to show in dashboard header
    body += ' for ' + selected_stations

    # Generate dashboard header using defined body
    st.subheader(
        body = body,
        anchor = False
    )

    ###########################
    # DEFINE DASHBOARD LAYOUT # 
    ###########################

    # 2 columns side by side of equal width and small spacing between columns.
    col1, col2 = st.columns(
        2, 
        gap = "small"
    )
    
    ###########################
    #PLOT 1: Annual Ridership #
    ###########################    
    # Create dataframe for plotting from base dataframe
    # For membership, 1 =  member, 0 = non-member
    
    # Group by year and membership (Bixi membership program)
    plot_df = df.groupby(
        by = ['yyyy','is_member'],
        as_index = False
    ).agg(
        rides = ('rides','sum')
    )
    
    # Pivot by is membership
    plot_df = plot_df.pivot(
        columns = 'is_member',
        index   = 'yyyy',
        values  = 'rides')
    
    # Create new columns to calculate total rides and % membership
    plot_df['total'] = plot_df[0] + plot_df[1]
    plot_df['membership_pct'] = plot_df[1] / plot_df['total']
    
    # Create plotly figure object
    fig = go.Figure()
    
    # Define a common x axis all traces
    x = plot_df.index.values
    
    ## Trace 1: Bar chart for total rides
    # Create hovertemplate, meaning data that shows up when you hover over chart
    hovertemplate = "<br>".join(
        [
            "Total trips: %{y:.2f} M",
            "<extra></extra>"
        ]
    )

    # Create text that is visible on top of each bar
    texttemplate = "<br>".join(
        [
            "%{y:.2f}"
        ]
    )

    # Create Bar trace and add to plotly figure object
    fig.add_trace(
            go.Bar(
                name          = "Total trips",
                x             = x,
                y             = plot_df['total'] / 1_000_000, # Represent numbers in terms of millions of rides
                hovertemplate = hovertemplate,
                texttemplate  = texttemplate,
                marker_color  = "cornflowerblue"
            )
    )
    
    ## Trace 2: Repeat trace 1, but for member rides only
    # Create custom data containing membership percentage to appear upon hover
    customdata = np.transpose([x,plot_df['membership_pct'].tolist()])

    # Create hovertemplate, meaning data that shows up when you hover over chart
    hovertemplate = "<br>".join(
        [
            "by Members: %{y:.2f} M",
            "% of year: %{customdata[1]:.2%}",
            "<extra></extra>"
        ]
    )

    # Create text that is visible on top of each bar
    texttemplate = "<br>".join(
        [
            "%{y:.2f}"
        ]
    )

    # Create Bar trace and add to plotly figure object
    fig.add_trace(
            go.Bar(
                name                 = "by Members",
                x                    = x,
                y                    = plot_df[1]/ 1_000_000,
                customdata           = customdata,
                hovertemplate        = hovertemplate,
                texttemplate         = texttemplate,
                marker_color         = "cornflowerblue",
                marker_pattern_shape = "/"
            )
    )
    
    ## Trace 3: Repeat trace 2, but for non-member rides only
    # Create custom data containing non-membership percentage to appear upon hover
    customdata = np.transpose([x,[1 - val for val in plot_df['membership_pct'].tolist()]])
    
    # Create hovertemplate, meaning data that shows up when you hover over chart
    hovertemplate = "<br>".join(
        [
            "by Non-members: %{y:.2f} M",
            "% of year: %{customdata[1]:.2%}",
            "<extra></extra>"
        ]
    )

    # Create text that is visible on top of each bar
    texttemplate = "<br>".join(
        [
            "%{y:.2f}"
        ]
    )

    # Create Bar trace and add to plotly figure object
    fig.add_trace(
            go.Bar(
                name                 = "by Non-members",
                x                    = x,
                y                    = plot_df[0]/ 1_000_000,
                customdata           = customdata,
                hovertemplate        = hovertemplate,
                texttemplate         = texttemplate,
                marker_color         = "cornflowerblue",
                marker_pattern_shape = "+"
            )
    )
    
    ## Update the traces to display the number of rides on top of each bar
    fig.update_traces(
        textfont_size = 12,
        textposition  = 'outside',
        cliponaxis    = False # The cliponaxis attribute is set to False in the example below to ensure that the outside text on the tallest bar is allowed to render outside of the plotting area
    )

    ## Update layout of figure object, meaning, x-axis, y-axis, titles, hovermode, and legend
    fig.update_layout(
        barmode   = 'group',
        hovermode = "x unified",

        # Uniform minimum textsize
        uniformtext = dict(
            minsize = 9, 
            mode    = 'show' # force show text to prevent text from dissapearing when squeezed
        ),
    
        # Set title and title position
        title = dict(
             text    = f"Number of Bixi Trips by Year",
             x       = 0.5,
             y       = 0.95,
             xanchor = 'center',
             yanchor = 'top'
         ),
    
        # Set x-axis
        xaxis = dict(
            title    = "Year",
            tickvals = x
        ),
        
        # Set y-axis
        yaxis = dict(
            title          = f"Number of Bixi Trips (millions)",
            # font_size = 14,
            tickfont_size  = 12
        ),

        # Set legend
        legend = dict(
            orientation = "h",
            yanchor     = "bottom",
            y           = 1.01
        )
    )
    
    #################
    # END OF PLOT 1 #
    #################

    # Display Plot 1 in column 1
    col1.plotly_chart(
        fig,
        use_container_width = True,
        # sharing             = "streamlit" # deprecated
    )
    
    ############################
    # PLOT 2 Monthly Ridership #
    ############################

    # Create dataframe for plotting from base dataframe
    plot_df = df.groupby(
        by = ['yyyymm','yyyy','mmm'],
        as_index = False).agg(
        rides = ('rides','sum')
    )
    
    # Initiate plotly graph object
    fig = go.Figure()
    
    # Add a line trace for each year 
    for year in plot_df['yyyy'].unique():

        # Define x and y values
        x = plot_df.loc[plot_df['yyyy'] == year, "mmm"].unique()
        y = plot_df.loc[plot_df['yyyy'] == year, "rides"]/1_000
        
        # Store percentage of year in customer data for displaying on hover
        pct_yr_total = [val/y.sum() for val in y]
        customdata = np.transpose([x,pct_yr_total])

        # Create hovertemplate, meaning data that shows up when you hover over chart
        hovertemplate = "".join(
            [
                "<b>%{text} </b>",
                "Trips: %{y:,.0f} K",
                ",  % of year: %{customdata[1]:.2%}",
                "<extra></extra>"
            ]
        )

        # Add line trace to figure object
        fig.add_trace(
            go.Scatter(
                name          = str(year), 
                x             = x, 
                y             = y,
                mode          = "lines",
                hovertemplate = hovertemplate,
                customdata    = customdata,
                text          = [year] * len(x), # Add label for each line for appearing in hovertemplate
            )
        )

    ## Update layout of figure object, meaning, x-axis, y-axis, titles, hovermode, and legend
    fig.update_layout(
        barmode = 'group',
        hovermode = "x unified",
        
        # Set text size
        uniformtext = dict(
            minsize = 9,
            mode = 'show'
        ),
    
        # Set title 
         title = dict(
             text    = f"Number of Bixi Trips by Month",
             x       = 0.5,
             y       = 0.95,
             xanchor = 'center',
             yanchor = 'top'
         ),
    
        # Set x-axis
        xaxis = dict(
            title = "Month",
            tickvals = x,
            side = 'bottom'
        ),
        
        # Set y-axis
        yaxis = dict(
            title = f"Number of Bixi Trips (thousands)"
        ),

        # Set legend
        legend = dict(
            orientation = "h",
            yanchor     = "bottom",
            y           = 1.01
        )
    )
    #################
    # END OF PLOT 2 #
    #################

   # Display Plot 2 in column 2
    col2.plotly_chart(
        fig,
        use_container_width = True,
        # sharing             = "streamlit" # depecrated
    )
    
    ########################
    # PLOT 3 Trip Duration #
    ########################
    
    # Create plot dataframe from base dataframe
    plot_df = df.groupby(
        by = ['yyyy','trip_length'],
        as_index = False).agg(
            rides = ('rides','sum')
    )
    
    # Initiate plotly graph object
    fig = go.Figure()
    
    # Add a bar trace for each year
    for year in plot_df['yyyy'].unique():

        # Define x and y values
        x = plot_df.loc[plot_df['yyyy'] == year, "trip_length"].unique()
        y = plot_df.loc[plot_df['yyyy'] == year, "rides"]/1_000_000 # Numbers in millions of rides,
        
        # Store percentage of year in customer data for displaying on hover
        pct_yr_total = [val/y.sum() for val in y]
        customdata = np.transpose([x,pct_yr_total])

        # Create hovertemplate, meaning data that shows up when you hover over chart
        hovertemplate = "".join(
            [
                "<b>%{text} </b>",
                "Trips: %{y:,.2f} M",
                ",  % of year: %{customdata[1]:.2%}",
                "<extra></extra>"       
            ]
        )

        # Create text that is visible on top of each bar
        texttemplate = "<br>".join(
            [
                "%{y:.2f}"
            ]
        )
    
        # Add bar trace to figure object
        fig.add_trace(
                go.Bar(
                    name          = str(year),
                    x             = x,
                    y             = y, 
                    hovertemplate = hovertemplate,
                    customdata    = customdata,
                    texttemplate  = texttemplate,
                    text          = [year] * len(x)
                )
        )
    
    ## Update the traces to display the number of rides on top of each bar
    fig.update_traces(
        textposition = 'outside',
        cliponaxis = False # The cliponaxis attribute is set to False in the example below to ensure that the outside text on the tallest bar is allowed to render outside of the plotting area
    )

    ## Update layout of figure object, meaning, x-axis, y-axis, titles, hovermode, and legend 
    fig.update_layout(
        barmode   = 'group',
        hovermode = 'x unified',
    
        # Set uniform text
        uniformtext = dict(
            minsize = 9,
            mode    = 'show'
        ),
    
        # Set title 
         title = dict(
             text    = f"Number of Bixi Trips by Trip Duration",
             x       = 0.5,
             y       = 0.95,
             xanchor = 'center',
             yanchor = 'top'
         ),
    
        # Set x-axis
        xaxis = dict(
            title = "Trip Duration (min)",
            tickvals = x,
            side = 'bottom'
        ),
        
        # Set y-axis
        yaxis = dict(
            title = f"Number of Bixi Trips (millions)"
        ),

        # Set legend
        legend = dict(
            orientation = "h",
            yanchor     = "bottom",
            y           = 1.01
        )
    )
    #################
    # END OF PLOT 3 #
    #################

    # Display plot 3 in column 1
    col1.plotly_chart(
        fig,
        use_container_width = True,
        # sharing             = "streamlit" # depecrated
    )
    
    ####################
    # Plot 4: Location #
    ####################

    # Create plot dataframe from base dataframe
    groupby_clause = ['yyyy','start_stn_code','stn_lat','stn_lon']
    
    plot_df = df.groupby(
        by = groupby_clause).agg(     
            rides = ('rides','sum'),
            stn_name = ('stn_name', lambda x: x.iloc[-1]) # If the same latitude and longitude has multiple names, select the latest name
        )    

    # Calculate average from averages using harmonic mean
    plot_df['avg_dur_sec'] = df.groupby(
        by = groupby_clause).apply(lambda x: np.average(x.avg_dur_sec, weights = x.rides))

    # Reset index of plot dataframe
    plot_df.reset_index(inplace = True)

    # Rename columns for displaying in hover tool
    plot_df.rename(
        columns = 
        {
            "yyyy"        : "Year",
            "stn_lat"     : "Lat",
            "stn_lon"     : "Lon",
            "rides"       : "Trips",
            "stn_name"    : "Station Name",
            "avg_dur_sec" : "Avg. Trip Duration (min)"
        },
        inplace = True
    )

    # Convert seconds to minutes
    plot_df['Avg. Trip Duration (min)'] = plot_df['Avg. Trip Duration (min)']/60 

    # Define mapbox secret
    px.set_mapbox_access_token(open(".mapbox_token").read())

    # Create plotly express figure object
    fig = px.scatter_mapbox(
        plot_df,
        lat        = "Lat",
        lon        = "Lon",
        text       = "Station Name",
        title      = "Number of Bixi Trips by Station",
        hover_name = "Station Name",
        hover_data = {
            "Trips"                    : ":,",
            "Lat"                      : ":.3f",
            "Lon"                      : ":.3f",
            "Avg. Trip Duration (min)" : ":,.0f",
            "Station Name"             : False
        },
        size                   = "Trips",
        size_max               = 15,
        color                  = "Avg. Trip Duration (min)",
        zoom                   = 11,
        color_continuous_scale = "Oryel",
        # mapbox_style = 'dark',
        animation_frame        = 'Year')

    fig.update_layout(
        # Set title
        title = dict(
            x = 0.3,
            y = 0.95
        ),
    )

    # Too many layers deep to write in dictionary form. Since just 1, for simplicity, just explicitly set
    fig.layout.coloraxis.colorbar.title.text = "Avg. Trip<br>Dur. (min)"
    #################
    # END OF PLOT 4 #
    #################

    # Display plot 4 in column 2
    col2.plotly_chart(
        fig,
        use_container_width = True,
        # sharing = "streamlit" # depecrated
    )