key = "10e2b5e7a9650662f3563651869e0c78ddcfaf5cdcf184978d723c4013802e08"

# import json
# from openaq import OpenAQ

# client = OpenAQ(api_key= key)
# response = client.measurements.list(sensors_id=3917, data="days", rollup="yearly", limit=1000)

# print(response)

import httpx
import pandas as pd
from datetime import datetime

sensor_id = 9552925

# For yearly aggregated data (recommended for 8+ years of data)
url = f"https://api.openaq.org/v3/sensors/{sensor_id}/years"

headers = {"X-API-Key": key}
params = {
    "limit": 1000,
    "page": 1
}

try:
    with httpx.Client(timeout=30.0) as client:
        response = client.get(url, params=params, headers=headers)
        response.raise_for_status()
        data = response.json()
        
        print(f"Found: {data['meta']['found']} yearly measurements")
        
        # Convert to DataFrame
        results = data['results']
        df = pd.DataFrame(results)
        
        # Extract nested fields if needed
        if len(df) > 0:
            df['year'] = df['period'].apply(lambda x: x['datetimeFrom']['local'][:4])
            print("\nYearly O3 averages:")
            print(df[['year', 'value']].head(20))
            
except Exception as e:
    print(f"Error: {e}")



import httpx
import pandas as pd

location_id = 2891221


# 1. Get sensors associated with this location
url = f"https://api.openaq.org/v3/locations/{location_id}/sensors"

headers = {"X-API-Key": key}
params = {"limit": 1000}

try:
    with httpx.Client(timeout=30.0) as client:
        r = client.get(url, params=params, headers=headers)
        r.raise_for_status()
        sensors = r.json()
        
        print("Sensors under this location:")
        for s in sensors["results"]:
            print(f"- Sensor ID {s['id']}: {s['parameter']}")

except Exception as e:
    print(f"Error: {e}")
