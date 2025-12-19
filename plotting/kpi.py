# plotting/kpi.py
import pandas as pd
import matplotlib.pyplot as plt
import data_loader
import config
import processors
from plot_utils import save_plot, plot_stacked_bar

def plot_kpi_weekly(df: pd.DataFrame):
    """生成周KPI概览图表"""
    df['week'] = pd.to_datetime(df.week, format='%Y%m%d')
    df_sorted = df.sort_values(by='weekid', ascending=True).iloc[:15]

    fig, ax = plt.subplots(2, 1, figsize=(14, 7), sharex=True, tight_layout=True)
    
    # WAU/WNU/WOU图
    ax[0].bar(df_sorted['md'], df_sorted['wou'], width=0.5, label='wou')
    ax[0].bar(df_sorted['md'], df_sorted['wnu'], width=0.5, bottom=df_sorted['wou'], label='wnu')
    ax[0].plot(df_sorted['md'], df_sorted['wau'], linewidth=3.5, c='#2ca02c', label='wau')
    ax[0].set_ylabel('WAU', fontsize=14, fontstyle='italic')
    ax[0].set_ylim(10000, 35000)
    ax[0].legend()
    for x, y in zip(df_sorted['md'], df_sorted['wau']):
        ax[0].text(x, y + 100, f'{y}', ha='center', va='bottom', fontsize=10)

    # 收入图
    revenue = df_sorted['sales'] // 10000
    ax[1].plot(df_sorted['md'], revenue, linewidth=3.0)
    ax[1].set_ylabel('Weekly Revenue (10k units)', fontsize=14, fontstyle='italic')
    ax[1].xaxis.set_major_locator(plt.MultipleLocator(2))
    for x, y in zip(df_sorted['md'], revenue):
        ax[1].text(x, y + 0.5, f'{y}W', ha='center', va='bottom', fontsize=10)

    fig.suptitle('Weekly KPI Summary', x=0.02, y=.98, ha='left', fontsize=20)
    save_plot(fig, 'kpi_weekly_overview.jpg', subdirectory='kpi')

def plot_kpi_daily(df: pd.DataFrame):
    """生成日KPI图表 (DAU/Revenue and ARPU/ARPPU/PR)"""
    df['day'] = pd.to_datetime(df.day, format='%Y%m%d')
    df_sorted = df.sort_values(by='day', ascending=True).iloc[:31]

    # DAU & Revenue图
    fig1, ax1 = plt.subplots(2, 1, figsize=(14, 7), sharex=True, tight_layout=True)
    ax1[0].bar(df_sorted['day'], df_sorted['dou'], width=0.5, label='dou')
    ax1[0].bar(df_sorted['day'], df_sorted['dnu'], width=0.5, bottom=df_sorted['dou'], label='dnu')
    ax1[0].plot(df_sorted['day'], df_sorted['dau'], linewidth=3.0, label='dau')
    ax1[0].set_ylabel('DAU', fontsize=14)
    ax1[0].set_ylim(5000, 25000)
    ax1[0].legend()
    fig1.suptitle('Daily KPI Summary', x=0.03, y=.98, ha='left', fontsize=20)
    
    revenue = df_sorted['sales'] // 10000
    ax1[1].plot(df_sorted['day'], revenue, linewidth=3.0)
    ax1[1].set_ylabel('Daily Revenue (10k units)', fontsize=14)
    save_plot(fig1, 'kpi_daily_dau_revenue.jpg', subdirectory='kpi')

    # ARPU, ARPPU, PR图
    fig2, ax2 = plt.subplots(3, 1, figsize=(14, 7), sharex=True, tight_layout=True)
    ax2[0].plot(df_sorted['day'], df_sorted['arpu'], label='arpu', linewidth=3.0)
    ax2[1].plot(df_sorted['day'], df_sorted['arppu'], label='arppu', linewidth=3.0)
    ax2[2].plot(df_sorted['day'], df_sorted['payrate'], label='payrate', linewidth=3.0)
    ax2[0].set_ylabel('ARPU')
    ax2[1].set_ylabel('ARPPU')
    ax2[2].set_ylabel('Pay Rate')
    fig2.suptitle('Daily ARPU, ARPPU & Pay Rate', x=0.03, y=.98, ha='left', fontsize=20)
    save_plot(fig2, 'kpi_daily_arpu_pr.jpg', subdirectory='kpi')

def plot_kpi_channel(df: pd.DataFrame):
    """生成渠道来源的WAU和WNU图表"""
    df_processed = processors.process_kpi_channel_data(df)
    
    fig, ax = plt.subplots(1, 2, figsize=(14, 7), sharex=True, tight_layout=True)
    
    plot_stacked_bar(df_processed, ax[0], x_col='md', y_col='wau', category_col='affcode', title='WAU by Source', ylabel='WAU')
    ax[0].legend(loc='upper left', fontsize=8)

    plot_stacked_bar(df_processed, ax[1], x_col='md', y_col='wnu', category_col='affcode', title='WNU by Source', ylabel='WNU')
    ax[1].get_legend().remove() # 移除第二个图的图例以避免重复

    fig.suptitle('Weekly User Acquisition by Source', x=0.03, y=.98, ha='left', fontsize=20)
    save_plot(fig, 'kpi_channel_source.jpg', subdirectory='kpi')

def plot_kpi_user(df: pd.DataFrame):
    """按注册日期生成WAU和Sales图表"""
    df['week'] = pd.to_datetime(df.week, format='%Y%m%d')
    df_recent = df[df['weekid'] > (df['weekid'].max() - 15)]
    df_agg = df_recent.groupby(['weekid', 'md', 'regmonth2']).agg({'wau': "sum", 'wsales': "sum"}).reset_index()

    fig, ax = plt.subplots(2, 1, figsize=(14, 10), tight_layout=True)
    
    plot_stacked_bar(df_agg, ax[0], x_col='md', y_col='wau', category_col='regmonth2', title='WAU by Registration Cohort', ylabel='WAU')
    ax[0].xaxis.set_major_locator(plt.MultipleLocator(2))
    
    plot_stacked_bar(df_agg, ax[1], x_col='md', y_col='wsales', category_col='regmonth2', title='Weekly Sales by Registration Cohort', ylabel='Weekly Sales')
    ax[1].xaxis.set_major_locator(plt.MultipleLocator(2))

    fig.suptitle('User KPIs by Registration Cohort', x=0.03, y=.99, ha='left', fontsize=20)
    save_plot(fig, 'kpi_user_cohort.jpg', subdirectory='kpi')

def generate_all():
    """生成所有KPI相关的图表"""
    print("\n--- Generating KPI Plots ---")
    
    # 周KPI
    df_wkly = data_loader.load_sheet('KPI_WKLY')
    if df_wkly is not None:
        plot_kpi_weekly(df_wkly)
        
    # 日KPI
    df_daily = data_loader.load_sheet('KPI_DAILY')
    if df_daily is not None:
        plot_kpi_daily(df_daily)
        
    # 渠道KPI
    df_channel = data_loader.load_sheet('KPI_CHANNEL')
    if df_channel is not None:
        plot_kpi_channel(df_channel)
        
    # 用户KPI
    df_user = data_loader.load_sheet('KPI_USER')
    if df_user is not None:
        plot_kpi_user(df_user)
