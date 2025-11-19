key = "10e2b5e7a9650662f3563651869e0c78ddcfaf5cdcf184978d723c4013802e08"

import httpx
import pandas as pd
import requests
import geopandas as gpd
from shapely.geometry import Point


headers = {"X-API-Key": key}
params = {
    "limit": 1000,
    "page": 1
}

base_url = "https://api.openaq.org/v3/locations"
all_locations = []
page = 1

while True:
    params = {
        'countries_id': 155,  
        'limit': 1000,
        'page': page
    }
    
    response = requests.get(base_url, params=params, headers=headers)
    
 
    if response.status_code != 200:
        print(f"Error: {response.status_code}")
        print(response.text)
        break
    
    data = response.json()
    
  
    if page == 1:
        print(f"Response keys: {data.keys()}")
        print(f"Meta info: {data.get('meta', {})}")
    
    results = data.get('results', [])

    if not results or len(results) == 0:
        break
    
    all_locations.extend(results)
    
    if len(results) < 1000:
        break
    
    page += 1
    

print(f"\nTotal locations found: {len(all_locations)}")



locations_df = pd.DataFrame([
    {
        'Location ID': loc['id'],
        'Name': loc['name'],
        'Latitude': loc.get('coordinates', {}).get('latitude'),
        'Longitude': loc.get('coordinates', {}).get('longitude')
    }
    for loc in all_locations
])


geometry = [Point(xy) for xy in zip(locations_df['Longitude'], locations_df['Latitude'])]

locations_gdf = gpd.GeoDataFrame(
    locations_df, 
    geometry=geometry, 
    crs="EPSG:4326"
)


states = gpd.read_file('https://www2.census.gov/geo/tiger/GENZ2018/shp/cb_2018_us_state_20m.zip')
states = states.to_crs("EPSG:4326")

result = gpd.sjoin(locations_gdf, states, how="left", predicate="within")

locations_df['State'] = result['NAME'].values
locations_df['Abbreviation'] = result['STUSPS'].values


locations_df.to_csv('US_Locations.csv', index=False)