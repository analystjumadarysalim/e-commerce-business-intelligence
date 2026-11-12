# 01_load_combine.py
# Read both worksheets of the raw workbook, standardise column names, combine, save as CSV.
# Slow (about 13 minutes on a phone) because Excel files are slow to read.
import pandas as pd
from pathlib import Path

project = Path(__file__).resolve().parent.parent
raw = project / "data/raw/Online_Retail_II.xlsx"
out = project / "data/processed/online_retail_combined.csv"
rename_map = {"invoice": "invoice_no", "stockcode": "stock_code", "invoicedate": "invoice_date", "price": "unit_price"}

def tidy(df, sheet):
    df.columns = df.columns.str.strip().str.lower().str.replace(" ", "_")
    df = df.rename(columns=rename_map)
    df["source_sheet"] = sheet
    return df

frames = []
for sheet in ["Year 2009-2010", "Year 2010-2011"]:
    frames.append(tidy(pd.read_excel(raw, sheet_name=sheet), sheet))
    print("Read", sheet, frames[-1].shape)

retail = pd.concat(frames, ignore_index=True)
assert retail.shape == (1067371, 9), "Combined shape changed"
out.parent.mkdir(parents=True, exist_ok=True)
retail.to_csv(out, index=False)
print("Saved", retail.shape, "to", out)
