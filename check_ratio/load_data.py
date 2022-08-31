import os
import pandas as pd
from datetime import datetime
data_folder = os.path.join(os.path.dirname(__file__), 'data')


def load_hs300(start_date='2002-01-04', end_date='today'):
    path_data = os.path.join(data_folder, '沪深300指数_公式.xlsx')
    rtn = pd.read_excel(path_data, header=3)
    name_dict = {'Date': 'date', 'close': 'close'}
    rtn.rename(columns=name_dict, inplace=True)
    #
    if end_date == 'today':
        end_date = datetime.today().strftime('%Y-%m-%d')
    rtn = rtn[rtn['date'].between(start_date, end_date)]
    rtn['date'] = pd.to_datetime(rtn['date']).dt.strftime('%Y-%m-%d')
    rtn.sort_values(by='date', inplace=True)
    rtn.reset_index(drop=True, inplace=True)
    return rtn


def load_bond_index2(start_date='2002-01-04', end_date='today'):
    path_data = os.path.join(data_folder, '中债-国债总财富(7-10年)指数.xlsx')
    rtn = pd.read_excel(path_data, header=3)
    name_dict = {'Date': 'date', 'close': 'close', 'pct_chg': 'ret_bond'}
    rtn.rename(columns=name_dict, inplace=True)
    rtn['ret_bond'] = rtn['ret_bond'] / 100
    #
    if end_date == 'today':
        end_date = datetime.today().strftime('%Y-%m-%d')
    rtn = rtn[rtn['date'].between(start_date, end_date)]
    rtn['date'] = pd.to_datetime(rtn['date']).dt.strftime('%Y-%m-%d')
    rtn.sort_values(by='date', inplace=True)
    rtn.reset_index(drop=True, inplace=True)
    return rtn


def load_riskfree_rate(start_date='2002-01-04', end_date='today'):
    path_data = os.path.join(data_folder, '银行间质押式回购利率7天.xlsx')
    rtn = pd.read_excel(path_data, header=3)
    name_dict = {'Date': 'date', 'M0041653': 'rate'}
    rtn.rename(columns=name_dict, inplace=True)
    #
    if end_date == 'today':
        end_date = datetime.today().strftime('%Y-%m-%d')
    rtn = rtn[rtn['date'].between(start_date, end_date)]
    rtn['date'] = pd.to_datetime(rtn['date']).dt.strftime('%Y-%m-%d')
    rtn.sort_values(by='date', inplace=True)
    rtn.reset_index(drop=True, inplace=True)
    return rtn


def load_bond_data(start_date, end_date):
    path_data = os.path.join(data_folder, '中债国债到期收益率(中债)(日).xlsx')
    rtn = pd.read_excel(path_data, header=1)
    name_dict = {'频率': 'date', '日': 'return_bond'}
    rtn.rename(columns=name_dict, inplace=True)
    rtn = rtn[rtn['date'].between(start_date, end_date)]
    rtn['date'] = rtn['date'].dt.strftime('%Y-%m-%d')
    rtn['return_bond'] = rtn['return_bond'] / 100
    rtn.reset_index(drop=True, inplace=True)
    return rtn


def load_tradedays():
    path_data = os.path.join(data_folder, 'tradedays.xlsx')
    rtn = pd.read_excel(path_data, header=None)[0]
    rtn = rtn.dt.strftime('%Y-%m-%d')
    return rtn


def load_bond_index(start_date='2002-01-04', end_date='today'):
    path_data = os.path.join(data_folder, '中债总财富指数.xlsx')
    rtn = pd.read_excel(path_data, header=1)
    name_dict = {'日期': 'date', '中债-总财富(总值)指数': 'close'}
    rtn.rename(columns=name_dict, inplace=True)
    #
    if end_date == 'today':
        end_date = datetime.today().strftime('%Y-%m-%d')
    rtn = rtn[rtn['date'].between(start_date, end_date)]
    rtn['date'] = pd.to_datetime(rtn['date']).dt.strftime('%Y-%m-%d')
    rtn.sort_values(by='date', inplace=True)
    rtn.reset_index(drop=True, inplace=True)
    return rtn


def load_crb_commidity(start_date='2002-01-04', end_date='today'):
    path_data = os.path.join(data_folder, 'CRB综合现货.xlsx')
    rtn = pd.read_excel(path_data, header=1)
    name_dict = {'日期': 'date', 'CRB综合现货': 'close'}
    rtn.rename(columns=name_dict, inplace=True)
    #
    if end_date == 'today':
        end_date = datetime.today().strftime('%Y-%m-%d')
    rtn = rtn[rtn['date'].between(start_date, end_date)]
    rtn['date'] = pd.to_datetime(rtn['date']).dt.strftime('%Y-%m-%d')
    rtn.sort_values(by='date', inplace=True)
    rtn.reset_index(drop=True, inplace=True)
    return rtn


def load_szindex(start_date='2002-01-04', end_date='today'):
    path_data = os.path.join(data_folder, '上证指数.xlsx')
    rtn = pd.read_excel(path_data, header=1)
    name_dict = {'日期': 'date', '上证指数': 'close'}
    rtn.rename(columns=name_dict, inplace=True)
    #
    if end_date == 'today':
        end_date = datetime.today().strftime('%Y-%m-%d')
    rtn = rtn[rtn['date'].between(start_date, end_date)]
    rtn['date'] = pd.to_datetime(rtn['date']).dt.strftime('%Y-%m-%d')
    rtn.sort_values(by='date', inplace=True)
    rtn.reset_index(drop=True, inplace=True)
    return rtn


if __name__ == '__main__':
    load_riskfree_rate()
    load_bond_index2()
    load_hs300()
    load_szindex()
