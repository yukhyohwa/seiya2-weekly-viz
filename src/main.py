# main.py

import time
from seiya2_viz.utils import plotting
from seiya2_viz.modules import kpi, currency, user_base, hero, activities

def main():
    """
    主函数，按顺序执行周报所有图表的生成.
    """
    start_time = time.time()
    print("=========================================")
    print("  Seiya2 Weekly Report Generation Start  ")
    print("=========================================")

    # 1. 设置图表样式
    plotting.setup_matplotlib_style()

    # 2. 生成各类图表
    kpi.generate_all()
    currency.generate_all()
    user_base.generate_all()
    hero.generate_all()
    activities.generate_all()

    end_time = time.time()
    print("\n========================================")
    print(f"  Report Generation Finished in {end_time - start_time:.2f} seconds.")
    print("========================================")

if __name__ == '__main__':
    main()
