import requests
import pandas as pd
import time

API_KEY = "10e2b5e7a9650662f3563651869e0c78ddcfaf5cdcf184978d723c4013802e08"
BASE_URL = "https://api.openaq.org/v3/locations"

df = pd.read_csv("US_Locations_Sampled.csv")
df["PM2.5 Sensor ID"] = None

for i, loc_id in enumerate(df["Location ID"]):
    if i % 60 == 0 and i > 0:
        print("Sleeping 60 seconds to respect API rate limit...")
        time.sleep(60)

    url = f"{BASE_URL}/{loc_id}/sensors"
    params = {"parameter": "pm25", "limit": 100}
    headers = {"x-api-key": API_KEY}

    try:
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()
        data = response.json()

        if data.get("results"):
            pm25_sensors = [
                s["id"] for s in data["results"]
                if s.get("parameter", {}).get("name") == "pm25"
            ]
            df.loc[i, "PM2.5 Sensor ID"] = ", ".join(map(str, pm25_sensors)) if pm25_sensors else None
        else:
            df.loc[i, "PM2.5 Sensor ID"] = None

    except Exception as e:
        print(f"Error fetching data for location {loc_id}: {e}")
        df.loc[i, "PM2.5 Sensor ID"] = None

df.to_csv("US_Locations_Sampled_with_PM25.csv", index=False)
print("✅ Done! Saved as US_Locations_Sampled_with_PM25.csv")
