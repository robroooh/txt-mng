import glob
import os
import folium
from folium import plugins
import pandas as pd
import webbrowser

# get source file names. police.uk data files are separated into respective month.
YEAR = '2017'
MONTH = '12'
met_path = "/home/r/Codes/txt-mng/crimedata/af801e3fc2a2673598aee1987e0f87c3e6b2936c"
os.chdir(met_path)
source_csvs = glob.glob("*/*.csv")
#%%
print(source_csvs)
temp_dflist = []
streetcrime_df = pd.DataFrame()
for csv in source_csvs:
    year, month = csv.split('-')[0], csv.split('-')[1]
    print(year)
    df = pd.read_csv(csv, index_col=None, header=0)
    df['Year'] = year
    df['Month'] = month
    temp_dflist.append(df)

streetcrime_df = pd.concat(temp_dflist)

# cleanse the data, dropping any rows without location info
streetcrime_df.dropna(subset=['Latitude', 'Longitude'], inplace=True)

# make another dataframe which includes only the data from specified year-month.
periodic_df = streetcrime_df[(streetcrime_df['Year'] == YEAR) & (streetcrime_df['Month'] == MONTH) & (
            streetcrime_df['Crime type'] == 'Violence and sexual offences')]
crime_locations = list(zip(periodic_df.Latitude, periodic_df.Longitude))

# generate map
base_map = folium.Map(location=[51.5074, 0.1277], zoom_start=10)
heatmap = plugins.HeatMap(crime_locations, radius=5, blur=2)
base_map.add_child(heatmap)
# Path to save heatmap
base_map.save('Heatmap8.html')

webbrowser.open('Heatmap8.html')

