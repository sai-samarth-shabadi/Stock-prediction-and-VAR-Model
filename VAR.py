import numpy as np
import pandas as pd
import yfinance as yf
import datetime
from scipy.stats import norm


def download_data(stock, start, end):
    data = {}
    ticker = yf.Ticker(stock)
    data[stock] = ticker.history(start= start, end = end)['Close']
    return pd.DataFrame(data)

def calculate_VAR(s0, mu, sigma, c):
    return s0 * (mu - sigma*norm.ppf(1-c))

def calculate_VAR_n(s0, mu, sigma, c, n):
    return s0 * (mu * n - sigma * np.sqrt(n) * norm.ppf(1-c))


if __name__ == '__main__':

    start= datetime.datetime(2015, 1 ,1)
    end= datetime.datetime(2025, 1 ,1)
    stock_data = download_data('SBIN.NS', start, end)

    #Calculate the log returns
    stock_data['returns'] = np.log(stock_data['SBIN.NS']/stock_data['SBIN.NS'].shift(1))

    #calculate the mean and std
    mu = np.mean(stock_data['returns'])
    sigma = np.std(stock_data['returns'])

    #Confidence level
    c = 0.99
    #initial position
    s0 = 100000
    print('The Value at Risk :%.2f' %calculate_VAR_n(s0, mu, sigma, c, 1))

