# plot_utils.py
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from .. import config

def setup_matplotlib_style():
    """应用自定义的matplotlib样式"""
    style = config.get_plot_style()
    plt.rcParams.update(style)
    print("Matplotlib style updated.")

def save_plot(fig, filename, subdirectory=None):
    """
    将图表保存到输出目录.
    
    Args:
        fig: matplotlib figure 对象.
        filename: 输出文件名.
        subdirectory: 在输出目录中可选的子目录.
    """
    output_path = config.OUTPUT_DIR
    if subdirectory:
        output_path = output_path / subdirectory
        output_path.mkdir(parents=True, exist_ok=True)
        
    full_path = output_path / filename
    try:
        fig.savefig(full_path, bbox_inches='tight')
        print(f"Plot saved to {full_path}")
    except Exception as e:
        print(f"Error saving plot {full_path}: {e}")
    plt.close(fig)

def plot_stacked_bar(df, ax, x_col, y_col, category_col, title,
                     xlabel='', ylabel='',
                     xtick_rotation=0, legend_loc='best',
                     colors=None):
    """
    使用pivot_table创建一个更简洁的堆叠柱状图。

    Args:
        df: 包含数据的Pandas DataFrame。
        ax: Matplotlib axes对象。
        x_col: 作为x轴的列名。
        y_col: 作为y轴（值）的列名。
        category_col: 用于堆叠的分类列名。
        title: 图表标题。
    """
    colors = colors or config.DEFAULT_COLORS
    pivot_df = df.pivot_table(index=x_col, columns=category_col, values=y_col, aggfunc='sum').fillna(0)
    
    # 如果有分类顺序，则按此排序
    if category_col == 'regmonth2': # Example of specific ordering
        # Try to sort by converting to numeric, ignore errors for non-numeric
        sorted_cols = sorted(pivot_df.columns, key=lambda x: pd.to_numeric(x, errors='coerce'), reverse=True)
        pivot_df = pivot_df[sorted_cols]

    pivot_df.plot.bar(stacked=True, ax=ax, color=colors, width=0.8)
    
    ax.set_title(title, loc='left', fontsize=12)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    ax.tick_params(axis='x', rotation=xtick_rotation)
    ax.grid(False)
    ax.legend(loc=legend_loc, fontsize=8)
