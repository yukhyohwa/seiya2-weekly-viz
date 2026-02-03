# plot_utils.py
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from .. import config

def setup_matplotlib_style():
    """Apply custom matplotlib styles"""
    style = config.get_plot_style()
    plt.rcParams.update(style)
    print("Matplotlib style updated.")

def save_plot(fig, filename, subdirectory=None):
    """
    Save the chart to the output directory.
    
    Args:
        fig: matplotlib figure object.
        filename: Output filename.
        subdirectory: Optional subdirectory within the output directory.
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
    Create a clean stacked bar chart using pivot_table.

    Args:
        df: Pandas DataFrame containing the data.
        ax: Matplotlib axes object.
        x_col: Column name for the x-axis.
        y_col: Column name for the y-axis (values).
        category_col: Column name for stacking categories.
        title: Chart title.
    """
    colors = colors or config.DEFAULT_COLORS
    pivot_df = df.pivot_table(index=x_col, columns=category_col, values=y_col, aggfunc='sum').fillna(0)
    
    # Sort categories if a specific order is needed
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
