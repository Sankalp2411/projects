import pandas as pd
import folium
from folium.plugins import MarkerCluster
from branca.element import Element
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
    high_risk_df = df[df["cloudburst_risk"] == "High Risk"]
    if len(high_risk_df) > 0:
        city_rows = ""
        for city in sorted(high_risk_df["city"].unique()):
            city_rows += f"<tr><td>{city}</td></tr>"
    else:
        city_rows = """
        <tr>
            <td>No cities at risk</td>
        </tr>
        """
    table_html = f"""
    <div style="
    position: fixed;
    up: 50px;
    right: 50px;
    z-index: 9999;
    background-color: white;
    border: 2px solid white;
    border-radius: 8px;
    width: 220px;
    max-height: 300px;
    overflow-y: auto;
    box-shadow: 3px 3px 10px rgba(0,0,0,0.3);
    font-size: 14px;
    ">
    <h4 style="margin-top:0;text-align:center;">
    High Risk Cities
    </h4>
    <table style="
    width:100%;
    border-collapse: collapse;
    ">
    {city_rows}
    </table>
    </div>
    """

    india_map.get_root().html.add_child(
        Element(table_html)
    )
india_map.save(OUTPUT_MAP_FILE)