import os
import pandas as pd


def load_ashare_industry_data():
    data_path = os.path.join(os.path.dirname(__file__), 'astock_industry.xlsx')
    rtn = pd.read_excel(data_path)
    name_dict = {'证券代码': 'code', '证券简称': 'name', '所属申万行业名称(2021)\n[交易日期] 最新收盘日\n[行业级别] 一级行业': 'sw_l1', '所属申万行业名称(2021)\n[交易日期] 最新收盘日\n[行业级别] 二级行业': 'sw_l2', '所属申万行业名称(2021)\n[交易日期] 最新收盘日\n[行业级别] 三级行业': 'sw_l3', '所属申万行业名称(2021)\n[交易日期] 最新收盘日\n[行业级别] 全部明细': 'sw_detail', '所属中信行业名称\n[交易日期] 最新收盘日\n[行业级别] 一级行业': 'ci_l1', '所属中信行业名称\n[交易日期] 最新收盘日\n[行业级别] 二级行业': 'ci_l2', '所属中信行业名称\n[交易日期] 最新收盘日\n[行业级别] 三级行业': 'ci_l3', '所属中信行业名称\n[交易日期] 最新收盘日\n[行业级别] 全部明细': 'ci_detail'}
    rtn.rename(columns=name_dict, inplace=True)
    return rtn


def check_stock_list():
    indu_data = load_ashare_industry_data()
    indu_data_sw = indu_data.iloc[:, :5]
    indu_data_sw.sort_values(by=['sw_l1', 'sw_l2', 'sw_l3'], inplace=True)
    sw_l1 = indu_data_sw['sw_l1'].drop_duplicates()
    sw_l2 = indu_data_sw['sw_l2'].drop_duplicates()
    sw_l3 = indu_data_sw['sw_l3'].drop_duplicates()
    #
    aim_stock = indu_data_sw[indu_data_sw['sw_l2'] == '半导体']
    aim_stock.sort_values
    aim_stock.reset_index(drop=True, inplace=True)
    return indu_data_sw


check_stock_list()
