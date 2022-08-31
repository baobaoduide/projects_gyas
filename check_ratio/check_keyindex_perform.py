import pandas as pd
from datetime import datetime
from dateutil import relativedelta
from load_data import load_hs300, load_bond_index, load_crb_commidity, load_szindex


def check_key_ind(close_data):
    date_list = pd.to_datetime(close_data['date'], '%Y-%m-%d')
    start_date = date_list.iloc[0]
    end_date = date_list.iloc[-1]
    result_df = relativedelta(end_date, start_date)
    return result_df


def check_result():
    hs300 = load_hs300()
    bond_index = load_bond_index()
    crb_commodity = load_crb_commidity()
    szindex = load_szindex()
    #
    check_key_ind(hs300)
    return


if __name__ == '__main__':
    check_result()
