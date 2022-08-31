import os
import pandas as pd
from my_package.load_data_from_wind_terminal import load_r007, load_dr007, load_shibor, load_fund_index_wind
path_save_folder = os.path.join(os.path.dirname(__file__), 'data_temp')


def check_money_asset(start_date, end_date):
    frequency = 'W'
    frequency = 'M'
    r007 = load_r007(start_d=start_date, end_d=end_date).set_index('date').rename(columns={'rate': 'R007'})
    r007.index = pd.to_datetime(r007.index)
    r007_w = r007.resample(frequency).last()
    dr007 = load_dr007(start_d=start_date, end_d=end_date).set_index('date').rename(columns={'rate': 'DR007'})
    dr007.index = pd.to_datetime(dr007.index)
    dr007_w = dr007.resample(frequency).last()
    shibor = load_shibor(start_d=start_date, end_d=end_date).set_index('date')
    shibor.index = pd.to_datetime(shibor.index)
    shibor_w = shibor.resample(frequency).last()
    #
    m_rate_007 = pd.concat([r007_w, dr007_w, shibor_w['shibor1w']], axis=1).sort_index().rename(columns={0: 'shibor1w'})
    r007_w.plot(linewidth=1)
    m_rate_007.plot(linewidth=1)
    shibor_w.plot(linewidth=1)
    #
    fund_index_wind = load_fund_index_wind(start_d=start_date, end_d=end_date).set_index('date')
    fund_index_wind.index = pd.to_datetime(fund_index_wind.index)
    fund_index_wind_w = fund_index_wind.resample(frequency).last()
    fund_index_wind_w.dropna(inplace=True)
    index_ret = (fund_index_wind_w / fund_index_wind_w.shift(1) - 1) * 12
    # rate_fund_df = pd.concat([r007_w, dr007_w, shibor_w['shibor1w'], index_ret], axis=1).sort_index().rename(columns={'close': 'ret_mfund'})
    rate_fund_df = pd.merge(r007_w, index_ret, left_index=True, right_index=True)
    rate_fund_df.dropna(how='any', inplace=True)
    path_data = os.path.join(path_save_folder, '货币市场利率与货币基金收益关系（月）.xlsx')
    rate_fund_df.to_excel(path_data)
    rate_fund_df.plot(linewidth=1)
    pass


if __name__ == '__main__':
    check_money_asset('2004-06-01', '2022-08-29')
