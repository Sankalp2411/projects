import numpy as np

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

            print(f"Epoch {epoch+1}/{epochs} | Reward: {self.reward_fn(self.weights):.2f}")