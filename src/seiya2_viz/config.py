# config.py
from pathlib import Path
import matplotlib.pyplot as plt

# -----------------
# Path Configuration (Modify based on your environment)
# -----------------
# Root directory of the script (Project root)
PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
# Input Excel file path
INPUT_FILE = PROJECT_ROOT / 'data' / 'raw' / 'SEIYA2CN_WKLYREPORT_version3.xlsx'
# Output directory for generated images
OUTPUT_DIR = PROJECT_ROOT / 'reports'

# Ensure the output directory exists
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# -----------------
# Chart Style Configuration
# -----------------
def get_plot_style():
    """Returns a dictionary of matplotlib chart styles"""
    return {
        "figure.facecolor": "#ffffff",
        "axes.facecolor": "#ffffff",
        "axes.grid": True,
        "axes.grid.axis": "y",
        "grid.color": "#d3d3d3",
        "grid.linewidth": 1,
        "axes.spines.left": False,
        "axes.spines.right": False,
        "axes.spines.top": False,
        "ytick.major.size": 0,
        "ytick.minor.size": 0,
        "ytick.labelsize": 12,
        "xtick.direction": "in",
        "xtick.major.size": 7,
        "xtick.color": "#191919",
        "xtick.labelsize": 12,
        "axes.edgecolor": "#191919",
        "axes.prop_cycle": plt.cycler('color',
                                    ['#006767', '#ff7f0e', '#2ca02c', '#d62728',
                                     '#9467bd', '#8c564b', '#e377c2', '#7f7f7f',
                                     '#bcbd22', '#17becf']),
        "axes.unicode_minus": False,
        "font.sans-serif": "Arial" # Use Arial for standard display
    }

# -----------------
# Common Dimensions and Mappings
# -----------------
DEFAULT_COLORS = ['#006767', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd', '#8c564b', '#e377c2', '#7f7f7f', '#bcbd22', '#17becf']

VIP_TYPE_MAPPING = {'Whale': 0, 'Super R': 1, 'Big R': 2, 'Medium R': 3, 'Small R': 4, 'Non-R or Cross-server New Role': 5}
VIP_TYPE_ORDER = ['Whale', 'Super R', 'Big R', 'Medium R', 'Small R', 'Non-R or Cross-server New Role']
VIP_TYPE_LABELS = ['Whale', 'Super R', 'Big R', 'Medium R', 'Small R', 'Non-R']

ZONE_TYPE_ORDER = ['Server Open 24Months+', 'Server Open 12Months+', 'Server Open 6Months+', 'Server Open 3Months+', 'Server Open 3Months-']
