# Technique Index

Where each technique is used in the project. Scripts are in src/.

| Area | Techniques | Where used |
|---|---|---|
| Data loading | read_excel, read_csv with explicit dtypes and date parsing, to_csv, pathlib file handling | 01_load_combine.py and every script |
| Data cleaning | Boolean filtering, duplicate detection, string methods and regular expressions, nullable integers, rule-based row labelling with np.select | 03_clean.py |
| Joins | merge_asof (time-based join with a tolerance), join, concat | 01, 04, 06 |
| Aggregation | groupby with named aggregation, transform, pivot_table, unstack, nunique | 04, 05, 06 |
| Time series | Datetime accessor, periods, rolling averages, pct_change, month and year comparisons | 05, 07 |
| Customer analytics | Pareto concentration, cohort retention, RFM segmentation with qcut and rank | 05, 06 |
| Forecasting | Seasonal growth-adjusted forecast with scenarios and a backtest | 07_forecast.py |
| Validation | Assertions against verified totals, row-count reconciliation, a saved pipeline log | every script, outputs/pipeline_log.txt |
| Visualisation | Line, bar and horizontal bar charts, heatmap, shaded range, saved with matplotlib | 05, 06, 07 |
| Reproducibility | Numbered scripts, run_all.py, requirements.txt, .gitignore | src/, repository root |
