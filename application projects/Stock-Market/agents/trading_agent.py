import numpy as np
from models.evolution_model import DeepEvolutionStrategy

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
            block = self.prices[start:t + 1]
        else:
            block = [self.prices[0]] * (-start) + self.prices[:t + 1]

        block = np.asarray(block)
        state = block[1:] - block[:-1]

        return state.reshape(1, -1)

    def act(self, state):
        return int(np.argmax(self.model.predict(state)[0]))

    def get_reward(self, weights):
        self.model.set_weights(weights)

        money = self.initial_money
        inventory = []
        state = self.get_state(0)

        for t in range(0, len(self.prices) - 1, self.skip):
            action = self.act(state)
            price = self.prices[t]

            if action == 1 and money >= price:
                inventory.append(price)
                money -= price

            elif action == 2 and inventory:
                inventory.pop(0)
                money += price

            state = self.get_state(t + 1)

        return ((money - self.initial_money) / self.initial_money) * 100

    def fit(self, epochs):
        self.es.train(epochs)

    def trade(self):
        money = self.initial_money
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