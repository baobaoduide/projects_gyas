import pandas as pd
from load_data import load_hs300, load_bond_data
import matplotlib.pyplot as plt


def check_relation(start_date, end_date, isplot=True):
    stock_data = load_hs300(start_date, end_date)
    bond_data = load_bond_data(start_date, end_date)
    #
    stock_data['return_stock'] = stock_data['close'] / stock_data['close'].shift(1) - 1
    stock_std = stock_data['return_stock'].std()
    bond_std = bond_data['return_bond'].std()
    ratio = stock_std / bond_std
    #
    if isplot:
        data = pd.merge(stock_data, bond_data, on=['date'])
        data.dropna(how='any', inplace=True)
        data['date'] = pd.to_datetime(data['date'])
        #
        data.plot.scatter(x='close', y='return_bond', s=5)
        plt.show()
        fig, ax1 = plt.subplots()
        ax1.plot(data['date'], data['close'], linewidth=0.7, color='blue', label='hs300')
        ax2 = ax1.twinx()
        ax2.plot(data['date'], data['return_bond'], linewidth=0.7, color='red', label='bond_10y')
        plt.grid()
        plt.show()
    return ratio, stock_std, bond_std


if __name__ == '__main__':
    start_date = '2010-01-04'
    end_date = '2022-07-22'
    ratio = check_relation(start_date, end_date)
