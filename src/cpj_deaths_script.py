import pandas as pd
import matplotlib.pyplot as plt


# make plots look nice
plt.rcParams['font.size'] = 14
plt.rcParams['axes.labelsize'] = 'large'
plt.rcParams['xtick.labelsize'] = 'large'
plt.rcParams['ytick.labelsize'] = 'large'
plt.rcParams['lines.linewidth'] = 3
plt.style.use('ggplot')


def get_unique_category_vals(df, col_name, dropna=False):
    '''
    Find unique category values for specified column in a dataframe, where some rows 
    contain multiple categories separated by commas.
    '''
    unique_entries = list(cpj[col_name].unique())
    unique_entries = list(map(str,unique_entries))
    unique_entries_split = list(map(lambda x: x.split(','),unique_entries))
    unique_vals = set([val for sublist in unique_entries_split for val in sublist])
    if dropna:
        unique_vals.remove('nan')
    return(unique_vals)


def add_category_counts_to_df(df, col_name, dropna=False):
    '''
    Add boolean columns to dataframe for each unique category in col_name indicating if that category 
    was present in col_name. Useful when some rows of col_name contain multiple categories separated by commas.
    Adding these columns allows us to sum/count each individual category separately (see count_categories function).
    '''
    df_new = df.copy()
    unique_vals = get_unique_category_vals(df_new, col_name, dropna)
    
    for val in unique_vals:
        df_new[col_name + '_' + val] = df_new[col_name].apply(str).apply(lambda x: x.split(',')).apply(lambda x: val in x)
    return df_new


def count_categories(df, col_name, dropna=False):
    '''
    Return a dataframe with sums of all columns starting with 'col_name' (specifically those made w/ add_category_counts_to_df function)
    '''
    df_count=add_category_counts_to_df(df, col_name, dropna)
    df_count=df_count.filter(regex='^' + col_name, axis=1).sum().to_frame(name='Count').reset_index().rename(columns={'index':col_name}).sort_values('Count',ascending=False)
    df_count[col_name]=df_count[col_name].apply(lambda x: x.replace(col_name +'_',''))
    return df_count


def remove_spaces_in_category_lists(df, col_name):
    '''
    Remove spaces in rows of col_name where a list of categories (separated by commas) is given
    
    Example: ['Camera Operator, Internet Reporter, Print reporter'] > ['Camera Operator,Internet Reporter,Print reporter']
    
    '''
    df[col_name] = df[col_name].apply(lambda x: x.replace(',  ',',') if type(x)==str else x)
    df[col_name] = df[col_name].apply(lambda x: x.replace(', ',',') if type(x)==str else x)
    return df


def category_count_df_one_column(df, col_name, topN=None ,dropna=False):
    '''
    Make dataframe with category counts for a specified column
    
    INPUT
    df : Pandas Dataframe
    col_name : (str) Name of column to count
    drop_na : (bool) (optional) Whether or not to include NaNs in counts
    
    OUTPUT
    df_count : Pandas dataframe with 2 columns: col_name and Count
    '''
    df_count = cpj[col_name].value_counts(dropna).to_frame().reset_index().rename(columns={col_name:'Count','index':col_name})
    if topN:
        df_count = df_count.head(topN)
    return df_count


def plot_hbar_category_count_multiplecats(df, col_name, topN=None, dropna=False):
    '''
    Make a horizontal bar chart of category counts for a specified column in dataframe. 
    This function is specifically designed for columns that contain a string list of several
    values. See functions add_category_counts_to_df and count_categories
    '''
    df_count = count_categories(df, col_name, dropna)
    _, ax = plt.subplots(1,figsize=(12,8))
    ax.barh(df_count[col_name], df_count['Count'])
    ax.set_xlabel('# Journalists Killed')
    if topN:
        ax.set_title('# Journalists Killed By ' + col_name + ' (Top ' + str(topN) +')')
    else:
        ax.set_title('# Journalists Killed By ' + col_name)
    ax.invert_yaxis()
    return 


def plot_hbar_category_count(df, col_name, topN=None, dropna=False):
    '''
    Make a horizontal bar chart of category counts for a specified column in dataframe
    '''
    df_count = category_count_df_one_column(df, col_name, topN, dropna=False)
    _, ax = plt.subplots(1,figsize=(12,8))
    ax.barh(df_count[col_name], df_count['Count'])
    ax.set_xlabel('# Journalists Killed')
    if topN:
        ax.set_title('# Journalists Killed By ' + col_name + ' (Top ' + str(topN) +')')
    else:
        ax.set_title('# Journalists Killed By ' + col_name)
    ax.invert_yaxis()
    return 


if __name__=='__main__':

    cpj = pd.read_csv('./data/Journalists Killed between 1992 and 2020.csv')
    cpj.dropna(axis=1, how='all', inplace=True)
    cpj.dropna(axis=1, thresh=1000, inplace=True)
    cpj = cpj[cpj['motiveConfirmed']=='Confirmed']
    cpj.drop(['status','type','employedAs','location','locality'], axis=1, inplace=True)
    cpj.drop(['primaryNationality','organizations','motiveConfirmed','combinedStatus'], axis=1, inplace=True)
    cpj['jobs'] = cpj['jobs'].apply(lambda x: x.replace('Broadcast reporter','Broadcast Reporter') if type(x)==str else x)
    cpj = remove_spaces_in_category_lists(cpj, 'sourcesOfFire')
    

    # Plot Number of Journalists killed per year
    cpj_GB_year_count = category_count_df_one_column(cpj,'year')
    _, ax = plt.subplots(1,figsize=(12,4))
    ax.bar(cpj_GB_year_count['year'],cpj_GB_year_count['Count'])
    ax.set_xlabel('Year')
    ax.set_xlabel('# Journalists Killed')
    ax.set_title('# Journalists Killed Per Year')
    plt.savefig('./images/TotalDeathsVsYear.png', bbox_inches='tight')

    #
    plot_hbar_category_count_multiplecats(cpj, 'jobs', dropna=True)
    plt.savefig('./images/TotalDeathsByJob.png',bbox_inches='tight')

    #
    plot_hbar_category_count_multiplecats(cpj, 'coverage', dropna=True)
    plt.savefig('./images/TotalDeathsByCoverage.png',bbox_inches='tight')

    #
    cpj_GB_yeargender_count = cpj.groupby(['year','gender']).count().unstack(fill_value=0).stack().reset_index().loc[:,['year','gender','combinedStatus']]
    cpj_GB_yeargender_count.rename(columns={'combinedStatus':'Count'},inplace=True)
 
    fig, ax = plt.subplots(1,figsize=(12,6))
    ax.bar(cpj_GB_yeargender_count[cpj_GB_yeargender_count['gender']=='Female']['year'],cpj_GB_yeargender_count[cpj_GB_yeargender_count['gender']=='Female']['Count'],color='red',label='female')
    ax.bar(cpj_GB_yeargender_count[cpj_GB_yeargender_count['gender']=='Male']['year'],cpj_GB_yeargender_count[cpj_GB_yeargender_count['gender']=='Male']['Count'],color='blue', label='male',bottom=cpj_GB_yeargender_count[cpj_GB_yeargender_count['gender']=='Female']['Count'])
    ax.legend()
    ax.set_title('# Journalists Killed Per Year')
    plt.savefig('./images/TotalDeathsVsYear_GenderStack.png',bbox_inches='tight')

    #
    plot_hbar_category_count(cpj, 'country', 20)
    plt.savefig('./images/TotalDeathsByCountry.png',bbox_inches='tight')

    #
    plot_hbar_category_count(cpj, 'primaryNationality',20)
    plt.savefig('./images/TotalDeathsByNationality.png',bbox_inches='tight')

    #
    plot_hbar_category_count_multiplecats(cpj, 'sourcesOfFire', dropna=True)
    plt.savefig('./images/TotalDeathsBysourcesOfFire.png',bbox_inches='tight')

    #
    plot_hbar_category_count(cpj, 'typeOfDeath', dropna=False)
    plt.savefig('./images/TotalDeathsByTypeOfDeath.png',bbox_inches='tight')