import argparse
import numpy as np
import matplotlib.pyplot as plt
import yfinance as yf

from sklearn.preprocessing import MinMaxScaler
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense, Dropout
parser = argparse.ArgumentParser(description="Stock Price Predictor (LSTM, TF2)")
parser.add_argument("--symbol", type=str, required=True)
parser.add_argument("--period", type=str, default="1y")
parser.add_argument("--epochs", type=int, default=10)
parser.add_argument("--window", type=int, default=30)
args = parser.parse_args()
df = yf.download(args.symbol, period=args.period, progress=False)
if df.empty or "Close" not in df.columns:
    raise RuntimeError("Failed to download stock data")
prices = np.asarray(df["Close"].values, dtype=np.float64).reshape(-1, 1)
scaler = MinMaxScaler(feature_range=(0, 1))
scaled_prices = scaler.fit_transform(prices)
X, y = [], []
for i in range(args.window, len(scaled_prices)):
    X.append(scaled_prices[i - args.window : i])
    y.append(scaled_prices[i])
X = np.array(X, dtype=np.float32)
y = np.array(y, dtype=np.float32)
model = Sequential([
    LSTM(64, return_sequences=True, input_shape=(args.window, 1)),
    Dropout(0.2),
    LSTM(64),
    Dense(1)
])
model.compile(
    optimizer="adam",
    loss="mse"
)
model.fit(
    X,
    y,
    epochs=args.epochs,
    batch_size=32,
    verbose=1
)
pred_scaled = model.predict(X)
predicted_prices = scaler.inverse_transform(pred_scaled)
real_prices = scaler.inverse_transform(y)
FUTURE_DAYS = 10
last_window = scaled_prices[-args.window:].copy()
future_scaled = []
for _ in range(FUTURE_DAYS):
    next_price = model.predict(last_window.reshape(1, args.window, 1), verbose=0)
    future_scaled.append(next_price[0, 0])
    last_window = np.vstack([last_window[1:], next_price])
future_prices = scaler.inverse_transform(
    np.array(future_scaled).reshape(-1, 1)
).flatten()
plt.figure(figsize=(15, 5))
plt.plot(prices, label="Historical Price", linewidth=2)
plt.plot(
    range(args.window, args.window + len(predicted_prices)),
    predicted_prices,
    label="Model Prediction",
    alpha=0.8,
)
plt.plot(
    range(len(prices), len(prices) + FUTURE_DAYS),
    future_prices,
    "--",
    label="Future Forecast",
    linewidth=2,
)
plt.title(f"{args.symbol} Price Prediction")
plt.xlabel("Time")
plt.ylabel("Price")
plt.legend()
plt.grid(True)
plt.show()