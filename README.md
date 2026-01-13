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

如果需要自定义路径，可以修改 `src/seiya2_viz/config.py` 文件。

- `INPUT_FILE`: 默认指向 `data/raw/SEIYA2CN_WKLYREPORT_version3.xlsx`。
- `OUTPUT_DIR`: 默认指向 `reports/` 文件夹。

### 2. 安装依赖

在终端中，导航到此项目的根目录，然后运行：
```shell
pip install -r requirements.txt
```

### 3. 运行报告生成器

安装完依赖后，在项目根目录运行以下命令来执行整个报告生成过程：
```shell
python src/main.py
```

---

## Project Structure

```text
seiya2-weekly-viz/
├── data/                  # 数据目录
│   └── raw/               # 原始Excel文件
├── src/                   # 源代码目录
│   ├── main.py            # 程序主入口
│   └── seiya2_viz/        # 核心包
│       ├── core/          # 核心逻辑 (加载器、处理器)
│       ├── modules/       # 业务分析模块 (KPI, 货币等)
│       ├── utils/         # 通用工具
│       └── config.py      # 项目配置
├── reports/               # 生成的分析报告图片
├── tests/                 # 测试代码
├── requirements.txt      # 依赖库
└── README.md              # 项目说明
```
