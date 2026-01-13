# plotting/activities.py
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from ..core import loader
from .. import config
from ..core import processors
from ..utils.plotting import save_plot

# ----------------------------------
# Reusable Activity Plotting Functions
# ----------------------------------

def _plot_activity_overview(df: pd.DataFrame, activity_name: str, date_col='date'):
    """通用函数: 绘制活动概览图 (总消耗 vs 参与率)"""
    
    # 动态构建聚合字典
    agg_dict = {'freediamond': 'sum', 'paiddiamond': 'sum', 'au': 'sum', 'pu': 'sum'}
    if 'backdiamond' in df.columns:
        agg_dict['backdiamond'] = 'sum'

    df_agg = df[df['row_number'] <= 30].groupby(date_col).agg(agg_dict).reset_index()
    
    # 仅当 backdiamond 存在时才进行计算
    if 'backdiamond' in df_agg.columns:
        df_agg['freediamond'] += df_agg['backdiamond']
    
    if 'pu' in df_agg.columns and 'au' in df_agg.columns and df_agg['au'].sum() > 0:
        df_agg['pr'] = (df_agg['pu'] / df_agg['au']).fillna(0)
    else:
        df_agg['pr'] = 0

    fig, ax1 = plt.subplots(figsize=(14, 7), tight_layout=True)
    
    # 耗钻柱状图
    ax1.bar(df_agg[date_col], df_agg['freediamond'], width=3, label='Free Diamond')
    ax1.bar(df_agg[date_col], df_agg['paiddiamond'], width=3, bottom=df_agg['freediamond'], label='Paid Diamond')
    ax1.set_ylabel('Diamond Spend')
    ax1.legend(loc='upper left')

    # 参与率双轴
    ax2 = ax1.twinx()
    ax2.plot(df_agg[date_col], df_agg['pr'], linewidth=3.0, color='#2ca02c', label='Participation Rate')
    ax2.set_ylabel('Participation Rate')
    ax2.grid(False)
    ax2.legend(loc='upper right')

    fig.suptitle(f'Overview of {activity_name}', x=0.03, y=.98, ha='left', fontsize=20)
    save_plot(fig, f'activity_{activity_name.lower()}_overview.jpg', subdirectory='activities')


def _plot_activity_cohort_analysis(df: pd.DataFrame, activity_name: str):
    """通用函数: 按zonetype和viptype绘制活动的群组分析图"""
    
    # 动态构建聚合字典
    agg_dict = {'freediamond': 'sum', 'paiddiamond': 'sum', 'au': 'sum', 'pu': 'sum'}
    if 'backdiamond' in df.columns:
        agg_dict['backdiamond'] = 'sum'
    if 'sales' in df.columns:
        agg_dict['sales'] = 'sum'

    df_agg = df[df['row_number'] <= 5].groupby(['row_number', 'day', 'zonetype', 'viptype_code']) \
        .agg(agg_dict).reset_index()

    # 根据可用数据动态构建要绘制的指标
    metrics = {}
    if 'sales' in df_agg.columns:
        metrics['sales'] = 'Sales (CNY)'
    
    if all(k in df_agg for k in ['pu', 'au']) and df_agg['au'].sum() > 0:
        df_agg['pr'] = (df_agg['pu'] / df_agg['au']).fillna(0)
        metrics['pr'] = 'Participation Rate'

    if all(k in df_agg for k in ['freediamond', 'paiddiamond', 'pu']) and df_agg['pu'].sum() > 0:
        if 'backdiamond' in df_agg.columns:
            df_agg['total_diamond'] = df_agg['freediamond'] + df_agg['paiddiamond'] + df_agg['backdiamond']
        else:
            df_agg['total_diamond'] = df_agg['freediamond'] + df_agg['paiddiamond']
        df_agg['avgdiamond'] = (df_agg['total_diamond'] / df_agg['pu']).fillna(0)
        metrics['avgdiamond'] = 'Avg. Diamond Spend per User'

    if not metrics:
        print(f"No metrics to plot for {activity_name} cohort analysis.")
        return
    
    for metric, title in metrics.items():
        fig, axes = plt.subplots(1, 5, figsize=(14, 7), sharey=True, tight_layout=True)
        dim_date = df_agg['day'].unique()

        for i, zonetype in enumerate(config.ZONE_TYPE_ORDER):
            ax = axes[i]
            zone_data = df_agg[df_agg['zonetype'] == zonetype]
            for j, day in enumerate(dim_date):
                day_data = zone_data[zone_data['day'] == day].sort_values('viptype_code')
                ax.plot(day_data['viptype_code'], day_data[metric], linewidth=2.0, linestyle='-', label=pd.to_datetime(day).strftime('%Y-%m-%d'))
            
            ax.set_xticks(range(len(config.VIP_TYPE_LABELS)))
            ax.set_xticklabels(config.VIP_TYPE_LABELS, rotation=45, ha='right')
            ax.xaxis.set_major_locator(plt.MultipleLocator(1))
            ax.set_title(zonetype, loc='left', fontsize=10)

        axes[4].legend(fontsize=8, loc='upper right')
        fig.suptitle(f'{title} in Recent {activity_name}', x=0.03, y=.98, ha='left', fontsize=20)
        save_plot(fig, f'activity_{activity_name.lower()}_cohort_{metric}.jpg', subdirectory='activities')


# ----------------------------------
# Specific Activity Plotting Functions
# ----------------------------------

def plot_prizewheel(df: pd.DataFrame):
    """为转盘活动生成所有图表"""
    activity_name = "Prizewheel"
    df_processed = processors.process_activity_data(df)
    
    _plot_activity_overview(df_processed, activity_name)
    _plot_activity_cohort_analysis(df_processed, activity_name)

def plot_forcecard(df: pd.DataFrame):
    """为原力活动生成所有图表"""
    activity_name = "Forcecard"
    df_processed = processors.process_activity_data(df)
    
    _plot_activity_overview(df_processed, activity_name)
    _plot_activity_cohort_analysis(df_processed, activity_name)

def plot_soulstonebox(df: pd.DataFrame):
    """为魂匣活动生成所有图表"""
    activity_name = "SoulstoneBox"
    
    # 总览和群组分析
    df_total = df[df['card_id'] == 'total'].copy()
    df_processed = processors.process_activity_data(df_total)
    _plot_activity_overview(df_processed, activity_name)
    _plot_activity_cohort_analysis(df_processed, activity_name)

    # 卡片特定分析
    df_cards = df[df['card_id'] != 'total'].copy()
    df_cards_processed = processors.process_activity_data(df_cards)
    df_latest = df_cards_processed[df_cards_processed['row_number'] == 1].groupby(['date', 'card_name', 'zonetype', 'viptype_code']) \
        .agg({'au': 'sum', 'pu': 'sum', 'freediamond':'sum', 'paiddiamond':'sum'}).reset_index()
    
    if 'pu' in df_latest.columns and df_latest['pu'].sum() > 0:
        df_latest['avgdiamond'] = ((df_latest['freediamond'] + df_latest['paiddiamond']) / df_latest['pu']).fillna(0)
    else:
        df_latest['avgdiamond'] = 0

    fig, axes = plt.subplots(5, 5, figsize=(16, 12), sharey='row', sharex=True, tight_layout=True)
    
    for i, zonetype in enumerate(config.ZONE_TYPE_ORDER):
        for j, viptype in enumerate(range(len(config.VIP_TYPE_LABELS)-1)): # Exclude '非R'
            ax = axes[i, j]
            data = df_latest[(df_latest['zonetype'] == zonetype) & (df_latest['viptype_code'] == viptype)]
            
            ax.bar(data['card_name'], data['avgdiamond'], label='Avg. Diamond Spend per User')
            ax.tick_params(axis='x', labelsize=8, rotation=90)
            
            if j == 0: ax.set_ylabel(zonetype, fontsize=10)
            if i == 0: ax.set_title(config.VIP_TYPE_LABELS[j], loc='center', fontsize=10)
            
            ax2 = ax.twinx()
            ax2.plot(data['card_name'], data['pu'], linewidth=2.0, linestyle='-', color='#ff7f0e', label='Participant Count')
            if not df_latest.empty and 'pu' in df_latest.columns:
                ax2.set_ylim(0, df_latest['pu'].max() * 1.1)
            ax2.grid(False)

    fig.suptitle(f'Latest {activity_name}: Spend per User & Participant Count by Card', x=0.03, y=.98, ha='left', fontsize=20)
    save_plot(fig, f'activity_{activity_name.lower()}_card_analysis.jpg', subdirectory='activities')


def plot_themegacha(df: pd.DataFrame):
    """为主题召唤生成所有图表"""
    activity_name = "ThemeGacha"
    df_processed = processors.process_activity_data(df)
    
    _plot_activity_overview(df_processed, activity_name)
    _plot_activity_cohort_analysis(df_processed, activity_name)

def plot_wishpool(df: pd.DataFrame):
    """为许愿池生成所有图表"""
    activity_name = "Wishpool"
    df_processed = processors.process_activity_data(df)
    
    # 总体收入概览
    df_recent = df_processed[df_processed['row_number'] <= 15]
    if 'sales' in df_recent.columns:
        df_agg = df_recent.groupby(['date', 'viptype_code']).agg({'sales': "sum"}).reset_index()
        fig, ax = plt.subplots(figsize=(14, 7), tight_layout=True)
        pivot_df = df_agg.pivot_table(index='date', columns='viptype_code', values='sales').fillna(0)
        pivot_df.plot.bar(stacked=True, ax=ax, color=config.DEFAULT_COLORS, width=0.8)
        ax.set_title(f'Revenue Overview of {activity_name}', loc='left', fontsize=16)
        ax.set_xticklabels([d.strftime('%Y-%m-%d') for d in pivot_df.index], rotation=45)
        save_plot(fig, f'activity_{activity_name.lower()}_revenue_overview.jpg', subdirectory='activities')

    # Heatmap 分析
    df_heat = df_processed[df_processed['row_number'] <= 6].groupby(['date', 'viptype_code']) \
        .agg(au=('au', 'sum'), cu=('cu', 'sum'), sales=('sales', 'sum')).reset_index()
    
    if 'sales' in df_heat.columns:
        df_heat['arpu'] = (df_heat['sales'] / df_heat['au']).fillna(0)
        df_heat['arppu'] = (df_heat['sales'] / df_heat['cu']).fillna(0)
    if 'cu' in df_heat.columns and 'au' in df_heat.columns:
        df_heat['payrate'] = (df_heat['cu'] / df_heat['au']).fillna(0)

    fig, axes = plt.subplots(2, 2, figsize=(14, 10), tight_layout=True)
    
    metrics = {}
    if 'cu' in df_heat.columns: metrics['cu'] = 'Paying User Count'
    if 'arppu' in df_heat.columns: metrics['arppu'] = 'ARPPU'
    if 'arpu' in df_heat.columns: metrics['arpu'] = 'ARPU'
    if 'payrate' in df_heat.columns: metrics['payrate'] = 'Pay Rate'
    
    cmap = plt.cm.get_cmap('RdYlBu_r')

    for ax, (metric, title) in zip(axes.flatten(), metrics.items()):
        pivot_df = df_heat.pivot_table(index='date', columns='viptype_code', values=metric).fillna(0)
        sns.heatmap(pivot_df, ax=ax, annot=True, fmt='.2f' if metric in ['payrate', 'arpu'] else 'g', cmap=cmap)
        ax.set_title(title, loc='left')
        ax.set_yticklabels([d.strftime('%Y-%m-%d') for d in pivot_df.index], rotation=0)
        ax.set_xticklabels(config.VIP_TYPE_LABELS, rotation=45, ha='right')

    fig.suptitle(f'Heatmap Analysis of Recent {activity_name}', x=0.03, y=.98, ha='left', fontsize=20)
    save_plot(fig, f'activity_{activity_name.lower()}_heatmap.jpg', subdirectory='activities')


def generate_all():
    """生成所有活动相关的图表"""
    print("\n--- Generating Activity Plots ---")

    activities_map = {
        'Prizewheel': ('ACT_PRIZEWHEEL', plot_prizewheel),
        'Forcecard': ('ACT_INTERZONE_FORCECARD', plot_forcecard),
        'SoulstoneBox': ('ACT_SOULSTONEBOX', plot_soulstonebox),
        'ThemeGacha': ('ACT_THEMEGACHA', plot_themegacha),
        'Wishpool': ('ACT_WISHPOOL', plot_wishpool),
    }

    for name, (sheet, plot_func) in activities_map.items():
        print(f"\n-- Plotting for {name} --")
        df = loader.load_sheet(sheet)
        if df is not None:
            plot_func(df)
