# Retail Sales Performance Analysis & Dashboard

An end-to-end EDA project on multi-region retail transaction data: cleaning,
feature engineering, visualization, and a stakeholder-ready Excel summary.
This is the exact code behind the matching bullet point on the resume — run
it yourself to reproduce every number.

## What this project demonstrates
- Data cleaning (duplicates, nulls, bad data entry, outlier detection)
- Feature engineering (date parts, profit margin)
- Exploratory Data Analysis with Pandas
- Data visualization with Matplotlib/Seaborn
- Business-ready reporting in Excel (KPIs + pivot tables)

## Folder structure
```
retail_sales_analysis/
├── generate_data.py     # creates a synthetic 10,000-row dataset (swap for real data any time)
├── analysis.py          # the actual analysis: cleaning -> EDA -> charts -> Excel
├── data/
│   ├── retail_sales.csv         # raw data (with intentional dupes/nulls to clean)
│   └── retail_sales_clean.csv   # output: cleaned dataset
├── visuals/              # output: 5 PNG charts
└── retail_sales_summary.xlsx  # output: KPI + pivot workbook
```

## How to run it
```bash
pip install pandas numpy matplotlib seaborn openpyxl
python3 generate_data.py   # step 1: create the dataset
python3 analysis.py        # step 2: clean, analyze, chart, export
```

## What you get
- `visuals/01_monthly_revenue_trend.png` — revenue trend over time
- `visuals/02_category_revenue.png` — revenue by category
- `visuals/03_region_category_heatmap.png` — region x category revenue heatmap
- `visuals/04_top_products.png` — top 10 products by revenue
- `visuals/05_payment_mode_share.png` — payment method breakdown
- `retail_sales_summary.xlsx` — KPI sheet + pivot tables for non-technical stakeholders

## Key insight this project surfaces
The top 3 product categories account for **90%+ of total revenue** — a real,
reproducible finding printed to the console when you run `analysis.py`.

## Using this with real data
Replace `data/retail_sales.csv` with any real transaction-level dataset
(e.g. a Kaggle "retail sales" or "superstore" dataset) that has these
columns, and `analysis.py` runs unchanged:
`order_id, order_date, customer_id, region, category, product, quantity,
unit_price, discount_pct, cost_price`.

## How to talk about this in interviews
- "I generated a realistic dataset with deliberate data-quality issues so I
  could demonstrate the full cleaning pipeline, not just charting."
- "I used the IQR method to flag outliers rather than blindly dropping them,
  since high-value orders are often legitimate, not errors."
- "The Excel export sheet is designed for a non-technical stakeholder —
  KPIs first, supporting pivot tables after."

## Putting it on GitHub
```bash
git init
git add .
git commit -m "Retail sales EDA and dashboard project"
git remote add origin https://github.com/pavan2719/retail-sales-analysis.git
git push -u origin main
```
Then link the repo from the resume's GitHub/project section.
