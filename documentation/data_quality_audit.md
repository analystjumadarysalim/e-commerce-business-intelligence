# Data Quality Audit

**Dataset:** Online Retail II (UCI Machine Learning Repository)
**Rows:** 1,067,371 | **Period:** 2009-12-01 to 2011-12-09
**Scale:** 53,628 invoices, 5,305 stock codes, 5,942 customers, 43 countries

Audit only: nothing was changed in this phase. Handling decisions are recorded in `cleaning_decisions.md`.

## Findings

| # | Check | Result | Planned handling |
|---|---|---|---|
| 1 | Missing `customer_id` | 243,007 rows (22.77%) | Keep for sales analysis; exclude from customer analysis (cohorts, RFM) |
| 2 | Missing `description` | 4,382 rows | Inspect in Phase 4 |
| 3 | Sheet overlap (2010-12-01 to 2010-12-09) | 22,523 rows in each sheet; 1,088 shared invoices; identical rows: True | Remove one copy to avoid double counting |
| 4 | Duplicate rows (all columns) | 34,335 total; 11,812 remaining after overlap removal | Investigate repeat scans vs. entry errors, then decide |
| 5 | Cancellations (invoice starts with C) | 19,494 rows (1.83%); 1 with positive quantity | Separate into a returns table; do not delete |
| 6 | Non-cancellation rows with quantity <= 0 | 3,457 | Inspect; likely adjustments, exclude from sales |
| 7 | Zero unit price | 6,202 | Inspect; exclude from revenue |
| 8 | Negative unit price | 5 | Inspect; exclude from revenue |
| 9 | Non-product stock codes (POST, DOT, M, D, BANK CHARGES, ADJUST, AMAZONFEE...) | 6,093 rows | Flag; exclude from product rankings |
| 10 | Extreme values | Quantity from -80,995 to 80,995; unit price from -53,594.36 to 38,970 | Inspect individually before any averages |

## Notes
- `customer_id` is stored as a float because of missing values; it will be converted to a nullable integer in cleaning.
- Row counts before cleaning: sheet 2009-2010 = 525,461; sheet 2010-2011 = 541,910.
