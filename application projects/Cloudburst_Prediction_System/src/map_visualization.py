# src/map_visualization.py
import pandas as pd
import folium
from folium.plugins import MarkerCluster
PREDICTION_FILE = "data/cloudburst_predictions.csv"
OUTPUT_MAP_FILE = "maps/india_cloudburst_prediction.html"
df = pd.read_csv(PREDICTION_FILE)
required_cols = {"latitude", "longitude", "city", "cloudburst_risk"}
if not required_cols.issubset(df.columns):
    raise ValueError("Required columns missing in prediction file")
if df.empty:
    print("No predictions available")
    exit()
india_map = folium.Map(location=[22.0, 79.0], zoom_start=5)
marker_cluster = MarkerCluster().add_to(india_map)
for _, row in df.iterrows():
    color = "red" if row["cloudburst_risk"] == "High Risk" else "green"
    popup = f"""
    <b>City:</b> {row['city']}<br>
    <b>State:</b> {row.get('state', 'N/A')}<br>
    <b>Temperature:</b> {row['temperature']} °C<br>
    <b>Humidity:</b> {row['humidity']} %<br>
    <b>Rainfall:</b> {row['rainfall']} mm<br>
    <b>Cloudburst Risk:</b> {row['cloudburst_risk']}
    """
    folium.CircleMarker(
        location=[row["latitude"], row["longitude"]],
        radius=6,
        color=color,
        fill=True,
        fill_color=color,
        fill_opacity=0.7,
        popup=popup
    ).add_to(marker_cluster)
india_map.save(OUTPUT_MAP_FILE)