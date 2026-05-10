import numpy as np
from data.data_loader import load_stock_data


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


class EvolutionStrategy:
    def __init__(self, weights, reward_fn, pop_size, sigma, lr):
        self.weights = weights
        self.reward_fn = reward_fn
        self.pop_size = pop_size
        self.sigma = sigma
        self.lr = lr

    def train(self, epochs):
        for _ in range(epochs):
            population = []
            rewards = np.zeros(self.pop_size)

            for _ in range(self.pop_size):
                noise = [np.random.randn(*w.shape) for w in self.weights]
                population.append(noise)

            for i in range(self.pop_size):
                trial = [w + self.sigma*n for w,n in zip(self.weights, population[i])]
                rewards[i] = self.reward_fn(trial)

            rewards = (rewards - rewards.mean()) / (rewards.std() + 1e-8)

            for i, w in enumerate(self.weights):
                A = np.array([p[i] for p in population])
                self.weights[i] += (self.lr/(self.pop_size*self.sigma)) * np.dot(A.T, rewards).T


class Agent:
    def __init__(self, model, window, prices, skip, initial, sims):
        self.model = model
        self.window = window
        self.prices = prices
        self.skip = skip
        self.initial = initial

        self.es = EvolutionStrategy(
            model.get_weights(),
            self.reward,
            sims,
            0.1,
            0.03
        )

    def state(self, t):
        w = self.window + 1
        start = t - w + 1
        block = self.prices[start:t+1] if start>=0 else [self.prices[0]]*(-start)+self.prices[:t+1]
        return (np.array(block[1:]) - np.array(block[:-1])).reshape(1,-1)

    def act(self, s):
        return np.argmax(self.model.predict(s)[0])

    def reward(self, weights):
        self.model.set_weights(weights)
        money = self.initial
        inv = []
        s = self.state(0)

        for t in range(0, len(self.prices)-1, self.skip):
            a = self.act(s)
            p = self.prices[t]

            if a==1 and money>=p:
                inv.append(p)
                money -= p
            elif a==2 and inv:
                inv.pop(0)
                money += p

            s = self.state(t+1)

        return (money - self.initial)/self.initial * 100

    def train(self, epochs):
        self.es.train(epochs)

    def trade(self):
        money = self.initial
        inventory = []

        buys = []
        sells = []

        state = self.state(0)

        for t in range(0, len(self.prices)-1, self.skip):
            action = self.act(state)
            price = self.prices[t]

            if action == 1 and money >= price:
                inventory.append(price)
                money -= price
                buys.append(t)

            elif action == 2 and inventory:
                inventory.pop(0)
                money += price
                sells.append(t)

            state = self.state(t+1)

        return buys, sells, money - self.initial


def run_agent(symbol, period, epochs, initial, skip, sims):
    prices = load_stock_data(symbol, period).tolist()

    model = Model(30, 50, 3)
    agent = Agent(model, 30, prices, skip, initial, sims)

    agent.train(epochs)
    buys, sells, profit = agent.trade()

    return {
        "prices": prices,
        "buys": buys,
        "sells": sells,
        "profit": profit
    }