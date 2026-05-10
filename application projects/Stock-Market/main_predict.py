import numpy as np
import pandas as pd
import torch
import torch.nn as nn
import yfinance as yf
from sklearn.preprocessing import MinMaxScaler

from models.lstm_model import LSTMModel


def run_prediction(symbol, period, epochs, window, sims):
    df = yf.download(symbol, period=period, progress=False)

    if df.empty:
        raise RuntimeError("No data")

    prices = df["Close"].values.reshape(-1, 1)

    scaler = MinMaxScaler()
    scaled = scaler.fit_transform(prices)

    X, y = [], []
    for i in range(window, len(scaled)):
        X.append(scaled[i - window:i])
        y.append(scaled[i])

    X = torch.tensor(np.array(X), dtype=torch.float32)
    y = torch.tensor(np.array(y), dtype=torch.float32)

    model = LSTMModel(input_size=1)
    optimizer = torch.optim.Adam(model.parameters(), lr=0.001)
    loss_fn = nn.MSELoss()

    # TRAIN
    for _ in range(epochs):
        for i in range(len(X)):
            out = model(X[i].unsqueeze(0))
            loss = loss_fn(out, y[i].unsqueeze(0))  # ✅ FIXED SHAPE

            optimizer.zero_grad()
            loss.backward()
            optimizer.step()

    # PREDICT
    preds = []
    for i in range(len(X)):
        pred = model(X[i].unsqueeze(0)).detach().numpy()
        preds.append(pred[0][0])

    preds = scaler.inverse_transform(np.array(preds).reshape(-1, 1)).flatten()
    real = prices.flatten()

    return {
        "real": real,
        "pred": np.concatenate([np.zeros(window), preds])  # align graph
    }