# 04_reversals.py
# Find order-entry reversals and build the adjusted tables.
# A cancellation is paired with the nearest earlier sale by the same customer,
# for the same product and the exact opposite quantity, within 24 hours.
import pandas as pd
from pathlib import Path

project = Path(__file__).resolve().parent.parent
proc = project / "data/processed"
dt = {"invoice_no": "str", "stock_code": "str"}
sales = pd.read_csv(proc / "sales.csv", dtype=dt, parse_dates=["invoice_date"])
returns = pd.read_csv(proc / "returns.csv", dtype=dt, parse_dates=["invoice_date"])
sales["row_id"] = sales.index
returns["row_id"] = returns.index

# 1. Prepare both sides (rows without a customer id cannot be matched)
s = sales.dropna(subset=["customer_id"]).copy()
r = returns.dropna(subset=["customer_id"]).copy()
s["match_qty"] = s.quantity
r["match_qty"] = -r.quantity
s["sale_date"] = s.invoice_date
s = s.rename(columns={"row_id": "row_id_sale", "revenue": "revenue_sale", "unit_price": "unit_price_sale"})
r = r.rename(columns={"row_id": "row_id_ret", "revenue": "revenue_ret", "unit_price": "unit_price_ret"})
keys = ["customer_id", "stock_code", "match_qty"]
s = s.sort_values("invoice_date")
r = r.sort_values("invoice_date")

# 2. For each cancellation, find the most recent earlier sale with the same keys, within 24 hours
left = r[keys + ["invoice_date", "row_id_ret", "revenue_ret", "unit_price_ret"]]
right = s[keys + ["invoice_date", "sale_date", "row_id_sale", "revenue_sale", "unit_price_sale"]]
pairs = pd.merge_asof(left, right, on="invoice_date", by=keys, direction="backward", tolerance=pd.Timedelta(hours=24))
pairs = pairs.dropna(subset=["row_id_sale"])
pairs["row_id_sale"] = pairs.row_id_sale.astype(int)
pairs = pairs.drop_duplicates("row_id_sale")
print("Reversed pairs:", len(pairs))
assert len(pairs) == 1331, "Reversed pair count differs from the verified number"

# 3. Save the adjusted tables
sales_adj = sales[~sales.row_id.isin(pairs.row_id_sale)].drop(columns="row_id")
returns_adj = returns[~returns.row_id.isin(pairs.row_id_ret)].drop(columns="row_id")
assert len(sales_adj) == 1001883 and len(returns_adj) == 16583, "Adjusted row counts differ"
sales_adj.to_csv(proc / "sales_adj.csv", index=False)
returns_adj.to_csv(proc / "returns_adj.csv", index=False)

# 4. One row per invoice
orders = sales_adj.groupby("invoice_no").agg(invoice_date=("invoice_date", "min"), customer_id=("customer_id", "first"), country=("country", "first"), items=("quantity", "sum"), revenue=("revenue", "sum")).reset_index()
assert orders.shape == (39393, 6), "Order table shape differs"
orders.to_csv(proc / "orders_adj.csv", index=False)
print("Saved sales_adj.csv, returns_adj.csv, orders_adj.csv | orders:", orders.shape)
