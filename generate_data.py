"""
generate_data.py
-----------------
Creates a realistic synthetic retail sales dataset (data/retail_sales.csv)
so the analysis script has something to run on. In a real portfolio project
you would swap this for a real dataset (e.g. a Kaggle retail dataset), but
the analysis code (analysis.py) works unchanged either way as long as the
column names match.
"""
import numpy as np
import pandas as pd

np.random.seed(42)

N_ROWS = 10000
START_DATE = "2023-01-01"
END_DATE = "2025-12-31"

regions = ["North", "South", "East", "West", "Central"]
categories = {
    "Electronics": ["Smartphone", "Laptop", "Headphones", "Smartwatch"],
    "Clothing": ["T-Shirt", "Jeans", "Jacket", "Sneakers"],
    "Home & Kitchen": ["Blender", "Cookware Set", "Vacuum Cleaner", "Lamp"],
    "Beauty": ["Shampoo", "Face Cream", "Perfume", "Lipstick"],
    "Sports": ["Yoga Mat", "Dumbbells", "Cricket Bat", "Running Shoes"],
}
payment_modes = ["Credit Card", "Debit Card", "UPI", "Net Banking", "Cash on Delivery"]

dates = pd.date_range(START_DATE, END_DATE, freq="D")

rows = []
order_id = 100000
for _ in range(N_ROWS):
    order_id += 1
    date = np.random.choice(dates)
    category = np.random.choice(list(categories.keys()), p=[0.30, 0.25, 0.18, 0.15, 0.12])
    product = np.random.choice(categories[category])
    region = np.random.choice(regions)
    unit_price = {
        "Electronics": np.random.randint(1500, 60000),
        "Clothing": np.random.randint(300, 4000),
        "Home & Kitchen": np.random.randint(500, 12000),
        "Beauty": np.random.randint(150, 3000),
        "Sports": np.random.randint(400, 8000),
    }[category]
    quantity = np.random.randint(1, 6)
    discount_pct = np.random.choice([0, 5, 10, 15, 20], p=[0.4, 0.25, 0.2, 0.1, 0.05])
    gross_amount = unit_price * quantity
    discount_amount = round(gross_amount * discount_pct / 100, 2)
    net_amount = round(gross_amount - discount_amount, 2)
    cost_price = round(unit_price * np.random.uniform(0.55, 0.8), 2)
    profit = round(net_amount - (cost_price * quantity), 2)
    payment_mode = np.random.choice(payment_modes)
    # inject some realistic messiness
    customer_id = f"CUST{np.random.randint(1, 2201):05d}"

    rows.append([
        order_id, date, customer_id, region, category, product,
        quantity, unit_price, discount_pct, gross_amount, discount_amount,
        net_amount, cost_price, profit, payment_mode,
    ])

df = pd.DataFrame(rows, columns=[
    "order_id", "order_date", "customer_id", "region", "category", "product",
    "quantity", "unit_price", "discount_pct", "gross_amount", "discount_amount",
    "net_amount", "cost_price", "profit", "payment_mode",
])

# Inject realistic data-quality issues for the cleaning step to fix
dupe_sample = df.sample(50, random_state=1)
df = pd.concat([df, dupe_sample], ignore_index=True)                 # duplicates
null_idx = df.sample(120, random_state=2).index
df.loc[null_idx, "discount_pct"] = np.nan                            # missing values
neg_idx = df.sample(15, random_state=3).index
df.loc[neg_idx, "quantity"] = -df.loc[neg_idx, "quantity"]            # bad data entry

df.to_csv("data/retail_sales.csv", index=False)
print(f"Generated data/retail_sales.csv with {len(df)} rows (includes intentional dupes/nulls/bad rows).")
