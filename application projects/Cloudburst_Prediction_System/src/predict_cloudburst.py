import sys
from pathlib import Path
import pandas as pd
import pickle
ROOT_DIR = Path(__file__).resolve().parent.parent
sys.path.append(str(ROOT_DIR))
from config.project_config import (
    FEATURE_COLUMNS,
    RAW_WEATHER_DATA,
    MODEL_PATH,
    PREDICTION_OUTPUT,
    HIGH_RISK_PROBABILITY
)
data_path = ROOT_DIR / RAW_WEATHER_DATA
if not data_path.exists():
    raise FileNotFoundError(f"Weather data file not found: {data_path}")
df = pd.read_csv(data_path)
if df.empty:
    print("No data available for prediction")
    df.to_csv(ROOT_DIR / PREDICTION_OUTPUT, index=False)
    exit()
model_path = ROOT_DIR / MODEL_PATH
if not model_path.exists():
    raise FileNotFoundError(f"Model not found. Train the model first: {model_path}")
with open(model_path, "rb") as f:
    model = pickle.load(f)
missing_cols = [c for c in FEATURE_COLUMNS if c not in df.columns]
if missing_cols:
    raise ValueError(f"Missing required feature columns: {missing_cols}")
X = df[FEATURE_COLUMNS].copy()
X["temperature"] = X["temperature"].fillna(X["temperature"].mean())
X["humidity"] = X["humidity"].fillna(X["humidity"].mean())
X["rainfall"] = X["rainfall"].fillna(0)
probabilities = model.predict_proba(X)[:, 1]
predictions = (probabilities >= HIGH_RISK_PROBABILITY).astype(int)
df["cloudburst_probability"] = probabilities.round(3)
df["cloudburst_prediction"] = predictions
df["cloudburst_risk"] = df["cloudburst_prediction"].map(
    {0: "Low Risk", 1: "High Risk"}
)
output_path = ROOT_DIR / PREDICTION_OUTPUT
output_path.parent.mkdir(parents=True, exist_ok=True)
df.to_csv(output_path, index=False)