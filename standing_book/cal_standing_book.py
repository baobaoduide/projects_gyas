import os
import pandas as pd
from load_data import load_position_data, load_trade_data, load_fp_cate, load_base_info
import warnings
warnings.filterwarnings('ignore')


def prepare_inventory_data(position_data, fp_cate, date_position):
    mmarket_instru = position_data['货币市场工具-2']['货币市场基金（RMB）']
    sinvest_fund = pd.merge(position_data['证券投资基金-3'], fp_cate, on='FP分类', how='left')
    bond = pd.merge(position_data['债券-4'], fp_cate, on='FP分类', how='left')
    fixed_deposit = pd.merge(position_data['定期存款-5'], fp_cate, on='FP分类', how='left')
    item = pd.merge(position_data['项目-6'], fp_cate, on='FP分类', how='left')
    stock = position_data['股票-7']
    equity_invest = pd.merge(position_data['股权投资-8'], fp_cate, on='FP分类', how='left')
    #
    fund_money = sinvest_fund[sinvest_fund['类型_一级'].isin(['货币型基金', '保险资产管理产品-货币型'])]
    fund_bond = sinvest_fund[sinvest_fund['类型_一级'].isin(['债券型基金', '保险资产管理产品-债券型'])]
    fund_equity = sinvest_fund[sinvest_fund['类型_一级'].isin(['股票型基金', '混合型基金', '保险资产管理产品-权益型', '保险资产管理产品-混合型'])]
    #
    mmarket_instru['类型_一级'] = '货币型基金'
    mmarket_instru.rename(columns={'组合': '所属组合', '成本': '持仓成本'}, inplace=True)
    liquidity = pd.concat([fund_money, mmarket_instru], ignore_index=True)
    liquidity['日期'] = date_position
    liquidity['操作'] = '存量'
    liquidity = liquidity[['日期', '操作', '类型_一级', '类型_二级', '证券代码', '证券名称', '单位成本', '持仓数量', '持仓成本', '市价', '市值', '累计估值', '累计减值', '所属组合', '投资类型', '交易市场', '发行公司', '内部分类', '应收红利']]
    #
    fix_bond = bond.copy()
    fix_bond['日期'] = date_position
    fix_bond['操作'] = '存量'
    fix_bond = fix_bond[['日期', '操作',
       '类型_一级', '类型_二级', '证券代码', '证券名称', '年利率', '到期日', '持仓面值', '单位成本', '持仓成本', '到期收益率', '质押券面值', '市值', '市价', '全价市值', '应收利息', '估值增值', '减值准备', '剩余期限', '所属组合', '投资类型',
       '交易市场', '发行日期', '下一付息日', '发行机构', '行业分类', '外部评级', '担保情况']]
    #
    fix_deposit = fixed_deposit.copy()
    fix_deposit['日期'] = date_position
    fix_deposit['操作'] = '存量'
    fix_deposit = fix_deposit[['日期', '操作', '类型_一级', '类型_二级', '证券代码', '名称', '年利率', '持仓面值', '单位成本', '持仓成本', '市值', '应收利息', '全价市值', '减值准备', '剩余期限', '所属组合', '交易市场', '起息日', '下一付息日', '到期日', '发行机构', '担保状态', '行业分类']]
    #
    fix_bond_fund = fund_bond.copy()
    fix_bond_fund['日期'] = date_position
    fix_bond_fund['操作'] = '存量'
    fix_bond_fund = fix_bond_fund[['日期', '操作', '类型_一级', '类型_二级', '证券代码', '证券名称', '单位成本', '持仓数量', '持仓成本', '市价', '市值', '累计估值', '累计减值', '所属组合', '投资类型', '交易市场', '发行公司', '内部分类', 'FP分类']]
    #
    equity_stock = stock.copy()
    equity_stock['日期'] = date_position
    equity_stock['操作'] = '存量'
    equity_stock = equity_stock[['日期', '操作', '证券代码', '证券简称', '证券类别', '市场类别', '投资类型', '数量', '成本', '全价市值', '累计估值', '累计减值', '所属组合', '行业分类']]
    #
    equity_fund = fund_equity.copy()
    equity_fund['日期'] = date_position
    equity_fund['操作'] = '存量'
    equity_fund = equity_fund[['日期', '操作', '类型_一级', '类型_二级', '证券代码', '证券名称', '单位成本', '持仓数量', '持仓成本', '市价', '市值', '累计估值', '累计减值', '所属组合', '投资类型', '交易市场', '发行公司', '内部分类']]
    #
    unlist_equity = equity_invest.copy()
    unlist_equity['日期'] = date_position
    unlist_equity['操作'] = '存量'
    unlist_equity = unlist_equity[['日期', '操作', '类型_一级', '类型_二级', '证券代码', '名称', '税前收益率', '税后收益率', '持仓数量', '单位成本', '持仓成本', '市值', '估值估增', '全价市值', '应收利息', '累计减值', '所属组合', '投资期限', '起息日', '计息截止日', '下一付息日', '退出日', '发行机构']]
    #
    nonstandard_asset = item.copy()
    nonstandard_asset['日期'] = date_position
    nonstandard_asset['操作'] = '存量'
    nonstandard_asset = nonstandard_asset[['日期', '操作', '类型_一级', '类型_二级', '证券代码', '名称', '税前收益率', '税后收益率', '持仓面值', '单位成本', '持仓成本', '市值', '应收利息', '全价市值', '估值增值', '减值准备', '剩余期限', '所属组合', '投资类型', '交易市场', '起息日', '下一付息日', '到期日', '发行机构', '担保状态', '行业分类']]
    #
    result = {'流动性': liquidity, '固定收益类_债券': fix_bond, '固定收益类_存款': fix_deposit, '固定收益类_债基': fix_bond_fund, '上市权益类_股票': equity_stock, '上市权益类_基金': equity_fund, '未上市股权': unlist_equity, '非标资产': nonstandard_asset}
    return result


def add_trade_data(trade_data, assets_dict):
    type_dict = {'存款': ['协议存款存入', '定期存款存入', '协议存款支取', '定期存款支取', '协议存款提前支取'], '债券': ['债券买入', '债券分销', '债券卖出', '债券兑付到账'], '股票': ['股票买入', '新股（上市）', '股票卖出'], '基金': ['保险产品申购确认', '申购基金确认', '封闭式基金买入', '转入基金确认', '保险产品赎回到账', '赎回基金到账', '封闭式基金卖出', '转出基金确认', '新基金（申购）网下'], '项目': ['项目AFS申购缴款', '项目买入缴款', '项目资产转入', '项目AFS卖出到账', '项目资产转出', '项目兑付到帐', '资产证券兑付到账']}
    # '项目兑付到账'
    trade_data_deposit = trade_data[trade_data['业务类型'].isin(type_dict['存款'])]
    trade_data_deposit = pd.merge(trade_data_deposit, assets_dict['存款'][['证券代码', '类型_一级', '类型_二级']], on=['证券代码'], how='left')
    trade_data_deposit = trade_data_deposit[['日期', '业务类型', '类型_一级', '类型_二级', '证券代码', '证券名称', '成交数量', '成交金额', '组合', '市场', '实际清算金额', '结转成本']] # 删去字段：'佣金', '印花税', '经手费', '过户费', '证管费', '其他费用', '债券利息', '回购收益'
    num_loss1 = trade_data_deposit['类型_一级'].isna().sum()
    print('存款，类型等字段数据缺失条数：', num_loss1)
    #
    trade_data_bond = trade_data[trade_data['业务类型'].isin(type_dict['债券'])]
    trade_data_bond = pd.merge(trade_data_bond, assets_dict['债券'][['证券代码', '类型_一级', '类型_二级', '年利率', '到期收益率', '到期日', '投资类型', '发行机构']], on=['证券代码'], how='left')
    trade_data_bond['月份'] = trade_data_bond['日期'].apply(func=lambda x: int(x[5:7]))
    trade_data_bond = trade_data_bond[['日期', '业务类型', '类型_一级', '类型_二级', '证券代码', '证券名称', '成交数量', '成交金额', '月份', '组合', '市场', '经手费', '其他费用', '债券利息', '实际清算金额', '结转成本', '年利率', '到期收益率', '到期日', '投资类型', '发行机构']] # 删去字段：'佣金', '印花税', '过户费', '证管费', '回购收益'
    num_loss2 = trade_data_bond['类型_一级'].isna().sum()
    print('债券，类型等字段数据缺失条数：', num_loss2)
    #
    trade_data_stock = trade_data[trade_data['业务类型'].isin(type_dict['股票'])]
    trade_data_stock = trade_data_stock[['日期', '业务类型', '证券代码', '证券名称', '成交数量', '成交金额', '组合', '市场', '佣金', '印花税', '经手费', '过户费', '证管费', '其他费用', '实际清算金额', '结转成本']] # 删去字段：, '债券利息', '回购收益'
    #
    trade_data_fund = pd.merge(trade_data[trade_data['业务类型'].isin(type_dict['基金'])], assets_dict['基金'][['证券代码', '类型_一级', '类型_二级']], on=['证券代码'], how='left')
    trade_data_fund['月份'] = trade_data_fund['日期'].apply(func=lambda x: int(x[5:7]))
    trade_data_fund = trade_data_fund[['日期', '业务类型', '类型_一级', '类型_二级', '证券代码', '证券名称', '成交数量', '成交金额', '月份', '组合', '市场', '佣金', '经手费', '其他费用', '实际清算金额', '结转成本']] # 删去字段：'印花税', '过户费', '证管费', '债券利息', '回购收益'
    num_loss3 = trade_data_fund['类型_一级'].isna().sum()
    print('基金，类型等字段数据缺失条数：', num_loss3)
    trade_data_fund_money = trade_data_fund[trade_data_fund['类型_一级'].isin(['货币型基金', '保险资产管理产品-货币型'])]
    trade_data_fund_bond = trade_data_fund[trade_data_fund['类型_一级'].isin(['债券型基金', '保险资产管理产品-债券型'])]
    trade_data_fund_stock = trade_data_fund[trade_data_fund['类型_一级'].isin(['股票型基金', '混合型基金', '保险资产管理产品-权益型', '保险资产管理产品-混合型'])]
    trade_data_fund_ = trade_data_fund[trade_data_fund['类型_一级'].isin(['不动产'])]
    trade_data_fund_nan = trade_data_fund[trade_data_fund['类型_一级'].isna()]
    trade_data_fund_stock = pd.concat([trade_data_fund_stock, trade_data_fund_nan], ignore_index=True)
    #
    trade_data_item = pd.merge(trade_data[trade_data['业务类型'].isin(type_dict['项目'])], assets_dict['非标股权'][['证券代码', '类型_一级', '类型_二级']], on=['证券代码'], how='left')
    trade_data_item['月份'] = trade_data_item['日期'].apply(func=lambda x: int(x[5:7]))
    trade_data_item = trade_data_item[['日期', '业务类型', '类型_一级', '类型_二级', '证券代码', '证券名称', '成交数量', '成交金额', '月份', '组合', '市场', '实际清算金额', '结转成本']] # 删去字段：'佣金', '印花税', '经手费', '过户费', '证管费', '其他费用', '债券利息', '回购收益'
    trade_data_item_unlistequity = trade_data_item[trade_data_item['类型_一级'].isin(['未上市股权', '非标股权'])]
    trade_data_item_ = trade_data_item[~trade_data_item['类型_一级'].isin(['未上市股权', '非标股权'])].drop(columns=['类型_一级', '类型_二级'])
    trade_data_item_ = pd.merge(trade_data_item_, assets_dict['项目'].drop(columns=['证券名称', 'FP分类']), on='证券代码', how='left')
    trade_data_item_ = trade_data_item_[['日期', '业务类型', '类型_一级', '类型_二级', '证券代码', '证券名称', '成交数量', '成交金额', '月份', '组合', '市场', '实际清算金额', '结转成本', '税前收益率', '税后收益率', '持仓面值', '单位成本', '持仓成本', '应收利息', '全价市值', '累计减值', '剩余期限', '起息日', '下一付息日', '到期日', '发行机构']]
    trade_data_item_ = pd.concat([trade_data_item_, trade_data_fund_])
    trade_data_item_.sort_values(by=['日期'], inplace=True)
    trade_data_item_.reset_index(drop=True, inplace=True)
    num_loss4 = trade_data_item_['类型_一级'].isna().sum()
    print('项目，类型等字段数据缺失条数：', num_loss4)
    trade_data_result = {'流动性': trade_data_fund_money, '固定收益类_债券': trade_data_bond, '固定收益类_存款': trade_data_deposit, '固定收益类_债基': trade_data_fund_bond, '上市权益类_股票': trade_data_stock, '上市权益类_基金': trade_data_fund_stock, '未上市股权': trade_data_item_unlistequity, '非标资产': trade_data_item_}
    return trade_data_result


def save_data(result_inv, result_trade, date_trade_end, portfolio):
    liquidity = result_inv['流动性']
    fix_bond = result_inv['固定收益类_债券']
    fix_deposit = result_inv['固定收益类_存款']
    fix_bond_fund = result_inv['固定收益类_债基']
    equity_stock = result_inv['上市权益类_股票']
    equity_fund = result_inv['上市权益类_基金']
    unlist_equity = result_inv['未上市股权']
    nonstandard_asset = result_inv['非标资产']
    positions = [len(liquidity), len(fix_bond), len(fix_deposit), len(fix_bond_fund), len(equity_stock),
                 len(equity_fund), len(unlist_equity), len(nonstandard_asset)]
    trade_data_fund_money = result_trade['流动性']
    trade_data_bond = result_trade['固定收益类_债券']
    trade_data_deposit = result_trade['固定收益类_存款']
    trade_data_fund_bond = result_trade['固定收益类_债基']
    trade_data_stock = result_trade['上市权益类_股票']
    trade_data_fund_stock = result_trade['上市权益类_基金']
    trade_data_item_unlistequity = result_trade['未上市股权']
    trade_data_item_ = result_trade['非标资产']
    #
    date_trade_end_num = date_trade_end[:4] + date_trade_end[5:7] + date_trade_end[8:]
    path_save_folder = os.path.join(os.path.dirname(__file__), 'result_'+date_trade_end_num)
    if not os.path.exists(path_save_folder):
        os.mkdir(path_save_folder)
    path_fund_dict = os.path.join(path_save_folder, '工银安盛人寿委内_' + portfolio + '_'+date_trade_end[:4]+'管理报告_'+date_trade_end_num+'.xlsx')
    with pd.ExcelWriter(path_fund_dict) as writer:
        liquidity.to_excel(writer, sheet_name='流动性', index=False)
        trade_data_fund_money.to_excel(writer, sheet_name='流动性', startrow=positions[0] + 4, index=False)
        fix_bond.to_excel(writer, sheet_name='固定收益类_债券', index=False)
        trade_data_bond.to_excel(writer, sheet_name='固定收益类_债券', startrow=positions[1] + 4, index=False)
        fix_deposit.to_excel(writer, sheet_name='固定收益类_存款', index=False)
        trade_data_deposit.to_excel(writer, sheet_name='固定收益类_存款', startrow=positions[2] + 4, index=False)
        fix_bond_fund.to_excel(writer, sheet_name='固定收益类_债基', index=False)
        trade_data_fund_bond.to_excel(writer, sheet_name='固定收益类_债基', startrow=positions[3] + 4, index=False)
        equity_stock.to_excel(writer, sheet_name='上市权益类_股票', index=False)
        trade_data_stock.to_excel(writer, sheet_name='上市权益类_股票', startrow=positions[4] + 4, index=False)
        equity_fund.to_excel(writer, sheet_name='上市权益类_基金', index=False)
        trade_data_fund_stock.to_excel(writer, sheet_name='上市权益类_基金', startrow=positions[5] + 4, index=False)
        unlist_equity.to_excel(writer, sheet_name='未上市股权', index=False)
        trade_data_item_unlistequity.to_excel(writer, sheet_name='未上市股权', startrow=positions[6] + 4, index=False)
        nonstandard_asset.to_excel(writer, sheet_name='非标资产', index=False)
        trade_data_item_.to_excel(writer, sheet_name='非标资产', startrow=positions[7] + 4, index=False)
    pass


def prepare_standing_book(portfolio, date_position, date_trade_end):
    date_trade_start = (pd.to_datetime(date_position) + pd.Timedelta(days=1)).strftime('%Y-%m-%d')
    position_data = load_position_data(portfolio, date_position)
    trade_data = load_trade_data(portfolio, date_trade_start, date_trade_end)
    fp_cate = load_fp_cate()
    assets_dict = load_base_info()
    #
    result_inv = prepare_inventory_data(position_data, fp_cate, date_position)
    result_trade = add_trade_data(trade_data, assets_dict)
    #
    save_data(result_inv, result_trade, date_trade_end, portfolio)
    return result_inv, result_trade


if __name__ == '__main__':
    portfolio_list = ['人民币自有', '传统', '万能', '税延养老', '分红长期', '分红短期']
    date_position = '2021-12-31'
    date_trade_end = '2022-08-26'
    for port in portfolio_list:
        print('\n', port)
        prepare_standing_book(port, date_position, date_trade_end)
    #
    # portfolio = portfolio_list[-1]
    # prepare_standing_book(portfolio, date_position, date_trade_end)
