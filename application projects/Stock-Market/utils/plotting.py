import matplotlib.pyplot as plt

def plot_trades(prices, buys, sells, title):
    plt.figure(figsize=(15, 5))
    plt.plot(prices, label="Price")

    plt.plot(buys, [prices[i] for i in buys], "^", label="Buy")
    plt.plot(sells, [prices[i] for i in sells], "v", label="Sell")

    plt.title(title)
    plt.legend()
    plt.show()