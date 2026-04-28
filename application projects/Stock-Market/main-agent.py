import argparse
from data.data_loader import load_stock_data
from agents.trading_agent import Model, Agent
import matplotlib.pyplot as plt

parser = argparse.ArgumentParser()
parser.add_argument("--symbol", required=True)
parser.add_argument("--period", default="6mo")
parser.add_argument("--epochs", type=int, default=10)
parser.add_argument("--initial", type=float, default=1000)
parser.add_argument("--skip", type=int, default=5)

args = parser.parse_args()

prices = load_stock_data(args.symbol, args.period).tolist()

model = Model(30, 50, 3)
agent = Agent(model, 30, prices, args.skip, args.initial)

agent.fit(args.epochs)
buys, sells, profit = agent.trade()

plt.plot(prices)
plt.plot(buys, [prices[i] for i in buys], "^")
plt.plot(sells, [prices[i] for i in sells], "v")
plt.title(f"{args.symbol} Profit: {profit:.2f}")
plt.show()