import os
import pandas as pd
from load_data import load_position_data, load_fp_cate
path_folder = r'D:\projects\standing_book\data_raw\data_position'


def prepare_all_history_data():
    fp_cate = load_fp_cate()
    #
    read_type = '全部'
    date_poeistion_list = ['2021-12-31', '2022-01-31', '2022-02-28', '2022-03-31', '2022-05-31', '2022-06-30', '2022-07-31', '2022-08-26']
    mmarket_fund_list = []
    sinvest_fund_list = []
    bond_list = []
    deposit_list = []
    item_list = []
    stock_list = []
    equity_invest_list = []
    for date in date_poeistion_list:
        data_position = load_position_data(read_type, date)
        mmarket_fund = data_position['货币市场工具-2']['货币市场基金（RMB）']
        mmarket_fund = mmarket_fund[mmarket_fund.iloc[:, 0] != '合计']
        sinvest_fund = data_position['证券投资基金-3']
        bond = data_position['债券-4']
        deposit = data_position['定期存款-5']
        item = data_position['项目-6']
        stock = data_position['股票-7']
        equity_invest = data_position['股权投资-8']
        print('fine...')
        mmarket_fund_list.append(mmarket_fund)
        sinvest_fund_list.append(sinvest_fund)
        bond_list.append(bond)
        deposit_list.append(deposit)
        item_list.append(item)
        stock_list.append(stock)
        equity_invest_list.append(equity_invest)
    mmarket_fund_df = pd.concat(mmarket_fund_list).drop_duplicates(subset=['证券代码'], keep='last')
    mmarket_fund_df = mmarket_fund_df[['证券代码', '证券名称']]
    mmarket_fund_df['FP分类'] = None
    mmarket_fund_df['类型_一级'] = '货币型基金'
    mmarket_fund_df['类型_二级'] = None
    #
    sinvest_fund_df = pd.concat(sinvest_fund_list).drop_duplicates(subset=['证券代码'], keep='last')
    sinvest_fund_df = pd.merge(sinvest_fund_df[['证券代码', '证券名称', 'FP分类']], fp_cate, on=['FP分类'], how='left')
    fund_df = pd.concat([mmarket_fund_df, sinvest_fund_df], ignore_index=True)
    num_loss1 = fund_df['类型_一级'].isna().sum()
    print('证券投资基金一级类型分类信息缺失数目：', num_loss1)
    #
    bond_df = pd.concat(bond_list).drop_duplicates(subset=['证券代码'], keep='last')
    bond_df = pd.merge(bond_df[['证券代码', '证券名称', 'FP分类', '年利率', '到期收益率', '到期日', '投资类型', '发行机构']], fp_cate, on=['FP分类'], how='left')
    num_loss2 = bond_df['类型_一级'].isna().sum()
    print('债券一级类型分类信息缺失数目：', num_loss2)
    #
    deposit_df = pd.concat(deposit_list).drop_duplicates(subset=['证券代码'], keep='last')
    deposit_df = pd.merge(deposit_df[['证券代码', '名称', 'FP分类']].rename(columns={'名称': '证券名称'}), fp_cate, on=['FP分类'], how='left')
    num_loss3 = deposit_df['类型_一级'].isna().sum()
    print('存款一级类型分类信息缺失数目：', num_loss3)
    #
    item_df = pd.concat(item_list).drop_duplicates(subset=['证券代码'], keep='last')
    item_df = pd.merge(item_df[['证券代码', '名称', 'FP分类', '税前收益率', '税后收益率', '持仓面值', '单位成本', '持仓成本', '应收利息', '全价市值', '减值准备', '剩余期限', '起息日', '下一付息日', '到期日', '发行机构']].rename(columns={'名称': '证券名称', '减值准备': '累计减值'}), fp_cate, on=['FP分类'], how='left')
    num_loss4 = item_df['类型_一级'].isna().sum()
    print('项目一级类型分类信息缺失数目：', num_loss4)
    #
    stock_df = pd.concat(stock_list).drop_duplicates(subset=['证券代码'], keep='last')
    stock_df = stock_df[['证券代码', '证券简称', 'FP分类']].rename(columns={'证券简称': '证券名称'})
    #
    equity_invest_df = pd.concat(equity_invest_list).drop_duplicates(subset=['证券代码'], keep='last')
    equity_invest_df = pd.merge(equity_invest_df[['证券代码', '名称', 'FP分类']].rename(columns={'名称': '证券名称'}), fp_cate, on=['FP分类'], how='left')
    num_loss5 = equity_invest_df['类型_一级'].isna().sum()
    print('非标股权一级类型分类信息缺失数目：', num_loss5)
    num_loss = num_loss1 + num_loss2 + num_loss3 + num_loss4 + num_loss5
    assert num_loss == 0, '出现新FP分类，需要在基础表格中添加相关信息！'
    #
    result_df = {'基金': fund_df, '债券': bond_df, '存款': deposit_df, '非标股权': equity_invest_df, '项目': item_df}
    return result_df


def save_result(result_df):
    path_data = os.path.join(os.path.dirname(__file__), 'data_raw')
    path_dict = os.path.join(path_data, '各资产历史2级类型分类信息.xlsx')
    with pd.ExcelWriter(path_dict) as writer:
        result_df['基金'].to_excel(writer, sheet_name='基金', index=False)
        result_df['债券'].to_excel(writer, sheet_name='债券', index=False)
        result_df['存款'].to_excel(writer, sheet_name='存款', index=False)
        result_df['非标股权'].to_excel(writer, sheet_name='非标股权', index=False)
        result_df['项目'].to_excel(writer, sheet_name='项目', index=False)
    pass


if __name__ == '__main__':
    result = prepare_all_history_data()
    save_result(result)
