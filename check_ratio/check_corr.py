import numpy as np
import pandas as pd
from load_data import load_hs300, load_bond_data
import matplotlib.pyplot as plt


def check_corr(start_date, end_date):
    stock_data = load_hs300(start_date, end_date)
    bond_data = load_bond_data(start_date, end_date)
    #
    stock_data['return_stock'] = stock_data['close'] / stock_data['close'].shift(1) - 1
    data = pd.merge(stock_data, bond_data, on=['date'])
    data.dropna(how='any', inplace=True)
    #
    corr = data['return_stock'].corr(data['return_bond'])
    #
    cov_m = np.cov(data[['close', 'return_stock', 'return_bond']].T)
    data['corr_3y'] = data['return_stock'].rolling(243*3).corr(data['return_bond'])
    #
    data = data[data['date'] >= '2013-01-01']
    data['date'] = pd.to_datetime(data['date'])
    data.plot(x='date', y='corr_3y', linewidth=0.7)
    plt.grid()
    plt.show()
    return data


if __name__ == '__main__':
    start_date = '2002-01-04'
    end_date = '2022-07-22'
    ratio = check_corr(start_date, end_date)
