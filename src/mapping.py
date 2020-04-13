import pandas as pd
import folium
import wget
import os
import time
from selenium import webdriver
import imageio


def make_Choropleth_map(geo_data, count_df, legend_name, bins=None):
    '''
    Make a Chorpleth map w/ folium
    '''
    m = folium.Map(location=[30, 0], zoom_start=2, tiles='CartoDB positron')

    if bins:
        folium.Choropleth(geo_data=geo_data,
                data=count_df,
                columns=['country', 'Count'],
                key_on='feature.properties.name',
                nan_fill_color='white',
                fill_color='YlGnBu', fill_opacity=0.7, line_opacity=0.2,
                legend_name=legend_name,
                bins=bins,
                highlight=True).add_to(m)
    else:
        folium.Choropleth(geo_data=geo_data,
                data=count_df,
                columns=['country', 'Count'],
                key_on='feature.properties.name',
                nan_fill_color='white',
                fill_color='YlGnBu', fill_opacity=0.7, line_opacity=0.2,
                legend_name=legend_name,
                highlight=True).add_to(m)
    return m


if __name__=='__main__':

    # Download world countries geojson file needed to make folium Choropleth map
    countries_url = 'https://raw.githubusercontent.com/python-visualization/folium/master/examples/data/world-countries.json'
    wget.download(countries_url,'./data/world-countries.json')
    country_geo = './data/world-countries.json'

    # 
    cpj = pd.read_csv('./data/Journalists Killed between 1992 and 2020.csv')
    cpj = cpj[cpj['motiveConfirmed']=='Confirmed']
    
    # Make map of total deaths by country for all years
    cpj_GB_country_count = cpj.groupby('country').count().reset_index().loc[:,['country','year']].sort_values('year',ascending=False)
    cpj_GB_country_count.rename(columns={'year':'Count'},inplace=True)
    m = make_Choropleth_map(country_geo, cpj_GB_country_count, 'Journalists Killed')
    m.save('./maps/DeathsByCountry.html')

    # Make html map for each individual year
    for year in range(1992,2020):
        # filter by year, group by country, count
        cpj_GB_country_count = cpj[cpj['year']==year].groupby('country').count().reset_index().loc[:,['country','year']].sort_values('year',ascending=False)
        cpj_GB_country_count.rename(columns={'year':'Count'},inplace=True)

        m = make_Choropleth_map(country_geo, cpj_GB_country_count, 'Journalists Killed in ' + str(year), bins = [0,10,20,30,40,50,60])
        m.save('./maps/DeathsByCountry_' + str(year) + '.html')

    
    # Make png images of maps by taking screenshots
    # folder with all the saved html maps I made above
    map_dir = os.path.join(os.getcwd(), 'maps/')
    # open browser; can take a few secs first time
    browser = webdriver.Firefox()
    time.sleep(30)
    for file_name in sorted(os.listdir(map_dir)):
        if file_name.startswith('DeathsByCountry') and file_name.endswith('.html'):
            tmpurl = 'file:' + map_dir + file_name
            print(tmpurl)
            # download screenshot of map
            delay = 10
            print('\n Opening map file in browser')
            browser.get(tmpurl)
            # give the map tiles some time to load
            time.sleep(delay)
            save_filename = map_dir + file_name[0:len(file_name)-5] + '.png'
            #print(save_filename)
            browser.save_screenshot(save_filename)
    browser.quit()
    

    # make gif from png images
    images = []
    # NOTE make sure to use *sorted*, as os.listdir() generally doesn't return sorted filenames (depends on filesystem etc.)
    for file_name in sorted(os.listdir(map_dir)):
        if file_name.startswith('DeathsByCountry_') and file_name.endswith('.png') :
            file_path = os.path.join(map_dir, file_name)
            #print(file_path)
            images.append(imageio.imread(file_path))
    # Make fps smaller to make gif go slower, larger to go faster...
    imageio.mimsave('./images/DeathByCountry.gif', images, fps=1)


    # repeat process for CPJ imprisoned dataset   
    del cpj
    cpj = pd.read_csv('./data/Journalists Imprisoned between 1992 and 2020.csv')
    cpj_GB_country_count = cpj.groupby('country').count().reset_index().loc[:,['country','year']].sort_values('year',ascending=False)
    cpj_GB_country_count.rename(columns={'year':'Count'},inplace=True)
    m = make_Choropleth_map(country_geo, cpj_GB_country_count, 'Journalists Imprisoned')
    m.save('./maps/ImprisonedByCountry.html')

    # Make html maps for each year
    for year in range(1992,2020):
        # filter by year, group by country, count
        cpj_GB_country_count = cpj[cpj['year']==year].groupby('country').count().reset_index().loc[:,['country','year']].sort_values('year',ascending=False)
        cpj_GB_country_count.rename(columns={'year':'Count'},inplace=True)

        m = make_Choropleth_map(country_geo, cpj_GB_country_count, 'Journalists Imprisoned in ' + str(year), bins = [0,10,20,30,40,50,60,70,80,90])
        m.save('./maps/ImprisonedByCountry_' + str(year) + '.html')

    
    # Make png images of maps by taking screenshots
    # folder with all the saved html maps made above
    map_dir = os.path.join(os.getcwd(), 'maps/')
    # open browser; can take a few secs first time
    browser = webdriver.Firefox()
    time.sleep(30)
    for file_name in sorted(os.listdir(map_dir)):
        if file_name.startswith('ImprisonedByCountry') and file_name.endswith('.html'):
            tmpurl = 'file:' + map_dir + file_name
            print(tmpurl)
            # download screenshot of map
            delay = 10
            print('\n Opening map file in browser')
            browser.get(tmpurl)
            # give the map tiles some time to load
            time.sleep(delay)
            save_filename = map_dir + file_name[0:len(file_name)-5] + '.png'
            #print(save_filename)
            browser.save_screenshot(save_filename)
    browser.quit()
    

    # make gif from png images
    images = []
    # NOTE make sure to use *sorted*, as os.listdir() generally doesn't return sorted filenames (depends on filesystem etc.)
    for file_name in sorted(os.listdir(map_dir)):
        if file_name.startswith('ImprisonedByCountry_') and file_name.endswith('.png') :
            file_path = os.path.join(map_dir, file_name)
            #print(file_path)
            images.append(imageio.imread(file_path))
    # Make fps smaller to make gif go slower, larger to go faster...
    imageio.mimsave('./images/ImprisonedByCountry.gif', images, fps=1)

