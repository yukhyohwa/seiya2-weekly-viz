# plotting/hero.py
import pandas as pd
import matplotlib.pyplot as plt
import data_loader
from plot_utils import save_plot

def plot_hero_hold(df: pd.DataFrame):
    """生成核心角色持有人数图表"""
    df_core_heroes = df[df['core'] == 1].copy()

    fig, ax = plt.subplots(figsize=(14, 7), tight_layout=True)

    ax.plot(df_core_heroes['card_name'], df_core_heroes['hu_tw'], linewidth=3.0, linestyle='-', marker='o', label='This Week Holders')
    ax.plot(df_core_heroes['card_name'], df_core_heroes['hu_lw'], linewidth=3.0, linestyle='-', marker='x', label='Last Week Holders')

    # 添加数据标签
    for x, y in zip(df_core_heroes['card_name'], df_core_heroes['hu_lw']):
        ax.text(x, y - 500, str(y), ha='center', va='bottom', fontsize=9, color='#ff7f0e')

    for x, y in zip(df_core_heroes['card_name'], df_core_heroes['hu_tw']):
        ax.text(x, y + 200, str(y), ha='center', va='bottom', fontsize=9, color='#006767')

    ax.tick_params(axis='x', rotation=90, labelsize=10)
    ax.legend(loc='upper right', fontsize=12)
    ax.set_ylabel('Number of Holders')
    ax.set_xlabel('Core Hero')
    fig.suptitle('Holders of Gold Soul Collaboration Characters (Core)', x=0.02, y=.98, ha='left', fontsize=20)
    
    save_plot(fig, 'hero_hold_core.jpg', subdirectory='hero')

def generate_all():
    """生成所有英雄相关的图表"""
    print("\n--- Generating Hero Plots ---")
    
    df_hero = data_loader.load_sheet('HERO_HOLD', usecols=range(7))
    if df_hero is not None:
        plot_hero_hold(df_hero)
