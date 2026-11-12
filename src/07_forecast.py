# 07_forecast.py
# Seasonal forecast (last year's same month times a growth rate) with a backtest. Saves chart 09.
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

orders = pd.read_csv(proc / "orders_adj.csv", dtype={"invoice_no": "str"}, parse_dates=["invoice_date"])
o = orders[orders.invoice_date < "2011-12-01"]
monthly = o.groupby(o.invoice_date.dt.to_period("M")).revenue.sum()
m10 = pd.Series(monthly.loc["2010-01":"2010-12"].values, index=range(1, 13))
m11 = pd.Series(monthly.loc["2011-01":"2011-11"].values, index=range(1, 12))

# Three growth rates measured from the data
r_low = m11.loc[1:8].sum() / m10.loc[1:8].sum()
r_high = m11.loc[9:11].sum() / m10.loc[9:11].sum()
r_base = m11.sum() / m10.loc[1:11].sum()
print("Growth rates: Jan-Aug", round((r_low - 1) * 100, 1), "% | Jan-Nov", round((r_base - 1) * 100, 1), "% | Sep-Nov", round((r_high - 1) * 100, 1), "%")
assert round((r_low - 1) * 100, 1) == -0.5 and round((r_base - 1) * 100, 1) == 1.8 and round((r_high - 1) * 100, 1) == 5.4, "Growth rates differ"

# Backtest: forecast Sep-Nov 2011 from data up to August
bt = pd.DataFrame({"actual": m11.loc[9:11], "same_month_last_year": m10.loc[9:11], "forecast": m10.loc[9:11] * r_low})
bt["forecast_error_pct"] = (bt["forecast"] / bt["actual"] - 1) * 100
bt["last_year_error_pct"] = (bt["same_month_last_year"] / bt["actual"] - 1) * 100
bt.index = ["2011-09", "2011-10", "2011-11"]
tot = bt[["actual", "forecast", "same_month_last_year"]].sum()
err = (tot["forecast"] / tot["actual"] - 1) * 100
print("Backtest three-month error:", round(err, 1), "%")
assert round(err, 1) == -5.6, "Backtest error differs"
bt.round(2).to_csv(tabs / "forecast_backtest.csv")

# December to date (1-8 December)
s = pd.read_csv(proc / "sales_adj.csv", usecols=["invoice_date", "revenue"], parse_dates=["invoice_date"])
d10 = s[(s.invoice_date >= "2010-12-01") & (s.invoice_date < "2010-12-09")].revenue.sum()
d11 = s[(s.invoice_date >= "2011-12-01") & (s.invoice_date < "2011-12-09")].revenue.sum()
r_dec = d11 / d10
print("1-8 December: 2010 =", round(d10), "| 2011 =", round(d11), "| ratio =", round(r_dec, 3))
assert round(d10) == 357473 and round(d11) == 415855, "December to date differs"

# Forecast December 2011 to March 2012
idx = ["2011-12", "2012-01", "2012-02", "2012-03"]
ly = pd.Series([m10.loc[12], m11.loc[1], m11.loc[2], m11.loc[3]], index=idx)
fc = pd.DataFrame({"same_month_last_year": ly, "low": ly * r_low, "base": ly * r_base, "high": ly * r_high})
fc["dec_to_date_method"] = np.nan
fc.loc["2011-12", "dec_to_date_method"] = ly.loc["2011-12"] * r_dec
base_total = fc["base"].sum()
print("Base-case total, Dec 2011 - Mar 2012:", round(base_total))
assert abs(base_total - 2604342) < 1, "Base forecast differs"
fc.round(0).to_csv(tabs / "forecast_scenarios.csv")

xh = np.arange(len(monthly))
xf = np.arange(len(monthly), len(monthly) + 4)
labels = [str(p) for p in monthly.index] + idx
plt.figure(figsize=(11, 5))
plt.plot(xh, monthly.values, marker="o", label="Actual")
plt.plot(np.r_[xh[-1], xf], np.r_[monthly.values[-1], fc["base"].values], marker="o", linestyle="--", label="Forecast (base)")
plt.fill_between(xf, fc["low"].values, fc["high"].values, alpha=0.3, label="Low to high range")
plt.xticks(range(0, len(labels), 2), labels[::2], rotation=45)
plt.title("Monthly Revenue (GBP) with Seasonal Forecast to March 2012")
plt.xlabel("Month")
plt.ylabel("Revenue (GBP)")
plt.legend()
plt.tight_layout()
plt.savefig(figs / "09_forecast.png", dpi=150)
plt.close()
print("07_forecast.py finished: chart 09 saved")
