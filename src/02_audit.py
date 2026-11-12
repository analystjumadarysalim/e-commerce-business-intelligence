# 02_audit.py
# Phase 3: measure data quality without changing anything.
import pandas as pd
from pathlib import Path

project = Path(__file__).resolve().parent.parent
retail = pd.read_csv(project / "data/processed/online_retail_combined.csv", dtype={"invoice_no": "str", "stock_code": "str"}, parse_dates=["invoice_date"])
cols = [c for c in retail.columns if c != "source_sheet"]
is_cancel = retail.invoice_no.str.startswith("C")

print("Shape:", retail.shape)
print("\nMissing values:\n", retail.isna().sum())
print("\nIdentical rows (ignoring sheet):", retail.duplicated(subset=cols).sum())
print("Cancellation rows:", is_cancel.sum())
print("Quantity <= 0 (not cancellations):", ((retail.quantity <= 0) & ~is_cancel).sum())
print("Zero prices:", (retail.unit_price == 0).sum(), "| Negative prices:", (retail.unit_price < 0).sum())
print("\nNon-product codes:\n", retail[~retail.stock_code.str.match(r"^\d{5}", na=False)].stock_code.value_counts().head(15))
print("\nInvoices:", retail.invoice_no.nunique(), "| Products:", retail.stock_code.nunique(), "| Customers:", retail.customer_id.nunique(), "| Countries:", retail.country.nunique())
