# plotting/user_base.py
import pandas as pd
import matplotlib.pyplot as plt
from ..core import loader
from .. import config
from ..utils.plotting import save_plot

def plot_kpi_zone(df: pd.DataFrame):
    """生成按战区划分的WNU和Sales图表"""
    df['date'] = pd.to_datetime(df.day, format='%Y%m%d')
    df_recent = df[df['date'].isin(pd.date_range(df['date'].max() - pd.to_timedelta(50, unit="D"), df['date'].max()))].copy()

    # 对user_type进行排名和分组
    rkdk_zone = df_recent.groupby('user_type')['wnu'].sum().reset_index()
    rkdk_zone = rkdk_zone.sort_values(by='wnu', ascending=False).reset_index(drop=True)
    rkdk_zone['row_number'] = rkdk_zone['wnu'].rank(ascending=False, method='first')
    
    df_merged = pd.merge(df_recent, rkdk_zone[['user_type', 'row_number']], how='left', on='user_type')
    df_merged.loc[df_merged["row_number"] >= 9, 'user_type'] = 'OU_其他来源'
    
    df_agg = df_merged.groupby(['day', 'zone', 'zone_type', 'user_type']).agg({'wnu': "sum", 'wsales': "sum"}).reset_index()

    fig = plt.figure(figsize=(14, 8), tight_layout=True)
    gs = fig.add_gridspec(2, 3, width_ratios=[2, 1, 1])
    
    axes_map = {
        'xiaoqi': (gs[0, 0], gs[1, 0]),
        'mix': (gs[0, 1], gs[1, 1]),
        'ios': (gs[0, 2], gs[1, 2]),
    }
    
    zone_titles = {'xiaoqi': '小7专服', 'mix': '安卓混服', 'ios': 'iOS服'}

    for zone_type, (ax_wnu_pos, ax_wsales_pos) in axes_map.items():
        ax_wnu = fig.add_subplot(ax_wnu_pos)
        ax_wsales = fig.add_subplot(ax_wsales_pos, sharex=ax_wnu)
        
        data = df_agg[df_agg['zone_type'] == zone_type]
        
        # 绘制WNU
        pivot_wnu = data.pivot_table(index='zone', columns='user_type', values='wnu', aggfunc='sum').fillna(0)
        pivot_wnu.plot.bar(stacked=True, ax=ax_wnu, color=config.DEFAULT_COLORS, legend=False)
        ax_wnu.set_title(zone_titles[zone_type], loc='left', fontsize=10)
        ax_wnu.set_xlabel('')
        if zone_type == 'xiaoqi':
            ax_wnu.set_ylabel('WNU', fontsize=14)
            ax_wnu.legend(fontsize=7, loc='upper left')

        # 绘制WSALES
        pivot_wsales = data.pivot_table(index='zone', columns='user_type', values='wsales', aggfunc='sum').fillna(0)
        pivot_wsales.plot.bar(stacked=True, ax=ax_wsales, color=config.DEFAULT_COLORS, legend=False)
        ax_wsales.set_xlabel('')
        if zone_type == 'xiaoqi':
            ax_wsales.set_ylabel('Weekly Sales', fontsize=14)

    fig.suptitle('WNU & Weekly Sales by Server Zone', x=0.03, y=.98, ha='left', fontsize=20)
    save_plot(fig, 'user_base_wnu_sales_by_zone.jpg', subdirectory='user_base')

def plot_sales_index(df: pd.DataFrame):
    """生成按档位划分的充值人数图表"""
    df['date'] = pd.to_datetime(df.day, format='%Y%m%d')
    df_recent = df[df['date'].isin(pd.date_range(df['date'].max() - pd.to_timedelta(60, unit="D"), df['date'].max()))].copy()

    fig, ax = plt.subplots(figsize=(14, 7), tight_layout=True)
    
    payment_tiers = {
        '198 or less': ['198_below'],
        '198-647': [198, 328],
        '648-2591': [648, 1296],
        '2592-7775': [2592, 5184],
        '7776 or more': [7776, 11110, 50000]
    }

    for label, indices in payment_tiers.items():
        tier_data = df_recent[df_recent['index'].isin(indices)]
        pu_by_date = tier_data.groupby('date')['pu'].sum().reset_index()
        ax.plot(pu_by_date['date'], pu_by_date['pu'], linewidth=2.5, linestyle='-', label=label)

    ax.set_title('Paying User Count by Payment Tier', loc='left', fontsize=20)
    ax.tick_params(axis='x', rotation=0)
    ax.legend(loc='upper right')
    ax.set_yscale('log', base=2)
    ax.set_xlabel('Date')
    ax.set_ylabel('Number of Paying Users (log scale)')
    
    save_plot(fig, 'user_base_paying_users_by_tier.jpg', subdirectory='user_base')


def generate_all():
    """生成所有用户基础相关的图表"""
    print("\n--- Generating User Base Plots ---")
    
    df_zone = loader.load_sheet('KPI_ZONE', usecols=range(7))
    if df_zone is not None:
        plot_kpi_zone(df_zone)
        
    df_sales_index = loader.load_sheet('SALES_INDEX', usecols=range(4))
    if df_sales_index is not None:
        plot_sales_index(df_sales_index)
