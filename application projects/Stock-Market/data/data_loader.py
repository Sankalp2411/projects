import yfinance as yf
import numpy as np

def load_stock_data(symbol, period):
    df = yf.download(symbol, period=period, progress=False)

    if df.empty or "Close" not in df.columns:
        raise RuntimeError("Failed to download stock data")

    return np.asarray(df["Close"].values, dtype=np.float64).flatten()