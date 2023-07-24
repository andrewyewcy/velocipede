def plot_histogram(df, col, df_name):
    """
    =======
    PURPOSE
    =======
    Given a pandas DataFrame and column, explores the distribution of the specified column by generating two subplots: one without any scaling of data and the other with LOG scaling.
    Subplot 1: A histogram without any transformations. The mean and median lines were included.
    Subplot 2: A hist
    Plots 2 subplots: 
    Left subplot: histogram without any transformation. The mean and median lines were included.
    Right subplot: histogram with LOG transformation and on LOG scale. The mean and median lines were included.

    ======
    INPUTS
    ======
    df      : a pandas DataFrame that contains numerical columns.
    col     : a string containing the name of the numerical column for which to plot histograms. 
    df_name : a string containing the name of the input dataframe, used for saving image name

    ======
    OUTPUT
    ======
    Two subplots detailing distribution of the numerical column.
    Subplot 1(LEFT): A histogram without any transformations. The mean and median lines were included.
    Subplot 2(RIGHT): A histogram with LOG transformation. The LOG mean and median lines were included.

    =======
    EXAMPLE
    =======
    Given pandas DataFrame 'df1' and numerical column 'col1':

    from common_functions.notebook_functions.plot import plot_histogram
    plot_histogram(df1,'col1','df1')

    >>>Histogram Sub-plots for col1
    >>>Subplot 1
    >>>Subplot 2
    '''
    
    assert(isinstance(df, pd.DataFrame), "Passed object is not a DataFrame")
    assert(isinstance(col, string),"Passed object is not a string")
    
    
    print(f"===== Distribution Plots for {col} =====")
    
    # Create subplot object with 1 row and 2 columns
    plt.subplots(1, 2, figsize = (15,5))

    # Calculate the summary statistics for column
    col_mean = np.mean(df[col].dropna())
    col_median = np.median(df[col].dropna())

    # Plot first histogram to show distribution as is
    plt.subplot(1,2,1)
    sns.histplot(data = df, x = col, stat = 'probability');
    plt.axvline(col_mean, linestyle = '-', c = 'red', label = f"mean: {np.round(col_mean,2)}")
    plt.axvline(col_median, linestyle = '--', c = 'red', label = f"median: {np.round(col_median,2)}")
    plt.legend()
    plt.title(f"Distribution for {col}", y = -0.05)

    # Calculate log of column
    log_df = np.log(df[[col]].dropna()+1)
    log_col_mean = np.mean(log_df[col])
    log_col_median = np.median(log_df[col])

    # Plot second histogram to show LOG distribution
    plt.subplot(1,2,2)
    sns.histplot(data = log_df, x = col, stat = 'probability');
    plt.axvline(log_col_mean, linestyle = '-', c = 'red', label = f"mean: {np.round(log_col_mean,2)}")
    plt.axvline(log_col_median, linestyle = '--', c = 'red', label = f"median: {np.round(log_col_median,2)}")
    plt.xlabel(f"LOG {col}")
    plt.legend()
    plt.title(f"LOG Distribution for {col}", y = -0.05)

    sns.despine()
    plt.show()
    plt.savefig(
        f"assets/images/histogram_{df_name}_{col}.png",
        format = "png",
        dpi = 300
        )
    print(f"===============================================")
    print(f"")
    print(f"")