import argparse
import numpy as np
import torch
import torch.nn as nn
import matplotlib.pyplot as plt
from sklearn.preprocessing import MinMaxScaler

from data.data_loader import load_stock_data
from models.lstm_model import LSTMModel

parser = argparse.ArgumentParser()
parser.add_argument("--symbol", required=True)
parser.add_argument("--period", default="1y")
parser.add_argument("--epochs", type=int, default=10)
parser.add_argument("--window", type=int, default=30)

args = parser.parse_args()

prices = load_stock_data(args.symbol, args.period).reshape(-1, 1)

scaler = MinMaxScaler()
scaled = scaler.fit_transform(prices)

X, y = [], []
for i in range(args.window, len(scaled)):
    X.append(scaled[i-args.window:i])
    y.append(scaled[i])

X = torch.tensor(np.array(X), dtype=torch.float32)
y = torch.tensor(np.array(y), dtype=torch.float32)

model = LSTMModel()
criterion = nn.MSELoss()
optimizer = torch.optim.Adam(model.parameters(), lr=0.001)

for epoch in range(args.epochs):
    model.train()
    output = model(X)
    loss = criterion(output, y)

    optimizer.zero_grad()
    loss.backward()
    optimizer.step()

    print(f"Epoch {epoch+1}, Loss: {loss.item():.6f}")

model.eval()
pred = model(X).detach().numpy()
pred = scaler.inverse_transform(pred)

plt.plot(prices, label="Real")
plt.plot(range(args.window, len(pred)+args.window), pred, label="Predicted")
plt.legend()
plt.show()