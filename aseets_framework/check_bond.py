import pandas as pd
from my_package.load_data_from_wind_terminal import load_industry_add, load_cpi, load_ppi, load_bond_10y, load_bond_10y_zz, load_r007
import matplotlib.pyplot as plt
plt.rcParams["font.sans-serif"] = ["SimHei"]
plt.rcParams["font.family"] = "sans-serif"
plt.rcParams['axes.unicode_minus'] = False


def check_bond_assets():
    industry_add = load_industry_add().set_index('date')
    cpi = load_cpi().set_index('date')
    ppi = load_ppi().set_index('date')
    bond_10y = load_bond_10y().set_index('date').rename(columns={'rate': '10年期国债收益率'})
    bond_10y_zz = load_bond_10y_zz().set_index('date').rename(columns={'rate': '10年期国债收益率_中债'})
    r007 = load_r007().set_index('date').rename(columns={'rate': 'R007'})
    #
    info_df = pd.concat([industry_add, cpi, ppi, r007, bond_10y_zz], axis=1).sort_index()
    info_df.fillna(method='ffill', inplace=True)
    info_df.index = pd.to_datetime(info_df.index)
    info_df_m = info_df.resample('M').last()
    info_df_m.dropna(how='any', inplace=True)
    info_df_m['dup_cpi'] = info_df_m['工业增加值'] + info_df_m['CPI'] + info_df_m['R007']
    info_df_m['dup_ppi'] = info_df_m['工业增加值'] + info_df_m['PPI'] + info_df_m['R007']
    #
    fig, ax = plt.subplots()
    ax2 = ax.twinx()
    info_df_m[['dup_cpi', 'dup_ppi']].plot(ax=ax)
    info_df_m['10年期国债收益率_中债'].plot(ax=ax2, color=['yellow'])
    plt.show()
    return info_df_m


if __name__ == '__main__':
    check_bond_assets()
