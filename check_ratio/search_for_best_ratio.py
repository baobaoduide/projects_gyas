import os
import numpy as np
import pandas as pd
from load_data import load_hs300, load_bond_index2, load_riskfree_rate
folder_result = os.path.join(os.path.dirname(__file__), 'result')


def check_range_result(start_date, end_date, ratio):
    hs300_data = load_hs300(start_date=start_date, end_date=end_date)
    bond_data = load_bond_index2(start_date=start_date, end_date=end_date)
    riskfree_data = load_riskfree_rate(start_date=start_date, end_date=end_date)
    #
    riskfree_data = riskfree_data[riskfree_data['date'] > start_date]
    rate_free = riskfree_data['rate'].mean() / 100
    hs300_data['ret_stock'] = hs300_data['close'] / hs300_data['close'].shift(1) - 1
    hs300_data['ret_stock'].fillna(0, inplace=True)
    hs300_data['nv_stock'] = (hs300_data['ret_stock'] + 1).cumprod()
    bond_data['ret_bond'][0] = 0
    bond_data['nv_bond'] = (bond_data['ret_bond'] + 1).cumprod()
    #
    num_stock = 1
    num_bond = num_stock * ratio
    part_stock = num_stock / (num_stock + num_bond)
    part_bond = num_bond / (num_stock + num_bond)
    nv_stock = [part_stock]
    nv_bond = [part_bond]
    nv_port = [1]
    ret_port = [0]
    drawd_port = [0]
    draw_stock = [0]
    draw_bond = [0]
    for i in range(1, len(bond_data)):
        date_i = hs300_data['date'][i]
        date_i_last = hs300_data['date'][i-1]
        if date_i[5:7] == date_i_last[5:7]:
            nv_stock_i = (hs300_data['ret_stock'][i] + 1) * nv_stock[-1]
            nv_bond_i = (bond_data['ret_bond'][i] + 1) * nv_bond[-1]
        else:
            nv_stock_i = nv_port[-1] * part_stock * (hs300_data['ret_stock'][i] + 1)
            nv_bond_i = nv_port[-1] * part_bond * (bond_data['ret_bond'][i] + 1)
        nv_port_i = nv_stock_i + nv_bond_i
        ret_port_i = nv_port_i / nv_port[-1] - 1
        drawdown_port_i = 1 - nv_port_i / max(nv_port)
        draw_stock_i = 1 - hs300_data['nv_stock'][i]/hs300_data['nv_stock'][:i+1].max()
        draw_bond_i = 1 - bond_data['nv_bond'][i]/bond_data['nv_bond'][:i+1].max()
        #
        nv_stock.append(nv_stock_i)
        nv_bond.append(nv_bond_i)
        nv_port.append(nv_port_i)
        ret_port.append(ret_port_i)
        drawd_port.append(drawdown_port_i)
        draw_stock.append(draw_stock_i)
        draw_bond.append(draw_bond_i)
    info_df = pd.DataFrame({'date': hs300_data['date'], 'nv_port': nv_port, 'nv_stock': nv_stock, 'nv_bond': nv_bond, 'ret_port': ret_port, 'drawb_port': drawd_port, 'draw_stock': draw_stock, 'draw_bond': draw_bond})
    #
    ret_df = pd.DataFrame({'ret_port': ret_port, 'ret_stock': hs300_data['ret_stock'], 'ret_bond': bond_data['ret_bond']}).dropna()
    nv_df = pd.DataFrame({'nv_port': nv_port, 'nv_stock': hs300_data['nv_stock'], 'nv_bond': bond_data['nv_bond']}).dropna()
    drawb_df = pd.DataFrame({'drawb_port': drawd_port, 'draw_stock': draw_stock, 'draw_bond': draw_bond}).dropna()
    ret_annual = ((nv_df.iloc[-1]/nv_df.iloc[0]) ** (252/(len(nv_df)-1)) - 1).to_numpy()
    vol_annual = (ret_df.iloc[1:].std() * np.sqrt(252)).to_numpy()
    max_drawb = drawb_df.iloc[1:].max().to_numpy()
    sharp_ratio = (ret_annual - rate_free) / vol_annual
    ret_drawb_ratio = ret_annual / max_drawb
    result_df = pd.DataFrame({'年化收益率': ret_annual, '年化波动率': vol_annual, '最大回撤': max_drawb, '夏普比率': sharp_ratio, '收益回撤比': ret_drawb_ratio}, index=['组合', '沪深300', '7-10年国债']).T
    return result_df


def cal_key_ratios_yoy(ratio):
    years = list(range(2004, 2023))
    start_date = str(years[0]) + '-12-31'
    end_date = str(years[-1]) + '-12-31'
    result_df = check_range_result(start_date, end_date, ratio)
    path_result0 = os.path.join(folder_result, 'result_2_组合加股债.xlsx')
    result_df.to_excel(path_result0)
    #
    result_port_year = []
    for i in range(len(years)-1):
        start_date = str(years[i]) + '-12-31'
        end_date = str(years[i+1]) + '-12-31'
        result_i = check_range_result(start_date, end_date, ratio)
        result_port_i = result_i['组合']
        result_port_year.append(result_port_i)
    result_port_year_df = pd.concat(result_port_year, axis=1).T
    result_port_year_df['年份'] = years[1:]
    result_port_year_df.set_index('年份', inplace=True)
    all_hist = result_df['组合'].rename('合计')
    result_port_year_df = result_port_year_df.append(all_hist)
    path_result = os.path.join(folder_result, 'result_'+str(int(ratio))+'.xlsx')
    result_port_year_df.to_excel(path_result)
    return result_port_year_df


if __name__ == '__main__':
    ratio = 2/1
    result = cal_key_ratios_yoy(ratio)
    #
    ratios = [2, 3, 4, 5, 6]
    ratio_results = []
    for ratio in ratios:
        result_i = cal_key_ratios_yoy(ratio)
        ratio_results.append(result_i)
    ratio_results_df = pd.concat(ratio_results)
    path_result = os.path.join(folder_result, 'result_all.xlsx')
    ratio_results_df.to_excel(path_result)
