# 05_analysis.py
# Sales analysis on the adjusted data. Saves tables to outputs/tables and charts 01-05 to outputs/figures.
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

sales = pd.read_csv(proc / "sales_adj.csv", dtype={"invoice_no": "str", "stock_code": "str"}, parse_dates=["invoice_date"])
orders = pd.read_csv(proc / "orders_adj.csv", dtype={"invoice_no": "str"}, parse_dates=["invoice_date"])

# December 2011 is incomplete (the data ends on 9 December), so trend work uses complete months only
o_c = orders[orders.invoice_date < "2011-12-01"].copy()
o_c["year"] = o_c.invoice_date.dt.year
o_c["month"] = o_c.invoice_date.dt.month
o_c["year_month"] = o_c.invoice_date.dt.to_period("M")

# 1. Monthly KPIs and trend chart
monthly = o_c.groupby("year_month").agg(revenue=("revenue", "sum"), orders=("invoice_no", "size"), customers=("customer_id", "nunique"))
monthly["aov"] = (monthly.revenue / monthly.orders).round(2)
monthly["mom_growth_pct"] = (monthly.revenue.pct_change() * 100).round(1)
monthly["rolling_3m"] = monthly.revenue.rolling(3).mean().round(0)
monthly["revenue"] = monthly.revenue.round(0)
monthly.to_csv(tabs / "monthly_kpis.csv")
x = monthly.index.astype(str)
plt.figure(figsize=(11, 5))
plt.plot(x, monthly.revenue.values, marker="o", label="Monthly revenue")
plt.plot(x, monthly.rolling_3m.values, linestyle="--", label="3-month average")
plt.xticks(range(0, len(x), 2), x[::2], rotation=45)
plt.title("Monthly Sales Revenue (GBP), Dec 2009 - Nov 2011")
plt.xlabel("Month")
plt.ylabel("Revenue (GBP)")
plt.legend()
plt.tight_layout()
plt.savefig(figs / "01_monthly_revenue.png", dpi=150)
plt.close()

# 2. Growth and seasonality
pv = o_c.pivot_table(index="month", columns="year", values="revenue", aggfunc="sum").round(0)
pv.to_csv(tabs / "seasonality_month_by_year.csv")
jn = o_c[o_c.month <= 11]
yr = jn.groupby("year").revenue.sum()
growth = (yr[2011] / yr[2010] - 1) * 100
q4 = o_c[o_c.month >= 10].revenue.sum() / o_c.revenue.sum() * 100
print("Jan-Nov growth:", round(growth, 1), "% | Oct-Dec share of revenue:", round(q4, 1), "%")
assert round(growth, 1) == 1.8 and round(q4, 1) == 35.1, "Growth or seasonality differ from the verified numbers"

# 3. Countries
by_country = sales.groupby("country").revenue.sum().sort_values(ascending=False)
ct = pd.DataFrame({"revenue": by_country.round(0), "share_pct": (by_country / by_country.sum() * 100).round(2)})
ct.to_csv(tabs / "revenue_by_country.csv")
assert round(ct.loc["United Kingdom", "share_pct"], 1) == 85.3, "UK share differs"
t = by_country.drop("United Kingdom").head(10)[::-1]
plt.figure(figsize=(9, 5))
plt.barh(t.index, t.values)
plt.title("Top 10 Export Markets by Revenue (excluding UK)")
plt.xlabel("Revenue (GBP)")
plt.tight_layout()
plt.savefig(figs / "02_top_countries_ex_uk.png", dpi=150)
plt.close()

# 4. Products
first_desc = sales.drop_duplicates("stock_code").set_index("stock_code").description
prod = sales.groupby("stock_code").agg(revenue=("revenue", "sum"), units=("quantity", "sum"), orders=("invoice_no", "nunique"))
prod["description"] = prod.index.map(first_desc)
prod = prod.sort_values("revenue", ascending=False)
prod.round(2).to_csv(tabs / "product_performance.csv")
top20 = prod.revenue.head(int(len(prod) * 0.2)).sum() / prod.revenue.sum() * 100
print("Top product:", prod.index[0], "| top 20% of products earn", round(top20, 1), "% of revenue")
assert prod.index[0] == "22423" and round(top20, 1) == 78.2, "Product results differ"
t = prod.head(10).iloc[::-1]
plt.figure(figsize=(10, 5))
plt.barh(t.description.str[:35], t.revenue.values)
plt.title("Top 10 Products by Revenue")
plt.xlabel("Revenue (GBP)")
plt.tight_layout()
plt.savefig(figs / "03_top_products.png", dpi=150)
plt.close()

# 5. Order value
med = o_c.revenue.median()
top_order = o_c.revenue.max()
print("Median order:", round(med, 2), "| mean order:", round(o_c.revenue.mean(), 2), "| largest order:", round(top_order, 2))
assert round(med, 2) == 301.22 and round(top_order, 2) == 52940.94, "Order value statistics differ"

# 6. Weekday and hour
days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
wd = o_c.groupby(o_c.invoice_date.dt.day_name()).agg(orders=("revenue", "size"), revenue=("revenue", "sum")).reindex(days).fillna(0).round(0)
hr = o_c.groupby(o_c.invoice_date.dt.hour).revenue.sum().round(0)
wd.to_csv(tabs / "weekday_summary.csv")
assert int(wd.loc["Thursday", "orders"]) == 7902 and int(hr.idxmax()) == 12, "Weekday or hour results differ"
plt.figure(figsize=(9, 4))
plt.bar(hr.index.astype(str), hr.values)
plt.title("Revenue by Hour of Day")
plt.xlabel("Hour (24h)")
plt.ylabel("Revenue (GBP)")
plt.tight_layout()
plt.savefig(figs / "04_revenue_by_hour.png", dpi=150)
plt.close()

# 7. Customer concentration (Pareto)
cust = sales.dropna(subset=["customer_id"]).groupby("customer_id").revenue.sum().sort_values(ascending=False)
c10 = cust.head(int(len(cust) * 0.1)).sum() / cust.sum() * 100
c20 = cust.head(int(len(cust) * 0.2)).sum() / cust.sum() * 100
print("Identified customers:", len(cust), "| top 10%:", round(c10, 1), "% | top 20%:", round(c20, 1), "%")
assert len(cust) == 5851 and round(c10, 1) == 63.2 and round(c20, 1) == 76.7, "Customer concentration differs"
cum = cust.cumsum() / cust.sum() * 100
pct_cust = np.arange(1, len(cust) + 1) / len(cust) * 100
plt.figure(figsize=(7, 5))
plt.plot(pct_cust, cum.values)
plt.axvline(10, linestyle="--")
plt.title("Customer Revenue Concentration (Pareto Curve)")
plt.xlabel("% of customers (largest first)")
plt.ylabel("Cumulative % of revenue")
plt.tight_layout()
plt.savefig(figs / "05_customer_pareto.png", dpi=150)
plt.close()
print("05_analysis.py finished: charts 01-05 saved")
