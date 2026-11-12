# Data Dictionary

Source: Chen, D. (2012). Online Retail II. UCI Machine Learning Repository. https://doi.org/10.24432/C5CG6D (CC BY 4.0)

| Column | Type | Description | Known issues |
|---|---|---|---|
| `invoice_no` | text | Invoice number, 6 digits. A leading C marks a cancellation. | Mixed numeric and C-prefixed values, so must stay text |
| `stock_code` | text | Product code, 5 digits (sometimes with a letter suffix). | Contains non-product codes such as POST, DOT, M, D |
| `description` | text | Product name. | Some missing |
| `quantity` | integer | Units per line. Negative for cancellations and adjustments. | Extreme outliers (+/-80,995) |
| `invoice_date` | datetime | Date and time of the transaction. | Overlap between the two sheets, 2010-12-01 to 2010-12-09 |
| `unit_price` | float | Price per unit in pounds sterling. | Zero and negative values present |
| `customer_id` | float (raw) | 5-digit customer number. | About 23% missing; stored as float |
| `country` | text | Country where the customer lives. | |
| `source_sheet` | text | Added by us: which worksheet the row came from. | Audit trail only |

## Derived columns (added during cleaning)
Will be listed here as we create them, e.g. `revenue = quantity * unit_price`.

## Derived columns added during cleaning

| Column | Definition |
|---|---|
| `revenue` | quantity * unit_price, rounded to 2 decimals |
| `row_class` | One of: sale, return, duplicate, non_product, odd_cancellation, adjustment, bad_price |

Analysis tables: `sales.csv` (row_class = sale) and `returns.csv` (row_class = return).
