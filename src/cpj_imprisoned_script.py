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
    Adding these columns allows us to sum/count each individual category separately.
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
    ax.set_xlabel('# Journalists Imprisoned')
    if topN:
        ax.set_title('# Journalists Imprisoned By ' + col_name + ' (Top ' + str(topN) +')')
    else:
        ax.set_title('# Journalists Imprisoned By ' + col_name)
    ax.invert_yaxis()
    return 


def plot_hbar_category_count(df, col_name, topN=None, dropna=False):
    '''
    Make a horizontal bar chart of category counts for a specified column in dataframe
    '''
    df_count = category_count_df_one_column(df, col_name, topN, dropna=False)
    _, ax = plt.subplots(1,figsize=(12,8))
    ax.barh(df_count[col_name], df_count['Count'])
    ax.set_xlabel('# Journalists Imprisoned')
    if topN:
        ax.set_title('# Journalists Imprisoned By ' + col_name + ' (Top ' + str(topN) +')')
    else:
        ax.set_title('# Journalists Imprisoned By ' + col_name)
    ax.invert_yaxis()
    return 


def clean_cpj_imprisoned(df):
    df.dropna(axis=1, how='all', inplace=True)
    df.dropna(axis=1, thresh=1000, inplace=True)
    df.drop(['combinedStatus','lastStatus','status','primaryNationality','organizations','healthProblems','sentence','locationImprisoned','type'], axis=1, inplace=True)
    df['employedAs'] = cpj['employedAs'].apply(lambda x: x.replace('staff','Staff') if type(x)==str else x)
    
    df = remove_spaces_in_category_lists(df, 'jobs')
    df['jobs'] = df['jobs'].apply(lambda x: x.replace('print reporter','Print Reporter') if type(x)==str else x)
    df['jobs'] = df['jobs'].apply(lambda x: x.replace('Print reporter','Print Reporter') if type(x)==str else x)
    df['jobs'] = df['jobs'].apply(lambda x: x.replace('Broadcast reporter','Broadcast Reporter') if type(x)==str else x)
    df['jobs'] = df['jobs'].apply(lambda x: x.replace(' Broadcast Reporter','Broadcast Reporter') if type(x)==str else x)
    df['jobs'] = df['jobs'].apply(lambda x: x.replace('Publisher/owner','Publisher/Owner') if type(x)==str else x)
    df['jobs'] = df['jobs'].apply(lambda x: x.replace('Internet reporter','Internet Reporter') if type(x)==str else x)
    df['jobs'] = df['jobs'].apply(lambda x: x.replace('Documentary filmmaker','Documentary Filmmaker') if type(x)==str else x)
    df['jobs'] = df['jobs'].apply(lambda x: x.replace('Columnist/commentator','Columnist/Commentator') if type(x)==str else x)
    df['jobs'] = df['jobs'].apply(lambda x: x.replace(' Editor','Editor') if type(x)==str else x)
    df['jobs'] = df['jobs'].apply(lambda x: x.replace('Camera operator','Camera Operator') if type(x)==str else x)

    df = remove_spaces_in_category_lists(df, 'coverage')
    df['coverage'] = df['coverage'].apply(lambda x: x.replace('Human rights','Human Rights') if type(x)==str else x)
    df['coverage'] = df['coverage'].apply(lambda x: x.replace('Human Rights`','Human Rights') if type(x)==str else x)
    df['coverage'] = df['coverage'].apply(lambda x: x.replace('politics','Politics') if type(x)==str else x)
    df['coverage'] = df['coverage'].apply(lambda x: x.replace('sports','Sports') if type(x)==str else x)

    df = remove_spaces_in_category_lists(df, 'mediums')
    df['mediums'] = df['mediums'].apply(lambda x: x.replace('print','Print') if type(x)==str else x)

    df = remove_spaces_in_category_lists(df, 'charges')
    df['charges'] = df['charges'].apply(lambda x: x.replace('False news','False News') if type(x)==str else x)
    df['charges'] = df['charges'].apply(lambda x: x.replace('false news','False News') if type(x)==str else x)
    df['charges'] = df['charges'].apply(lambda x: x.replace('Censorship violation','Censorship Violation') if type(x)==str else x)
    df['charges'] = df['charges'].apply(lambda x: x.replace('No charge','No Charge') if type(x)==str else x)
    df['charges'] = df['charges'].apply(lambda x: x.replace('No Charge disclosed','No Charge') if type(x)==str else x)
    df['charges'] = df['charges'].apply(lambda x: x.replace('Ethnic/Religious Insult','Ethnic or Religious Insult') if type(x)==str else x)
    df['charges'] = df['charges'].apply(lambda x: x.replace('Ethnic or religious insult','Ethnic or Religious Insult') if type(x)==str else x)
    df['charges'] = df['charges'].apply(lambda x: x.replace('Religious or ethnic insult','Ethnic or Religious Insult') if type(x)==str else x)
    df['charges'] = df['charges'].apply(lambda x: x.replace('retaliatory','Retaliatory') if type(x)==str else x)
    df['charges'] = df['charges'].apply(lambda x: x.replace('Anti-state','Anti-State') if type(x)==str else x)

    df['lengthOfSentence'] = df['lengthOfSentence'].apply(lambda x: x.replace('Not sentenced','Not Sentenced') if type(x)==str else x)
    df['lengthOfSentence'] = df['lengthOfSentence'].apply(lambda x: x.replace('not sentenced','Not Sentenced') if type(x)==str else x)
    df['lengthOfSentence'] = df['lengthOfSentence'].apply(lambda x: x.replace('not Sentenced','Not Sentenced') if type(x)==str else x)
    df['lengthOfSentence'] = df['lengthOfSentence'].apply(lambda x: x.replace('5-10 years','5-10 Years') if type(x)==str else x)
    df['lengthOfSentence'] = df['lengthOfSentence'].apply(lambda x: x.replace('0-5 years','0-5 Years') if type(x)==str else x)
    df['lengthOfSentence'] = df['lengthOfSentence'].apply(lambda x: x.replace('0-5 years','0-5 Years') if type(x)==str else x)
    df['lengthOfSentence'] = df['lengthOfSentence'].apply(lambda x: x.replace('10+ years','10+ Years') if type(x)==str else x)
    df['lengthOfSentence'] = df['lengthOfSentence'].apply(lambda x: x.replace('5 years to <10 years','5-10 Years') if type(x)==str else x)
    df['lengthOfSentence'] = df['lengthOfSentence'].apply(lambda x: x.replace('1 year to <5 years','0-5 Years') if type(x)==str else x)
    df['lengthOfSentence'] = df['lengthOfSentence'].apply(lambda x: x.replace('<1 year','0-5 Years') if type(x)==str else x)

    return df


if __name__=='__main__':

    cpj = pd.read_csv('./data/Journalists Imprisoned between 1992 and 2020.csv')
    cpj = clean_cpj_imprisoned(cpj)
    
    #
    plot_hbar_category_count_multiplecats(cpj, 'jobs', dropna=True)
    plt.savefig('./images/N_ImprisonedByjobs.png', bbox_inches='tight')

    #
    plot_hbar_category_count_multiplecats(cpj, 'coverage', dropna=True)
    plt.savefig('./images/N_ImprisonedBycoverage.png', bbox_inches='tight')

    #
    plot_hbar_category_count_multiplecats(cpj, 'mediums', dropna=True)
    plt.savefig('./images/N_ImprisonedBymedium.png', bbox_inches='tight')

    #
    plot_hbar_category_count_multiplecats(cpj, 'charges', dropna=True)
    plt.savefig('./images/N_ImprisonedBycharges.png', bbox_inches='tight')

    #
    plot_hbar_category_count(cpj, 'country', 20)
    plt.savefig('./images/N_ImprisonedBycountry.png', bbox_inches='tight')

    #
    plot_hbar_category_count_multiplecats(cpj, 'lengthOfSentence', dropna=True)
    plt.savefig('./images/N_ImprisonedBylengthOfSentence.png', bbox_inches='tight')

    # Plot Number of Journalists imprisoned per year
    cpj_GB_year_count = category_count_df_one_column(cpj,'year')
    _, ax = plt.subplots(1,figsize=(12,4))
    ax.bar(cpj_GB_year_count['year'],cpj_GB_year_count['Count'])
    ax.set_title('# Journalists Imprisoned Per Year')
    plt.savefig('./images/N_ImprisonedByYear.png', bbox_inches='tight')