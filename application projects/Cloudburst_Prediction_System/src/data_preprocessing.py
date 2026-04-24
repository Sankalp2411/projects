# src/data_preprocessing.py
import pandas as pd
import os
RAW_DATA_PATH = "data/raw/weather_data.csv"
PROCESSED_DATA_PATH = "data/processed/cleaned_weather_data.csv"
CLOUD_BURST_THRESHOLD = 100  
def load_data(file_path):
    """Load CSV dataset"""
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File not found: {file_path}")
    df = pd.read_csv(file_path)
    return df
def clean_data(df):
    """Clean and preprocess dataset"""
    df = df.drop_duplicates()
    for col in ['temperature', 'humidity', 'pressure', 'wind_speed', 'cloud_cover']:
        if col in df.columns:
            df[col] = df[col].fillna(df[col].mean())
    if 'rainfall' in df.columns:
        df['rainfall'] = df['rainfall'].fillna(0)
    if 'timestamp' in df.columns:
        df['timestamp'] = pd.to_datetime(df['timestamp'])
    return df
def save_processed_data(df, output_path):
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    df.to_csv(output_path, index=False)
if __name__ == "__main__":
    df = load_data(RAW_DATA_PATH)
    df = clean_data(df)
    save_processed_data(df, PROCESSED_DATA_PATH)