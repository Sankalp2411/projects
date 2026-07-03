import sys
from pathlib import Path
ROOT_DIR = Path(__file__).resolve().parent.parent
sys.path.append(str(ROOT_DIR))
import pandas as pd
from config.project_config import (
    FEATURE_COLUMNS,
    RAIN_THRESHOLD_MM,
    HUMIDITY_THRESHOLD,
    RAW_WEATHER_DATA,
    PROCESSED_DATA
)
raw_path = ROOT_DIR / RAW_WEATHER_DATA
if not raw_path.exists():
    raise FileNotFoundError(f"Raw weather file not found: {raw_path}")
df = pd.read_csv(raw_path)
missing_cols = [col for col in FEATURE_COLUMNS if col not in df.columns]
if missing_cols:
    raise ValueError(f"Missing required columns: {missing_cols}")
df = df[FEATURE_COLUMNS]
df["temperature"] = df["temperature"].fillna(df["temperature"].mean())
df["humidity"] = df["humidity"].fillna(df["humidity"].mean())
df["rainfall"] = df["rainfall"].fillna(0)
df["cloudburst_label"] = (
    (df["rainfall"] >= RAIN_THRESHOLD_MM) &
    (df["humidity"] >= HUMIDITY_THRESHOLD)
).astype(int)
output_path = ROOT_DIR / PROCESSED_DATA
output_path.parent.mkdir(parents=True, exist_ok=True)
df.to_csv(output_path, index=False)