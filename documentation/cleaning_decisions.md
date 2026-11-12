# Cleaning Decisions

Raw data is never edited. Every cleaned row is labelled with a `row_class`, and the analysis tables (`sales.csv`, `returns.csv`) are filtered from the labelled data. Script logic: Phase 4 of the project.

## Decision log

| # | Decision | Rows affected | Reason |
|---|---|---|---|
| 1 | Removed the 2009-2010 worksheet copy of the 2010-12-01 to 2010-12-09 transactions | 22,523 | The same transactions appear in both worksheets (identical rows, verified). Keeping both would double count about nine days of sales. Rows after removal: 1,044,848 |
| 2 | Converted `customer_id` from decimal to a nullable whole number | missing IDs stay missing | Missing IDs are treated as guest checkouts. They stay in sales analysis but are excluded from customer analysis. 77.4% of sales rows have a customer ID |
| 3 | Created `revenue = quantity * unit_price` | all rows | Needed for every analysis |
| 4 | Flagged exact duplicate rows, keeping the first copy | 11,812 | Repeated identical lines treated as entry duplicates. Assumption: a few may be legitimate repeat scans |
| 5 | Flagged non-product stock codes (POST, DOT, M, D, BANK CHARGES, ADJUST, AMAZONFEE, etc.) | 5,980 | Postage, fees and manual entries would distort product rankings |
| 6 | Separated cancellations (invoice starts with C, negative quantity, positive price) into a returns table | 17,914 | Analysed separately as refunds, not deleted |
| 7 | Flagged cancellations that did not fit the return pattern | 0 | None remained after the earlier rules |
| 8 | Flagged non-cancellation rows with quantity of zero or less | 3,362 | Stock adjustments or write-offs, not sales. Revenue effect: 0.00 |
| 9 | Flagged rows with unit price of zero or less | 2,566 | Not real sales. Revenue effect: 0.00 |

Rules are applied in this order, and a row receives the first label that matches: duplicate, non_product, return, odd_cancellation, adjustment, bad_price. Everything else is labelled sale.

## Result of cleaning

| row_class | rows | revenue (GBP) |
|---|---|---|
| sale | 1,003,214 | 19,642,692.15 |
| return | 17,914 | -716,425.97 |
| duplicate | 11,812 | 54,228.42 |
| non_product | 5,980 | -70,732.50 |
| adjustment | 3,362 | 0.00 |
| bad_price | 2,566 | 0.00 |
| **Total** | **1,044,848** | |

Validation: the six row counts add up exactly to the 1,044,848 rows kept. The saved files were read back from disk and their row counts matched (sales 1,003,214; returns 17,914).

## Known limitations

- Extreme quantities (up to 80,995 units in one line) remain in the sales table. Analyses use medians where averages would be distorted.
- The duplicate rule is an assumption and may flag a few legitimate repeat lines.
- Returns carry no reference to the original sale, so return rates compare refunds and sales in the same period.

## Phase 5b additions: reversed orders

| # | Decision | Rows affected | Reason |
|---|---|---|---|
| 10 | Excluded reversed orders. A cancellation is paired with the nearest earlier sale by the same customer, for the same product and the exact opposite quantity, when it comes within 24 hours. Both rows are left out of the performance tables (sales_adj.csv and returns_adj.csv) but stay in the original files | 1,331 pairs (1,331 sale lines and 1,331 cancellation lines) | These are order-entry reversals, not demand or customer returns. They account for GBP 388,911 of sales (1.98 percent) and GBP 351,210 of refunds (49.0 percent of all refund value) |
| 11 | Excluded the pair for product 22502 (customer 15098, 10 June 2011) as an error | 1 pair, included in the 1,331 | 60 units were sold at GBP 649.50 (GBP 38,970) and refunded 11 minutes later at GBP 4.95 (GBP 297), a price about 130 times lower. Assumed to be a pricing error. This is an assumption, not confirmed by the data. It explains almost all of the GBP 37,702 gap between reversed sales and refunds |
| 12 | Kept invoice 574941 (7 Nov 2011, GBP 52,941, 14,149 items, no customer ID) | 1 order | Many different products at plausible quantities; looks like a genuine bulk order, unlike the 80,995-unit line that was reversed |

## Result of the adjustment

| Table | Rows | Value (GBP) |
|---|---|---|
| sales_adj.csv | 1,001,883 | 19,253,781 |
| returns_adj.csv | 16,583 | 365,216 (refunds) |

Refunds are 1.9 percent of adjusted sales. Before the adjustment they were GBP 716,426, about 3.6 percent of sales. Validation: both saved files were read back from disk and their row counts matched the expected counts.

## Limitations of the reversal rule

- Orders with no customer ID cannot be matched, so some reversals remain. The true reversal share is probably above 49.0 percent.
- Only exact reversals are caught. Partial reversals (different quantity) are not.
- The 24-hour window is a judgement call.
- One known mis-pairing: product 23056 (customer 14607, 24 Oct 2011). The refund of GBP 1,293.60 was paired with a later GBP 360 sale instead of the GBP 1,293.60 sale. The effect is under GBP 1,000.
