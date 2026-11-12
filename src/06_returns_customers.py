# 06_returns_customers.py
# Genuine returns, cohort retention and RFM segments on the adjusted data. Saves charts 06-08.
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from pathlib import Path

project = Path(__file__).resolve().parent.parent
proc = project / "data/processed"
figs = project / "outputs/figures"
tabs = project / "outputs/tables"
figs.mkdir(parents=True, exist_ok=True)
tabs.mkdir(parents=True, exist_ok=True)

dt = {"invoice_no": "str", "stock_code": "str"}
sales = pd.read_csv(proc / "sales_adj.csv", dtype=dt, parse_dates=["invoice_date"])
returns = pd.read_csv(proc / "returns_adj.csv", dtype=dt, parse_dates=["invoice_date"])
cut = pd.Timestamp("2011-12-01")

# A. Returns
returns["refund"] = -returns.revenue
returns["units_back"] = -returns.quantity
total_sales = sales.revenue.sum()
total_refunds = returns.refund.sum()
rate = total_refunds / total_sales * 100
print("Sales:", round(total_sales), "| refunds:", round(total_refunds), "| refund rate:", round(rate, 2), "%")
assert round(total_sales) == 19253781 and round(total_refunds) == 365216 and round(rate, 1) == 1.9, "Return totals differ"

sales["ym"] = sales.invoice_date.dt.to_period("M")
returns["ym"] = returns.invoice_date.dt.to_period("M")
s_m = sales[sales.invoice_date < cut].groupby("ym").revenue.sum()
r_m = returns[returns.invoice_date < cut].groupby("ym").refund.sum()
rm = pd.DataFrame({"sales": s_m, "refunds": r_m}).fillna(0)
rm["return_rate_pct"] = (rm.refunds / rm.sales * 100).round(2)
rm.to_csv(tabs / "monthly_returns.csv")
assert rm.return_rate_pct.idxmax() == pd.Period("2011-04", "M"), "Peak return month differs"
plt.figure(figsize=(11, 4))
plt.plot(rm.index.astype(str), rm.return_rate_pct.values, marker="o")
plt.xticks(range(0, len(rm), 2), rm.index.astype(str)[::2], rotation=45)
plt.title("Monthly Genuine Returns as % of Sales Revenue")
plt.xlabel("Month")
plt.ylabel("Refunds / sales (%)")
plt.tight_layout()
plt.savefig(figs / "06_monthly_return_rate.png", dpi=150)
plt.close()

desc = sales.drop_duplicates("stock_code").set_index("stock_code").description
ps = sales.groupby("stock_code").agg(sales=("revenue", "sum"), units_sold=("quantity", "sum"))
pr = returns.groupby("stock_code").agg(refunds=("refund", "sum"), units_returned=("units_back", "sum"), return_invoices=("invoice_no", "nunique"))
pp = ps.join(pr, how="left").fillna(0)
pp["return_rate_pct"] = pp.refunds / pp.sales * 100
pp["description"] = pp.index.map(desc)
pp.sort_values("refunds", ascending=False).round(2).to_csv(tabs / "product_returns.csv")
cdf = pd.DataFrame({"sales": sales.groupby("country").revenue.sum(), "refunds": returns.groupby("country").refund.sum()}).fillna(0)
cdf["return_rate_pct"] = cdf.refunds / cdf.sales * 100
cdf.round(2).to_csv(tabs / "country_returns.csv")

# B. Cohort retention
cs = sales[(sales.invoice_date < cut) & sales.customer_id.notna()].copy()
cs["customer_id"] = cs.customer_id.astype(int)
cs["cohort"] = cs.groupby("customer_id").invoice_date.transform("min").dt.to_period("M")
cs["idx"] = cs.invoice_date.dt.year * 12 + cs.invoice_date.dt.month
cs["cohort_idx"] = cs.cohort.dt.year * 12 + cs.cohort.dt.month
cs["period"] = cs.idx - cs.cohort_idx
counts = cs.groupby(["cohort", "period"]).customer_id.nunique().unstack()
retention = counts.div(counts[0], axis=0) * 100
retention.round(1).to_csv(tabs / "cohort_retention.csv")
avg1 = retention.mean().loc[1]
print("First cohort size:", int(counts[0].iloc[0]), "| average month-1 retention:", round(avg1, 1), "%")
assert int(counts[0].iloc[0]) == 951 and round(avg1, 1) == 21.2, "Cohort results differ"
plt.figure(figsize=(11, 7))
plt.imshow(retention.values, aspect="auto")
plt.colorbar(label="% of cohort still buying")
plt.xticks(range(len(retention.columns)), retention.columns)
plt.yticks(range(0, len(retention), 2), retention.index.astype(str)[::2])
plt.title("Customer Retention by Monthly Cohort")
plt.xlabel("Months since first purchase")
plt.ylabel("First-purchase month")
plt.tight_layout()
plt.savefig(figs / "07_cohort_heatmap.png", dpi=150)
plt.close()

# C. RFM segments
snap = sales.invoice_date.max().normalize() + pd.Timedelta(days=1)
ca = sales[sales.customer_id.notna()]
rfm = ca.groupby("customer_id").agg(last_order=("invoice_date", "max"), frequency=("invoice_no", "nunique"), monetary=("revenue", "sum"))
rfm["recency"] = (snap - rfm["last_order"]).dt.days
rfm["R"] = pd.qcut(rfm.recency.rank(method="first"), 5, labels=[5, 4, 3, 2, 1]).astype(int)
rfm["F"] = pd.qcut(rfm.frequency.rank(method="first"), 5, labels=[1, 2, 3, 4, 5]).astype(int)
rfm["M"] = pd.qcut(rfm.monetary.rank(method="first"), 5, labels=[1, 2, 3, 4, 5]).astype(int)
R = rfm.R.to_numpy()
F = rfm.F.to_numpy()
conds = [(R >= 4) & (F >= 4), (R >= 3) & (F >= 3), (R >= 4) & (F <= 2), (R <= 2) & (F >= 3), (R <= 2) & (F <= 2)]
names = ["Champions", "Loyal", "New / promising", "At risk", "Lost / hibernating"]
rfm["segment"] = np.select(conds, names, default="Needs attention")
seg = rfm.groupby("segment").agg(customers=("monetary", "size"), revenue=("monetary", "sum"), avg_recency_days=("recency", "mean"), avg_orders=("frequency", "mean"))
seg["pct_customers"] = seg.customers / seg.customers.sum() * 100
seg["pct_revenue"] = seg.revenue / seg.revenue.sum() * 100
seg = seg.sort_values("revenue", ascending=False)
repeat = (rfm.frequency >= 2).mean() * 100
print("Customers scored:", len(rfm), "| champions:", int(seg.loc["Champions", "customers"]), "| repeat buyers:", round(repeat, 1), "%")
assert len(rfm) == 5851 and int(seg.loc["Champions", "customers"]) == 1463 and round(repeat, 1) == 72.3, "RFM results differ"
rfm.to_csv(tabs / "rfm_customers.csv", float_format="%.2f")
seg.to_csv(tabs / "rfm_segments.csv", float_format="%.2f")
seg[["pct_customers", "pct_revenue"]].plot(kind="bar", figsize=(10, 5))
plt.title("Share of Customers vs Share of Revenue by RFM Segment")
plt.xlabel("Segment")
plt.ylabel("Percent")
plt.xticks(rotation=30, ha="right")
plt.tight_layout()
plt.savefig(figs / "08_rfm_segments.png", dpi=150)
plt.close()
print("06_returns_customers.py finished: charts 06-08 saved")
