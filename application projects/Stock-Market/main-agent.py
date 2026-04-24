import argparse
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import yfinance as yf
sns.set()
parser = argparse.ArgumentParser(description="Stock Trading Agent (Evolution Strategy)")
parser.add_argument("--symbol", type=str, required=True)
parser.add_argument("--period", type=str, default="6mo")
parser.add_argument("--epochs", type=int, default=10)
parser.add_argument("--initial", type=float, default=1000.0)
parser.add_argument("--skip", type=int, default=5)
args = parser.parse_args()
df = yf.download(args.symbol, period=args.period, progress=False)
if df.empty or "Close" not in df.columns:
    raise RuntimeError("Failed to download stock data")
prices = np.asarray(df["Close"].values, dtype=np.float64).reshape(-1).tolist()
class DeepEvolutionStrategy:
    def __init__(self, weights, reward_fn, pop_size, sigma, lr):
        self.weights = weights
        self.reward_fn = reward_fn
        self.pop_size = pop_size
        self.sigma = sigma
        self.lr = lr
    def train(self, epochs):
        for epoch in range(epochs):
            population = []
            rewards = np.zeros(self.pop_size)
            for _ in range(self.pop_size):
                noise = [np.random.randn(*w.shape) for w in self.weights]
                population.append(noise)
            for i in range(self.pop_size):
                trial_weights = [
                    w + self.sigma * n for w, n in zip(self.weights, population[i])
                ]
                rewards[i] = self.reward_fn(trial_weights)
            rewards = (rewards - rewards.mean()) / (rewards.std() + 1e-8)
            for i, w in enumerate(self.weights):
                noise_stack = np.array([p[i] for p in population])
                self.weights[i] += (
                    self.lr / (self.pop_size * self.sigma)
                    * np.dot(noise_stack.T, rewards).T
                )
            print(
                f"Epoch {epoch + 1}/{epochs} | Reward: {self.reward_fn(self.weights):.2f}"
            )
class Model:
    def __init__(self, input_size, hidden_size, output_size):
        self.weights = [
            np.random.randn(input_size, hidden_size),
            np.random.randn(hidden_size, output_size),
            np.zeros((1, hidden_size)),
        ]
    def predict(self, x):
        hidden = np.dot(x, self.weights[0]) + self.weights[2]
        return np.dot(hidden, self.weights[1])
    def get_weights(self):
        return self.weights
    def set_weights(self, weights):
        self.weights = weights
class Agent:
    POP_SIZE = 15
    SIGMA = 0.1
    LR = 0.03
    def __init__(self, model, window_size, prices, skip, initial_money):
        self.model = model
        self.window_size = window_size
        self.prices = prices
        self.skip = skip
        self.initial_money = float(initial_money)
        self.es = DeepEvolutionStrategy(
            self.model.get_weights(),
            self.get_reward,
            self.POP_SIZE,
            self.SIGMA,
            self.LR,
        )
    def get_state(self, t):
        window = self.window_size + 1
        start = t - window + 1
        if start >= 0:
            block = self.prices[start : t + 1]
        else:
            block = [self.prices[0]] * (-start) + self.prices[: t + 1]
        block = np.asarray(block, dtype=np.float64)
        state = block[1:] - block[:-1]
        return state.reshape(1, -1)
    def act(self, state):
        return int(np.argmax(self.model.predict(state)[0]))
    def get_reward(self, weights):
        self.model.set_weights(weights)
        money = float(self.initial_money)
        inventory = []
        state = self.get_state(0)
        for t in range(0, len(self.prices) - 1, self.skip):
            action = self.act(state)
            price = float(self.prices[t])
            if action == 1 and money >= price:
                inventory.append(price)
                money -= price
            elif action == 2 and inventory:
                inventory.pop(0)
                money += price
            state = self.get_state(t + 1)
        return ((money - self.initial_money) / self.initial_money) * 100.0
    def fit(self, epochs):
        self.es.train(epochs)
    def trade(self):
        money = float(self.initial_money)
        inventory = []
        buys, sells = [], []
        state = self.get_state(0)
        for t in range(0, len(self.prices) - 1, self.skip):
            action = self.act(state)
            price = float(self.prices[t])
            if action == 1 and money >= price:
                inventory.append(price)
                money -= price
                buys.append(t)
            elif action == 2 and inventory:
                inventory.pop(0)
                money += price
                sells.append(t)
            state = self.get_state(t + 1)
        return buys, sells, money - self.initial_money
WINDOW = 30
model = Model(WINDOW, 50, 3)
agent = Agent(model, WINDOW, prices, args.skip, args.initial)
agent.fit(args.epochs)
buys, sells, profit = agent.trade()
plt.figure(figsize=(15, 5))
plt.plot(prices, label="Price")
plt.plot(buys, [prices[i] for i in buys], "^", markersize=8, label="Buy")
plt.plot(sells, [prices[i] for i in sells], "v", markersize=8, label="Sell")
plt.title(f"{args.symbol} | Profit: {profit:.2f}")
plt.legend()
plt.show()