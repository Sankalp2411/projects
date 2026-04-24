# app.py
import subprocess
import webbrowser
from pathlib import Path
ROOT_DIR = Path(__file__).resolve().parent
MAP_FILE = ROOT_DIR / "maps" / "india_cloudburst_prediction.html"
print("Starting Cloudburst Prediction Pipeline...")
subprocess.run(["python", "src/fetch_weather.py"], check=True)
subprocess.run(["python", "src/data_preprocessing.py"], check=True)
subprocess.run(["python", "src/feature_engineering.py"], check=True)
subprocess.run(["python", "src/model_training.py"], check=True)
subprocess.run(["python", "src/predict_cloudburst.py"], check=True)
subprocess.run(["python", "src/map_visualization.py"], check=True)
if MAP_FILE.exists():
    webbrowser.open(f"file://{MAP_FILE.resolve()}")
else:
    print("Map file not found!")
print("Cloudburst Prediction Pipeline completed successfully!")