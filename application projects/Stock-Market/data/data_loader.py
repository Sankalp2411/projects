#data/data_loader.py
import yfinance as yf
import numpy as np
import pandas as pd
def load_stock_data(symbol, period):
    df = yf.download(symbol, period=period, progress=False)
    # Flatten MultiIndex columns from newer yfinance versions
    if isinstance(df.columns, pd.MultiIndex):
        df.columns = df.columns.get_level_values(0)
    if df.empty or "Close" not in df.columns:
        raise RuntimeError("Failed to download stock data")
    return np.asarray(df["Close"].values, dtype=np.float64).flatten()