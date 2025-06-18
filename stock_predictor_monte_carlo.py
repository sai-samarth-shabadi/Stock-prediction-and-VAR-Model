import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

num_of_random_walks = 1000

def stock_monte_carlo(s0, mu, sigma, N= 252):
    data = []

    #generate stock random walks
    for _ in range(num_of_random_walks):
        prices = [s0]

        for _ in range(N):
            #generate sttock prices on daily basis where t = 1
            stock_price = prices[-1]*np.exp((mu - (0.5*sigma*sigma)) + sigma*np.random.normal())
            prices.append(stock_price)

        data.append(prices)

    simulated_paths = pd.DataFrame(data)
    simulated_paths = simulated_paths.T
    simulated_paths['mean'] = simulated_paths.mean(axis=1)
    print('The predicted Future price of the stock after a year: %.2f' % simulated_paths['mean'].tail(1))

def plot_simulations(data):
    plt.plot(data)
    plt.show()

if __name__ == '__main__':

    stock_monte_carlo(50, 0.0002, 0.01)