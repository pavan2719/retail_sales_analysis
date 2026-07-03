"""
analysis.py
------------
Retail Sales Performance Analysis & Dashboard
Author: Chennam Pavan Kumar

Steps performed (matches the resume bullet points 1:1):
1. Load raw data and profile it.
2. Clean data: remove duplicates, handle nulls, fix bad entries.
3. Feature engineering: date parts, profit margin.
4. Exploratory analysis: revenue trend, category performance, regional
   heatmap, top products.
5. Save all charts to visuals/ and a stakeholder-ready Excel summary
   (with a pivot table + KPI sheet) to retail_sales_summary.xlsx.

Run with:  python3 analysis.py
"""
import pandas as pd
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import seaborn as sns

sns.set_theme(style="whitegrid")

RAW_PATH = "data/retail_sales.csv"
CLEAN_PATH = "data/retail_sales_clean.csv"
VIS_DIR = "visuals"

# ---------------------------------------------------------------------------
# 1. LOAD + PROFILE
# ---------------------------------------------------------------------------
df = pd.read_csv(RAW_PATH, parse_dates=["order_date"])
print("Raw shape:", df.shape)
print("\nNull counts:\n", df.isna().sum()[df.isna().sum() > 0])
print("\nDuplicate rows:", df.duplicated().sum())
print("\nNegative quantity rows:", (df["quantity"] < 0).sum())

# ---------------------------------------------------------------------------
# 2. CLEAN
# ---------------------------------------------------------------------------
df = df.drop_duplicates()
df["quantity"] = df["quantity"].abs()                       # fix bad sign entries
df["discount_pct"] = df["discount_pct"].fillna(df["discount_pct"].median())

# recompute money fields so they stay consistent after cleaning
df["gross_amount"] = df["unit_price"] * df["quantity"]
df["discount_amount"] = (df["gross_amount"] * df["discount_pct"] / 100).round(2)
df["net_amount"] = (df["gross_amount"] - df["discount_amount"]).round(2)
df["profit"] = (df["net_amount"] - (df["cost_price"] * df["quantity"])).round(2)

# simple outlier guard on net_amount using IQR
q1, q3 = df["net_amount"].quantile([0.25, 0.75])
iqr = q3 - q1
upper_bound = q3 + 3 * iqr
outliers = df[df["net_amount"] > upper_bound]
print(f"\nExtreme high-value outliers flagged (kept, not dropped): {len(outliers)}")

# ---------------------------------------------------------------------------
# 3. FEATURE ENGINEERING
# ---------------------------------------------------------------------------
df["year"] = df["order_date"].dt.year
df["month"] = df["order_date"].dt.to_period("M").astype(str)
df["margin_pct"] = (df["profit"] / df["net_amount"] * 100).round(2)

df.to_csv(CLEAN_PATH, index=False)
print(f"\nClean shape: {df.shape} -> saved to {CLEAN_PATH}")

# ---------------------------------------------------------------------------
# 4. EXPLORATORY ANALYSIS + VISUALS
# ---------------------------------------------------------------------------

# 4a. Monthly revenue trend
monthly = df.groupby("month", as_index=False)["net_amount"].sum()
plt.figure(figsize=(11, 5))
sns.lineplot(data=monthly, x="month", y="net_amount", marker="o")
plt.xticks(rotation=90, fontsize=7)
plt.title("Monthly Net Revenue Trend")
plt.ylabel("Net Revenue (₹)")
plt.xlabel("Month")
plt.tight_layout()
plt.savefig(f"{VIS_DIR}/01_monthly_revenue_trend.png", dpi=150)
plt.close()

# 4b. Category performance (revenue share)
cat_perf = df.groupby("category", as_index=False)["net_amount"].sum().sort_values("net_amount", ascending=False)
cat_perf["share_pct"] = (cat_perf["net_amount"] / cat_perf["net_amount"].sum() * 100).round(1)
plt.figure(figsize=(8, 5))
sns.barplot(data=cat_perf, x="net_amount", y="category", palette="viridis")
plt.title("Revenue by Category")
plt.xlabel("Net Revenue (₹)")
plt.tight_layout()
plt.savefig(f"{VIS_DIR}/02_category_revenue.png", dpi=150)
plt.close()
top3_share = cat_perf.head(3)["share_pct"].sum()
print(f"\nTop 3 categories account for {top3_share:.1f}% of revenue")

# 4c. Regional heatmap (category x region revenue)
pivot = df.pivot_table(values="net_amount", index="category", columns="region", aggfunc="sum")
plt.figure(figsize=(9, 5))
sns.heatmap(pivot, annot=True, fmt=".0f", cmap="YlGnBu")
plt.title("Revenue Heatmap: Category vs Region")
plt.tight_layout()
plt.savefig(f"{VIS_DIR}/03_region_category_heatmap.png", dpi=150)
plt.close()

# 4d. Top 10 products by revenue
top_products = df.groupby("product", as_index=False)["net_amount"].sum().sort_values("net_amount", ascending=False).head(10)
plt.figure(figsize=(8, 5))
sns.barplot(data=top_products, x="net_amount", y="product", palette="mako")
plt.title("Top 10 Products by Revenue")
plt.xlabel("Net Revenue (₹)")
plt.tight_layout()
plt.savefig(f"{VIS_DIR}/04_top_products.png", dpi=150)
plt.close()

# 4e. Payment mode distribution
plt.figure(figsize=(7, 5))
df["payment_mode"].value_counts().plot(kind="pie", autopct="%1.1f%%")
plt.title("Orders by Payment Mode")
plt.ylabel("")
plt.tight_layout()
plt.savefig(f"{VIS_DIR}/05_payment_mode_share.png", dpi=150)
plt.close()

print(f"\nSaved 5 charts to {VIS_DIR}/")

# ---------------------------------------------------------------------------
# 5. EXCEL SUMMARY FOR STAKEHOLDERS (pivot table + KPI sheet)
# ---------------------------------------------------------------------------
kpis = pd.DataFrame({
    "KPI": ["Total Net Revenue", "Total Profit", "Total Orders", "Avg Order Value", "Overall Margin %"],
    "Value": [
        round(df["net_amount"].sum(), 2),
        round(df["profit"].sum(), 2),
        df["order_id"].nunique(),
        round(df["net_amount"].sum() / df["order_id"].nunique(), 2),
        round(df["profit"].sum() / df["net_amount"].sum() * 100, 2),
    ],
})

with pd.ExcelWriter("retail_sales_summary.xlsx", engine="openpyxl") as writer:
    kpis.to_excel(writer, sheet_name="KPIs", index=False)
    pivot.to_excel(writer, sheet_name="Category_x_Region_Pivot")
    cat_perf.to_excel(writer, sheet_name="Category_Performance", index=False)
    top_products.to_excel(writer, sheet_name="Top_10_Products", index=False)

print("\nSaved retail_sales_summary.xlsx (KPIs + pivot tables)")
print("\nDone. See README.md for how to present this project.")
