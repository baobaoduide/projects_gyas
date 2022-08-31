import os
import datetime
import pandas as pd
path_folder = r'D:\database\data_raw\wind_terminal'


def load_tradedays():
    path_data = os.path.join(path_folder, 'trade_days.xlsx')
    rtn = pd.read_excel(path_data, header=None)[0].dt.strftime('%Y-%m-%d')
    return rtn


def load_hs300(start_d='2002-01-04', end_d=datetime.date.today().strftime('%Y-%m-%d')):
    path_data = os.path.join(path_folder, '沪深300指数.xlsx')
    rtn = pd.read_excel(path_data, header=1)
    name_dict = {'日期': 'date', '沪深300': 'close'}
    rtn.rename(columns=name_dict, inplace=True)
    #
    tradedays = load_tradedays()
    rtn = rtn[rtn['date'].isin(tradedays)]
    rtn = rtn[rtn['date'].between(start_d, end_d)]
    rtn.reset_index(drop=True, inplace=True)
    return rtn


def load_bond_index(start_d='2002-01-04', end_d=datetime.date.today().strftime('%Y-%m-%d')):
    path_data = os.path.join(path_folder, '中债-总财富(总值)指数.xlsx')
    rtn = pd.read_excel(path_data, header=1)
    name_dict = {'日期': 'date', '中债-总财富(总值)指数': 'close'}
    rtn.rename(columns=name_dict, inplace=True)
    #
    tradedays = load_tradedays()
    rtn = rtn[rtn['date'].isin(tradedays)]
    rtn = rtn[rtn['date'].between(start_d, end_d)]
    rtn.reset_index(drop=True, inplace=True)
    return rtn


def load_industry_add(start_d='1990-01-31', end_d=datetime.date.today().strftime('%Y-%m-%d')):
    path_data = os.path.join(path_folder, '工业增加值_当月同比.xlsx')
    rtn = pd.read_excel(path_data)
    name_dict = {'指标名称': 'date', '工业增加值:当月同比': '工业增加值'}
    rtn.rename(columns=name_dict, inplace=True)
    #
    rtn['date'] = rtn['date'].dt.strftime('%Y-%m-%d')
    rtn = rtn[rtn['date'].between(start_d, end_d)]
    rtn['工业增加值'] = rtn['工业增加值'] / 100
    return rtn


def load_cpi(start_d='1987-01-31', end_d=datetime.date.today().strftime('%Y-%m-%d')):
    path_data = os.path.join(path_folder, 'CPI_当月同比.xlsx')
    rtn = pd.read_excel(path_data)
    name_dict = {'指标名称': 'date', 'CPI:当月同比': 'CPI'}
    rtn.rename(columns=name_dict, inplace=True)
    #
    rtn['date'] = rtn['date'].dt.strftime('%Y-%m-%d')
    rtn = rtn[rtn['date'].between(start_d, end_d)]
    rtn['CPI'] = rtn['CPI'] / 100
    return rtn


def load_ppi(start_d='1996-10-31', end_d=datetime.date.today().strftime('%Y-%m-%d')):
    path_data = os.path.join(path_folder, 'PPI_全部工业品_当月同比.xlsx')
    rtn = pd.read_excel(path_data)
    name_dict = {'指标名称': 'date', 'PPI:全部工业品:当月同比': 'PPI'}
    rtn.rename(columns=name_dict, inplace=True)
    #
    rtn['date'] = rtn['date'].dt.strftime('%Y-%m-%d')
    rtn = rtn[rtn['date'].between(start_d, end_d)]
    rtn['PPI'] = rtn['PPI'] / 100
    return rtn


def load_bond_10y(start_d='2015-01-04', end_d=datetime.date.today().strftime('%Y-%m-%d')):
    path_data = os.path.join(path_folder, '10年期国债收益率.xlsx')
    rtn = pd.read_excel(path_data)
    name_dict = {'指标名称': 'date', '10年期国债收益率': 'rate'}
    rtn.rename(columns=name_dict, inplace=True)
    #
    rtn['date'] = rtn['date'].dt.strftime('%Y-%m-%d')
    rtn = rtn[rtn['date'].between(start_d, end_d)]
    rtn['rate'] = rtn['rate'] / 100
    return rtn


def load_bond_10y_zz(start_d='2002-01-04', end_d=datetime.date.today().strftime('%Y-%m-%d')):
    path_data = os.path.join(path_folder, '中债国债到期收益率_10年.xlsx')
    rtn = pd.read_excel(path_data)
    name_dict = {'指标名称': 'date', '中债国债到期收益率:10年': 'rate'}
    rtn.rename(columns=name_dict, inplace=True)
    #
    rtn['date'] = rtn['date'].dt.strftime('%Y-%m-%d')
    rtn = rtn[rtn['date'].between(start_d, end_d)]
    rtn['rate'] = rtn['rate'] / 100
    return rtn


def load_bond_corp_5y(start_d='2002-01-04', end_d=datetime.date.today().strftime('%Y-%m-%d')):
    path_data = os.path.join(path_folder, '中债企业债到期收益率(AA+)_5年.xlsx')
    rtn = pd.read_excel(path_data)
    name_dict = {'指标名称': 'date', '中债企业债到期收益率(AA+):5年': 'rate'}
    rtn.rename(columns=name_dict, inplace=True)
    #
    rtn['date'] = rtn['date'].dt.strftime('%Y-%m-%d')
    rtn = rtn[rtn['date'].between(start_d, end_d)]
    rtn['rate'] = rtn['rate'] / 100
    return rtn


def load_r007(start_d='1999-01-04', end_d=datetime.date.today().strftime('%Y-%m-%d')):
    path_data = os.path.join(path_folder, 'R007.xlsx')
    rtn = pd.read_excel(path_data)
    name_dict = {'指标名称': 'date', 'R007': 'rate'}
    rtn.rename(columns=name_dict, inplace=True)
    #
    rtn['date'] = rtn['date'].dt.strftime('%Y-%m-%d')
    rtn['rate'] = rtn['rate'] / 100
    rtn = rtn[rtn['date'].between(start_d, end_d)]
    rtn.reset_index(drop=True, inplace=True)
    return rtn


def load_dr007(start_d='2014-12-15', end_d=datetime.date.today().strftime('%Y-%m-%d')):
    path_data = os.path.join(path_folder, 'DR007.xlsx')
    rtn = pd.read_excel(path_data)
    name_dict = {'指标名称': 'date', 'DR007': 'rate'}
    rtn.rename(columns=name_dict, inplace=True)
    #
    rtn['date'] = rtn['date'].dt.strftime('%Y-%m-%d')
    rtn['rate'] = rtn['rate'] / 100
    rtn = rtn[rtn['date'].between(start_d, end_d)]
    rtn.reset_index(drop=True, inplace=True)
    return rtn


def load_shibor(start_d='2006-10-08', end_d=datetime.date.today().strftime('%Y-%m-%d')):
    path_data = os.path.join(path_folder, 'SHIBOR.xlsx')
    rtn = pd.read_excel(path_data)
    name_dict = {'指标名称': 'date', 'SHIBORO/N': 'SHIBORON'}
    rtn.rename(columns=name_dict, inplace=True)
    #
    rtn['date'] = rtn['date'].dt.strftime('%Y-%m-%d')
    rtn = rtn[rtn['date'].between(start_d, end_d)]
    rtn.set_index('date', inplace=True)
    rtn.columns = [x.lower() for x in rtn.columns]
    rtn = rtn / 100
    rtn.reset_index(inplace=True)
    return rtn


def load_fund_index_wind(start_d='2003-12-31', end_d=datetime.date.today().strftime('%Y-%m-%d')):
    path_data = os.path.join(path_folder, '万得货币市场基金指数.xlsx')
    rtn = pd.read_excel(path_data, header=1)
    name_dict = {'日期': 'date', '万得货币市场基金指数': 'close'}
    rtn.rename(columns=name_dict, inplace=True)
    #
    tradedays = load_tradedays()
    rtn = rtn[rtn['date'].isin(tradedays)]
    rtn = rtn[rtn['date'].between(start_d, end_d)]
    rtn.reset_index(drop=True, inplace=True)
    return rtn


def load_commodity_index(start_d='2004-06-01', end_d=datetime.date.today().strftime('%Y-%m-%d')):
    path_data = os.path.join(path_folder, '南华综合指数.xlsx')
    rtn = pd.read_excel(path_data)
    name_dict = {'指标名称': 'date', '南华综合指数': 'close'}
    rtn.rename(columns=name_dict, inplace=True)
    rtn['date'] = rtn['date'].dt.strftime('%Y-%m-%d')
    rtn = rtn[rtn['date'].between(start_d, end_d)]
    rtn.reset_index(drop=True, inplace=True)
    return rtn


def load_gold(start_d='1968-01-02', end_d=datetime.date.today().strftime('%Y-%m-%d')):
    path_data = os.path.join(path_folder, '伦敦现货黄金_以美元计价.xlsx')
    rtn = pd.read_excel(path_data)
    name_dict = {'指标名称': 'date', '伦敦现货黄金:以美元计价': 'price'}
    rtn.rename(columns=name_dict, inplace=True)
    rtn['date'] = rtn['date'].dt.strftime('%Y-%m-%d')
    rtn = rtn[rtn['date'].between(start_d, end_d)]
    rtn.reset_index(drop=True, inplace=True)
    return rtn


def load_money_fund(start_d='2004-01-07', end_d=datetime.date.today().strftime('%Y-%m-%d')):
    path_data = os.path.join(path_folder, '中证基金指数_货币基金.xlsx')
    rtn = pd.read_excel(path_data)
    name_dict = {'指标名称': 'date', '中证基金指数:货币基金': 'close'}
    rtn.rename(columns=name_dict, inplace=True)
    rtn['date'] = rtn['date'].dt.strftime('%Y-%m-%d')
    rtn = rtn[rtn['date'].between(start_d, end_d)]
    rtn.reset_index(drop=True, inplace=True)
    return rtn


if __name__ == '__main__':
    # load_tradedays()
    start_date = '2004-04-01'
    end_date = '2022-08-29'
    # load_hs300()
    # load_bond_index()
    # load_industry_add()
    # load_cpi()
    # load_ppi()
    # load_bond_10y()
    # load_bond_10y_zz()
    load_bond_corp_5y()
    # load_r007()
    # load_dr007()
    # load_shibor()
    load_fund_index_wind()
    load_commodity_index()
    load_gold()
    load_money_fund()
