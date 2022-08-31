import os
import pandas as pd
path_folder = r'D:\projects\standing_book\data_raw'


def load_position_data(portfolio, date):
    date_num = date[:4] + date[5:7] + date[8:]
    date_char = date[:4] + '年' + date[5:7] + '月' + date[8:] + '日'
    #
    folder_position = os.path.join(path_folder, 'data_position')
    path_data = os.path.join(folder_position, 'data_position_'+date_num+'.xlsx')
    xls = pd.ExcelFile(path_data)
    fasset_impairment = pd.read_excel(xls, '金融资产减值-1', header=2)
    #
    mmarket_instru = pd.read_excel(xls, '货币市场工具-2', header=None)
    split_keyindex = mmarket_instru[0].apply(func=lambda x: x[-11:] == date_char if isinstance(x, str) else False)
    key_titles = mmarket_instru[0][split_keyindex]
    key_titles = key_titles.apply(func=lambda x: x[:-11].replace(' ', '').replace('(', '（').replace(')', '）'))
    result_list = []
    for i in range(len(key_titles)):
        if i == 0:
            ind_start = key_titles.index[i]+1
        else:
            ind_start = key_titles.index[i]+2
        if i == len(key_titles)-1:
            ind_end = len(mmarket_instru)
        else:
            ind_end = key_titles.index[i+1]-1
        result = mmarket_instru.iloc[ind_start: ind_end]
        result.reset_index(drop=True, inplace=True)
        result.columns = result.iloc[0]
        result.drop(index=0, inplace=True)
        result.reset_index(drop=True, inplace=True)
        result.dropna(axis=1, how='all', inplace=True)
        #
        if i == 0:
            result.set_index(result.iloc[:, 0].name, inplace=True)
            col_names = result.columns.to_list()
            if portfolio != '全部':
                use_cols = [x for x in col_names if portfolio in x]
                result = result[use_cols]
        elif i < len(key_titles)-1:
            if len(result) > 0:
                if portfolio != '全部':
                    result = result[result['组合'].apply(func=lambda x: portfolio in x if isinstance(x, str) else False)]
                result.reset_index(drop=True, inplace=True)
        result_list.append(result)
    mmarket_instru_dict = dict(zip(key_titles, result_list))
    #
    sinvest_fund = pd.read_excel(xls, '证券投资基金-3')
    sinvest_fund['FP分类'] = sinvest_fund['证券代码'].apply(func=lambda x: x[6:] if x[:5] == 'TOTAL' else None)
    sinvest_fund['FP分类'].fillna(method='bfill', inplace=True)
    sinvest_fund.dropna(subset=['证券名称'], inplace=True)
    #
    bond = pd.read_excel(xls, '债券-4', dtype={'证券代码': str})
    bond['FP分类'] = bond['证券名称'].apply(func=lambda x: x[6:] if x[:5] == 'TOTAL' else None)
    bond['FP分类'].fillna(method='bfill', inplace=True)
    bond.dropna(subset=['证券代码'], inplace=True)
    #
    fixed_deposit = pd.read_excel(xls, '定期存款-5')
    fixed_deposit['FP分类'] = fixed_deposit['名称'].apply(func=lambda x: x[6:] if x[:5] == 'TOTAL' else None)
    fixed_deposit['FP分类'].fillna(method='bfill', inplace=True)
    fixed_deposit.dropna(subset=['证券代码'], inplace=True)
    #
    item = pd.read_excel(xls, '项目-6')
    item['FP分类'] = item['名称'].apply(func=lambda x: x[6:] if x[:5] == 'TOTAL' else None)
    item['FP分类'].fillna(method='bfill', inplace=True)
    item.dropna(subset=['证券代码'], inplace=True)
    #
    stock = pd.read_excel(xls, '股票-7')
    stock['FP分类'] = stock['证券代码'].apply(func=lambda x: x[6:] if x[:5] == 'TOTAL' else None)
    stock['FP分类'].fillna(method='bfill', inplace=True)
    stock.dropna(subset=['证券简称'], inplace=True)
    #
    equity_invest = pd.read_excel(xls, '股权投资-8')
    equity_invest['FP分类'] = equity_invest['名称'].apply(func=lambda x: x[6:] if x[:5] == 'TOTAL' else None)
    equity_invest['FP分类'].fillna(method='bfill', inplace=True)
    equity_invest.dropna(subset=['证券代码'], inplace=True)
    #
    fore_currency = pd.read_excel(xls, '外币-9')
    fore_currency['FP分类'] = fore_currency['证券名称'].apply(func=lambda x: x[6:] if x[:5] == 'TOTAL' else None)
    fore_currency['FP分类'].fillna(method='bfill', inplace=True)
    fore_currency.dropna(subset=['证券代码'], inplace=True)
    #
    derivatives = pd.read_excel(xls, '衍生品-10')
    derivatives['FP分类'] = derivatives['证券名称'].apply(func=lambda x: x[6:] if x[:5] == 'TOTAL' else None)
    derivatives['FP分类'].fillna(method='bfill', inplace=True)
    derivatives.dropna(subset=['证券代码'], inplace=True)
    #
    if portfolio != '全部':
        sinvest_fund = sinvest_fund[sinvest_fund['所属组合'].apply(func=lambda x: portfolio in x)]
        bond = bond[bond['所属组合'].apply(func=lambda x: portfolio in x)]
        fixed_deposit = fixed_deposit[fixed_deposit['所属组合'].apply(func=lambda x: portfolio in x)]
        item = item[item['所属组合'].apply(func=lambda x: portfolio in x)]
        stock = stock[stock['所属组合'].apply(func=lambda x: portfolio in x)]
        equity_invest = equity_invest[equity_invest['所属组合'].apply(func=lambda x: portfolio in x)]
        derivatives = derivatives[derivatives['所属组合'].apply(func=lambda x: portfolio in x)]
    #
    rtn = {'金融资产减值-1': fasset_impairment, '货币市场工具-2': mmarket_instru_dict, '证券投资基金-3': sinvest_fund, '债券-4': bond, '定期存款-5': fixed_deposit, '项目-6': item, '股票-7': stock, '股权投资-8': equity_invest, '外币-9': fore_currency, '衍生品-10': derivatives}
    return rtn


def load_trade_data(portfolio, date_trade_start, date_trade_end):
    date_trade_start_num = date_trade_start[:4] + date_trade_start[5:7] + date_trade_start[8:]
    date_trade_end_num = date_trade_end[:4] + date_trade_end[5:7] + date_trade_end[8:]
    folder_position = os.path.join(path_folder, 'data_trade')
    path_data = os.path.join(folder_position, 'data_trade_'+date_trade_start_num+'to'+date_trade_end_num+'.xlsx')
    rtn = pd.read_excel(path_data, header=2, dtype={'日期': str})
    rtn['日期'] = rtn['日期'].apply(func=lambda x: x[:4]+'-'+x[4:6]+'-'+x[6:])
    rtn = rtn[rtn['组合'].apply(func=lambda x: portfolio in x)]
    rtn.reset_index(drop=True, inplace=True)
    return rtn


def load_fp_cate():
    path_data = os.path.join(path_folder, 'dict_fp_cate.xlsx')
    rtn = pd.read_excel(path_data)
    return rtn


def load_base_info():
    path_data = os.path.join(path_folder, '各资产历史2级类型分类信息.xlsx')
    xls = pd.ExcelFile(path_data)
    rtn_fund = pd.read_excel(xls, '基金', dtype={'证券代码': str})
    rtn_bond = pd.read_excel(xls, '债券', dtype={'证券代码': str})
    rtn_deposit = pd.read_excel(xls, '存款', dtype={'证券代码': str})
    rtn_equity_unlist = pd.read_excel(xls, '非标股权', dtype={'证券代码': str})
    rtn_item = pd.read_excel(xls, '项目', dtype={'证券代码': str})
    rtn = {'基金': rtn_fund, '债券': rtn_bond, '存款': rtn_deposit, '非标股权': rtn_equity_unlist, '项目': rtn_item}
    return rtn


if __name__ == '__main__':
    load_base_info()
    # load_dict_all_2l_types()
    # load_dict_asset()
    # load_fp_cate()
    #
    date_position = '2021-12-31'
    date_trade_start = '2022-01-01'
    date_trade_end = '2022-08-10'
    portfolio = '分红短期'
    load_position_data(portfolio, date_position)
    load_trade_data(portfolio, date_trade_start, date_trade_end)
