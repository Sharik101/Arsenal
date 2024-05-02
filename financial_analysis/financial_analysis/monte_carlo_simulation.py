import numpy as np
import matplotlib.pyplot as plt

def monte_carlo_option_pricing(S0, r, sigma, T, K, option_type, num_simulations=10000):
    num_steps = int(T * 252)
    dt = T / num_steps
    sigma /= 100
    stock_prices = np.zeros((num_steps + 1, num_simulations))
    stock_prices[0] = S0
    for t in range(1, num_steps + 1):
        Z = np.random.standard_normal(num_simulations)
        stock_prices[t] = stock_prices[t - 1] * np.exp((r - 0.5 * sigma**2) * dt + sigma * np.sqrt(dt) * Z)
    if option_type.lower() == 'c':
        payoffs = np.maximum(stock_prices[-1] - K, 0)
    else:
        payoffs = np.maximum(K - stock_prices[-1], 0)
    option_price = np.exp(-r * T) * np.mean(payoffs)
    return option_price, stock_prices

def plot_stock_paths(stock_prices):
    plt.figure(figsize=(10, 5))
    for i in range(min(10, stock_prices.shape[1])):
        plt.plot(stock_prices[:, i], lw=1)
    plt.title('Sample Stock Price Paths')
    plt.xlabel('Time Steps')
    plt.ylabel('Stock Price')
    plt.grid(True)
    plt.show()
