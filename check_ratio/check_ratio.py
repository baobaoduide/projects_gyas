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
        stock_data['std_stock'] = stock_data['return_stock'].rolling(243).std()
        bond_data['std_bond'] = bond_data['return_bond'].rolling(window=243).std()
        data = pd.merge(stock_data, bond_data, on=['date'])
        data.dropna(how='any', inplace=True)
        data['date'] = pd.to_datetime(data['date'])
        data.set_index('date', inplace=True)
        data_weekly = data.resample('W')
        #
        data.plot.scatter(x='return_stock', y='return_bond', s=5)
        plt.show()
        data.plot.scatter(x='std_stock', y='std_bond', s=5)
        plt.show()
        data.plot(x='date', y=['return_stock', 'return_bond'], linewidth=0.4)
        plt.grid()
        plt.show()
    return ratio, stock_std, bond_std


if __name__ == '__main__':
    start_date = '2002-01-04'
    end_date = '2022-07-22'
    ratio = check_relation(start_date, end_date)
    start_date_list = ['2017-07-22', '2018-07-22', '2019-07-22', '2020-07-22', '2021-07-22']
    ratio_list = []
    stock_std_list = []
    bond_std_list = []
    for date in start_date_list:
        ratio, stock_std, bond_std = check_relation(date, end_date, isplot=False)
        ratio_list.append(ratio)
        stock_std_list.append(stock_std)
        bond_std_list.append(bond_std)
