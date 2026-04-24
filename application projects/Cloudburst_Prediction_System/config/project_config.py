# config/project_config.py
"""
Central configuration file for Cloudburst Prediction Project
This file acts as a SINGLE SOURCE OF TRUTH
"""
FEATURE_COLUMNS = [
    "temperature",
    "humidity",
    "rainfall"
]
RAIN_THRESHOLD_MM = 100
HUMIDITY_THRESHOLD = 85
HIGH_RISK_PROBABILITY = 0.7
RAW_WEATHER_DATA = "data/combined_weather_data.csv"
PROCESSED_DATA = "data/processed/ml_ready_weather_data.csv"
MODEL_PATH = "models/cloudburst_model.pkl"
PREDICTION_OUTPUT = "data/cloudburst_predictions.csv"