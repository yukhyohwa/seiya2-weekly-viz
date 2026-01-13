# config.py
from pathlib import Path
import matplotlib.pyplot as plt

# -----------------
# 路径配置 (请根据您的环境修改)
# -----------------
# 脚本的根目录 (项目根目录)
PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
# 输入的Excel文件路径
INPUT_FILE = PROJECT_ROOT / 'data' / 'raw' / 'SEIYA2CN_WKLYREPORT_version3.xlsx'
# 生成图片的输出目录
OUTPUT_DIR = PROJECT_ROOT / 'reports'

# 确保输出目录存在
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# -----------------
# 图表样式配置
# -----------------
def get_plot_style():
    """返回matplotlib图表样式字典"""
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
        "font.sans-serif": "SimHei" # 使用黑体显示中文
    }

# -----------------
# 通用维度和映射
# -----------------
DEFAULT_COLORS = ['#006767', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd', '#8c564b', '#e377c2', '#7f7f7f', '#bcbd22', '#17becf']

VIP_TYPE_MAPPING = {'鲸鱼': 0, '超R': 1, '大R': 2, '中R': 3, '小R': 4, '非R或跨服新角色': 5}
VIP_TYPE_ORDER = ['鲸鱼', '超R', '大R', '中R', '小R', '非R或跨服新角色']
VIP_TYPE_LABELS = ['鲸鱼', '超R', '大R', '中R', '小R', '非R']

ZONE_TYPE_ORDER = ['开服24月+', '开服12月+', '开服6月+', '开服3月+', '开服3月-']
