# Seiya2 Weekly Data Report Generator

[![Python](https://img.shields.io/badge/Python-3.8%2B-blue)](https://www.python.org/)
![Status](https://img.shields.io/badge/Status-Active-brightgreen)
![Platform](https://img.shields.io/badge/Platform-Cross--Platform-lightgrey)

An automated Python script designed to read weekly data from Seiya2 game Excel files and generate a comprehensive set of analytical charts and visualizations.

## Features

This project supports data analysis and visualization across the following dimensions:

- **KPI Metrics**: Visual presentation of key performance indicators, including core data such as DAU and Revenue.
- **Currency Flow**: Monitoring of production and consumption for in-game currencies (e.g., Diamonds, Gold).
- **Activity Analysis**: Participation analysis of players in daily and limited-time events.
- **Hero Progression**: Statistics on hero character development depth and usage frequency.
- **User Base**: Active user stratification and trend analysis for churned users.

## Getting Started

### 1. (Important) Path Configuration

If you need to customize file paths, you can modify the `src/seiya2_viz/config.py` file.

- `INPUT_FILE`: Defaults to `data/raw/SEIYA2CN_WKLYREPORT_version3.xlsx`.
- `OUTPUT_DIR`: Defaults to the `reports/` folder.

### 2. Install Dependencies

Navigate to the project root directory in your terminal and run:
```shell
pip install -r requirements.txt
```

### 3. Run the Report Generator

After installing the dependencies, execute the entire report generation process by running:
```shell
python src/main.py
```

---

## Project Structure

```text
seiya2-weekly-viz/
├── data/                  # Data directory
│   └── raw/               # Raw Excel files
├── src/                   # Source code directory
│   ├── main.py            # Main entry point
│   └── seiya2_viz/        # Core package
│       ├── core/          # Core logic (Loaders, Processors)
│       ├── modules/       # Business analysis modules (KPI, Currency, etc.)
│       ├── utils/         # General utilities
│       └── config.py      # Project configuration
├── reports/               # Generated analysis report images
├── requirements.txt      # Dependency list
└── README.md              # Project documentation
```

## License

[MIT](LICENSE)
