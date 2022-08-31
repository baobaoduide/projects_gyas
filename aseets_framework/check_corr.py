import pandas as pd
from my_package.load_data_from_wind_terminal import load_hs300, load_bond_index, load_r007, load_commodity_index, load_gold, load_money_fund


def check_corr(start_date, end_date):
    stock = load_hs300(start_d=start_date, end_d=end_date).set_index('date')
    stock['股票'] = stock['close'] / stock['close'].shift(1) - 1
    bond = load_bond_index(start_d=start_date, end_d=end_date).set_index('date')
    bond['债券'] = bond['close'] / bond['close'].shift(1) - 1
    r007 = load_r007(start_d=start_date, end_d=end_date).set_index('date').rename(columns={'rate': 'R007'})
    commodity = load_commodity_index(start_d=start_date, end_d=end_date).set_index('date')
    commodity['大宗商品'] = commodity['close'] / commodity['close'].shift(1) - 1
    gold = load_gold(start_d=start_date, end_d=end_date).set_index('date')
    gold['黄金'] = gold['price'] / gold['price'].shift(1) - 1
    m_fund = load_money_fund(start_d=start_date, end_d=end_date).set_index('date')
    m_fund['货币基金'] = m_fund['close'] / m_fund['close'].shift(1) - 1
    #
    all_assets = pd.concat([stock['股票'], bond['债券'], r007['R007'], commodity['大宗商品'], gold['黄金'], m_fund['货币基金']], axis=1)
    all_assets.sort_index(inplace=True)
    all_assets.dropna(how='any', inplace=True)
    #
    corr_df = all_assets.corr()
    return corr_df


if __name__ == '__main__':
    corr_20170430 = check_corr('2004-06-01', '2017-04-30')
    corr_20220829 = check_corr('2004-06-01', '2022-08-29')
