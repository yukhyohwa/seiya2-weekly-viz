# Seiya2每周数据报告生成器

这是一个自动化的Python脚本，用于读取Seiya2游戏的周报数据Excel文件，并生成一系列分析图表。

## 功能概览

本项目支持以下维度的数据分析与图表生成：

- **KPI 指标 (KPI)**: 关键绩效指标的可视化展示，包括 DAU, 收入等核心数据。
- **货币产销 (Currency)**: 游戏内钻石、金币等货币的产出与消耗监控。
- **活动分析 (Activities)**: 玩家在各类日常与限时活动中的参与度分析。
- **英雄养成 (Hero)**: 英雄角色的培养深度与使用频率统计。
- **用户基础 (User Base)**: 活跃用户分层与流失用户的趋势分析。

## 如何运行

### 1. (重要) 配置路径

打开根目录下的 `config.py` 文件。确保 `INPUT_FILE` 变量指向您的 `SEIYA2CN_WKLYREPORT_version3.xlsx` 文件，并根据需要修改 `OUTPUT_DIR` 变量。

默认配置会读取当前目录下的 `SEIYA2CN_WKLYREPORT_version3.xlsx` 文件，并将图片输出到 `report_images` 文件夹。

### 2. 安装依赖

在终端中，导航到此项目的根目录，然后运行：
```shell
pip install -r requirements.txt
```

### 3. 运行报告生成器

安装完依赖后，在项目根目录运行以下命令来执行整个报告生成过程：
```shell
python main.py
```

---

## Project Structure

```
.
├── main.py               # 程序主入口
├── config.py             # 所有配置，包括文件路径和图表样式
├── data_loader.py        # 负责从Excel加载数据
├── processors.py         # 包含数据清洗和转换的逻辑
├── plot_utils.py         # 通用的绘图辅助函数
├── plotting/             # 存放所有具体绘图逻辑的模块
│   ├── kpi.py            # KPI 指标分析
│   ├── currency.py       # 货币产销分析
│   ├── activities.py     # 活动参与度分析
│   ├── hero.py           # 英雄养成分析
│   └── user_base.py      # 用户基础分析
├── requirements.txt      # 项目的Python依赖库
├── README.md             # 本说明文件
└── SEIYA2CN_WKLYREPORT_version3.xlsx # (您需要提供的数据文件)
```
