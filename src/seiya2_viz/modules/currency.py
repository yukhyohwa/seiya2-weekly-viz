# plotting/currency.py
import pandas as pd
import matplotlib.pyplot as plt
from ..core import loader
from .. import config
from ..core import processors
from ..utils.plotting import save_plot, plot_stacked_bar

def plot_cur_spend(df: pd.DataFrame):
    """生成钻石消耗图表"""
    df_processed = processors.process_cur_spend_data(df)
    
    fig, ax = plt.subplots(2, 1, figsize=(14, 10), tight_layout=True)

    # 总钻石消耗
    plot_stacked_bar(
        df=df_processed, ax=ax[0], x_col='day', y_col='totaldiamond', 
        category_col='a_typ', title='Total Diamond Spend by Activity', 
        ylabel='Net Diamond Spend', legend_loc='upper left'
    )
    ax[0].xaxis.set_major_locator(plt.MultipleLocator(7))
    ax[0].tick_params(axis='x', rotation=0)

    # 付费钻石消耗
    plot_stacked_bar(
        df=df_processed, ax=ax[1], x_col='day', y_col='paiddiamond', 
        category_col='a_typ', title='Paid Diamond Spend by Activity', 
        ylabel='Paid Diamond Spend', legend_loc='upper left'
    )
    ax[1].xaxis.set_major_locator(plt.MultipleLocator(7))
    ax[1].tick_params(axis='x', rotation=0)

    fig.suptitle('Diamond Spend Analysis', x=0.03, y=.99, ha='left', fontsize=20)
    save_plot(fig, 'currency_spend.jpg', subdirectory='currency')

def plot_cur_stock(df: pd.DataFrame):
    """生成按VIP等级划分的钻石持有量图表"""
    df['day'] = pd.to_datetime(df.day, format='%Y%m%d')
    df_recent = df.sort_values(by='day', ascending=True).iloc[-60:]

    fig = plt.figure(figsize=(14, 8), tight_layout=True)
    gs = fig.add_gridspec(3, 1) # 创建一个3行1列的网格

    # 高VIP
    ax0 = fig.add_subplot(gs[0, 0])
    vip_high = ['v18', 'v17', 'v16', 'v15']
    for v in vip_high:
        ax0.plot(df_recent['day'], df_recent[v], label=v, linewidth=2.5)
    ax0.set_ylabel('High VIP (v15-v18)')
    ax0.legend(loc='upper left')
    ax0.set_ylim(bottom=80000)

    # 中VIP
    ax1 = fig.add_subplot(gs[1, 0], sharex=ax0)
    vip_mid = ['v12', 'v11', 'v10', 'v09']
    for v in vip_mid:
        ax1.plot(df_recent['day'], df_recent[v], label=v, linewidth=2.5)
    ax1.set_ylabel('Mid VIP (v9-v12)')
    ax1.legend(loc='upper left')
    ax1.set_ylim(20000, 50000)

    # 低VIP
    ax2 = fig.add_subplot(gs[2, 0], sharex=ax0)
    vip_low = ['v08', 'v07', 'v06', 'v05']
    for v in vip_low:
        ax2.plot(df_recent['day'], df_recent[v], label=v, linewidth=2.5)
    ax2.set_ylabel('Low VIP (v5-v8)')
    ax2.legend(loc='upper left')
    ax2.set_ylim(0, 20000)
    
    # 隐藏共享x轴的刻度标签
    plt.setp(ax0.get_xticklabels(), visible=False)
    plt.setp(ax1.get_xticklabels(), visible=False)
    
    fig.suptitle('Diamond Holdings by VIP Level', x=0.03, y=.98, ha='left', fontsize=20)
    save_plot(fig, 'currency_stock_by_vip.jpg', subdirectory='currency')

def generate_all():
    """生成所有货币相关的图表"""
    print("\n--- Generating Currency Plots ---")
    
    # 货币消耗 (移除usecols限制，以确保'backdiamond'列被加载)
    df_spend = loader.load_sheet('CUR_SPEND')
    if df_spend is not None:
        plot_cur_spend(df_spend)

    # 货币存量
    df_stock = loader.load_sheet('CUR_STOCK', usecols=range(21))
    if df_stock is not None:
        plot_cur_stock(df_stock)
