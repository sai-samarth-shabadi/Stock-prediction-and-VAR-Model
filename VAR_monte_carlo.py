import numpy as np
import yfinance as yf
import pandas as pd
import datetime

def download_data(stock, start, end):
    data = {}
    ticker = yf.Ticker(stock)
    data[stock] = ticker.history(start= start, end = end)['Close']
    return pd.DataFrame(data)

class VAR_monte_carlo:

    def __init__(self, S, mu, sigma, c, n, iterations):
        self.S = S
        self.mu = mu
        self.sigma = sigma
        self.n =n
        self.c = c
        self.iterations = iterations


    def simulations(self):
        rand = np.random.normal(0, 1, [1, self.iterations])
        return self.S*np.exp((self.mu - 0.5*self.sigma**2)*self.n + self.sigma* np.sqrt(self.n) * rand)

    def calculate_VAR(self):
        prices = self.simulations()

        #Sort the simulated prices
        np.sort(prices)

        #Calculating the percentile
        percentile = np.percentile(prices, (1-self.c) * 100)

        return self.S - percentile



if __name__ == '__main__':

    start = datetime.datetime(2015, 1, 1)
    end = datetime.datetime(2025, 1, 1)
    stock_data = download_data('SBIN.NS', start, end)

    #calculate the log returns
    # stock_data['returns'] = np.log(stock_data['SBIN.NS']/ stock_data['SBIN.NS'].shift(1))
    stock_data['returns'] = stock_data['SBIN.NS'].pct_change()

    #calculate mean and std
    mu = np.mean(stock_data['returns'])
    sigma = np.std(stock_data['returns'])

    #confidence level
    c = 0.99

    model = VAR_monte_carlo(100000, mu, sigma, c, 1, 10000)
    print('The Value at Risk :%.2f' %model.calculate_VAR())