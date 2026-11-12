# 03_clean.py
# Remove the sheet overlap, add revenue, label every row, and save the sales and returns tables.
# Raw data is never edited; every row is kept and labelled in the row_class column.
import numpy as np
import pandas as pd
from pathlib import Path

project = Path(__file__).resolve().parent.parent
proc = project / "data/processed"

retail = pd.read_csv(proc / "online_retail_combined.csv", dtype={"invoice_no": "str", "stock_code": "str"}, parse_dates=["invoice_date"])
print("Loaded:", retail.shape)

# 1. Remove the 2009-2010 copy of the 1-9 December 2010 rows (they also appear in the 2010-2011 sheet)
overlap = (retail.source_sheet == "Year 2009-2010") & (retail.invoice_date >= "2010-12-01")
retail = retail[~overlap].reset_index(drop=True)
assert len(retail) == 1044848, "Row count after removing the overlap changed"

# 2. Types and revenue
retail["customer_id"] = retail["customer_id"].astype("Int64")
retail["revenue"] = (retail.quantity * retail.unit_price).round(2)

# 3. Flags
id_cols = ["invoice_no", "stock_code", "description", "quantity", "invoice_date", "unit_price", "customer_id", "country"]
is_cancel = retail.invoice_no.str.startswith("C")
is_dup = retail.duplicated(subset=id_cols, keep="first")
is_nonprod = ~retail.stock_code.str.match(r"^\d{5}", na=False)

# 4. One label per row (the first matching rule wins)
conditions = [is_dup, is_nonprod, is_cancel & (retail.quantity < 0) & (retail.unit_price > 0), is_cancel, (retail.quantity <= 0) & ~is_cancel, retail.unit_price <= 0]
labels = ["duplicate", "non_product", "return", "odd_cancellation", "adjustment", "bad_price"]
retail["row_class"] = np.select([c.to_numpy() for c in conditions], labels, default="sale")
counts = retail.row_class.value_counts().to_dict()
print("Row classes:", counts)
expected = {"sale": 1003214, "return": 17914, "duplicate": 11812, "non_product": 5980, "adjustment": 3362, "bad_price": 2566}
assert counts == expected, "Row classes differ from the verified numbers"

# 5. Save the analysis tables
retail[retail.row_class == "sale"].to_csv(proc / "sales.csv", index=False)
retail[retail.row_class == "return"].to_csv(proc / "returns.csv", index=False)
print("Saved sales.csv and returns.csv")
