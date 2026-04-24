# src/fetch_weather.py
import os
import requests
import pandas as pd
from datetime import datetime
API_KEY = "f721ec92f16714f2deb81dd002027d28"
BASE_URL = "https://api.openweathermap.org/data/2.5/weather"
CITY_FILE = "data/indian_cities.csv"
OUTPUT_DIR = "data/weather_data"
COMBINED_FILE = "data/combined_weather_data.csv"
os.makedirs(OUTPUT_DIR, exist_ok=True)
if not os.path.exists(CITY_FILE):
    raise FileNotFoundError(f"City file not found: {CITY_FILE}")
cities_df = pd.read_csv(CITY_FILE)
all_weather_records = []
for _, row in cities_df.iterrows():
    city = row["City"]
    state = row["State"]
    params = {
        "q": f"{city},IN",
        "appid": API_KEY,
        "units": "metric"
    }
    response = requests.get(BASE_URL, params=params)
    if response.status_code != 200:
        continue
    data = response.json()
    record = {
        "city": city,
        "state": state,
        "latitude": data["coord"]["lat"],
        "longitude": data["coord"]["lon"],
        "temperature": data["main"]["temp"],
        "humidity": data["main"]["humidity"],
        "pressure": data["main"]["pressure"],
        "wind_speed": data["wind"]["speed"],
        "rainfall": data.get("rain", {}).get("1h", 0),
        "cloud_cover": data["clouds"]["all"],
        "weather_description": data["weather"][0]["description"],
        "datetime": datetime.now()
    }
    city_file = os.path.join(OUTPUT_DIR, f"{city}.csv")
    pd.DataFrame([record]).to_csv(city_file, index=False)
    all_weather_records.append(record)
if not all_weather_records:
    print("No weather data collected")
    exit()
combined_df = pd.DataFrame(all_weather_records)
combined_df.to_csv(COMBINED_FILE, index=False)