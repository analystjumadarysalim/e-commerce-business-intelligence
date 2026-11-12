# Findings

All figures use the adjusted data (sales_adj.csv and returns_adj.csv) unless stated. Trends use complete months only (Dec 2009 to Nov 2011), because the data ends on 9 Dec 2011. Source tables are in outputs/tables and charts in outputs/figures.

## Data quality

| # | Question | Result | Meaning |
|---|---|---|---|
| D1 | Did the two worksheets overlap? | 22,523 identical rows for 1-9 Dec 2010 appeared in both | Removing one copy prevents double counting nine days of sales |
| D2 | How many sales were later reversed? | 1,331 sale and cancellation pairs; 49.0 percent of refund value | The raw return rate of about 3.6 percent falls to 1.9 percent once order-entry reversals are excluded |

## Sales performance

| # | Question | Result | Meaning |
|---|---|---|---|
| P1 | Is revenue growing? | Jan-Nov 2011 vs 2010: +1.8 percent (GBP 8.54M to GBP 8.70M). Before the reversal adjustment it read +3.0 percent | Essentially flat |
| P2 | Where did the growth come from? | Jan-Aug fell 0.5 percent (GBP 5.17M to GBP 5.14M); Sep-Nov rose 5.4 percent (GBP 3.37M to GBP 3.56M); September 2011 alone was +18.6 percent | All of the growth came late in the year. See P9 for what drove September 2011. |
| P3 | Is there seasonality? | November peaks: GBP 1.42M (2010) and GBP 1.44M (2011). Jan-Aug months sit between GBP 0.51M and GBP 0.76M. Oct-Dec earns 35.1 percent of revenue | Strong autumn build-up; stock and staffing should follow it |
| P4 | Why does December drop? | December 2010 was GBP 772K, 45.8 percent below November. Sales stop on 23 Dec in both 2009 and 2010 | December is a shorter trading month, but it is still lower per day. The data does not say why |
| P5 | Which countries matter? | UK is about 85 percent of sales, then EIRE (GBP 614K), Netherlands (GBP 550K), Germany (GBP 383K), France (GBP 310K) | Heavy dependence on the UK; Ireland and the Netherlands lead the export markets |
| P6 | Which products earn most? | Regency Cakestand 3 Tier GBP 328K; White Hanging Heart T-Light Holder GBP 255K; Jumbo Bag Red White Spotty GBP 179K; Party Bunting GBP 148K; Assorted Colour Bird Ornament GBP 129K. The top 20 percent of products earn 78.2 percent of revenue | Close to an 80/20 split. By units, World War 2 Gliders lead (106,043 units) but earn only GBP 24K |
| P7 | What is a typical order? | Median GBP 301, mean GBP 488, 90th percentile GBP 904, 99th percentile GBP 3,991, largest GBP 52,941 | A few very large orders pull the mean up, so the median is the better typical order |
| P8 | When do customers buy? | Thursday and Tuesday are highest (GBP 3.85M and GBP 3.73M), then Monday and Wednesday (GBP 3.31M and GBP 3.30M), Friday GBP 2.86M and Sunday GBP 1.76M. Saturday has only 30 orders (GBP 9.8K). The busiest hours are hour 12 (GBP 2.71M), hour 13 (GBP 2.43M) and hour 11 (GBP 2.36M) | A weekday daytime pattern, consistent with business customers. The business barely trades on Saturdays but does on Sundays |
| P9 | What drove September 2011 (up GBP 160K, 18.6 percent on September 2010)? | The number of orders rose only 1.7 percent (1,783 to 1,814), but the median order rose 6.8 percent (GBP 303 to GBP 324) and the mean 16.6 percent (GBP 484 to GBP 564). Orders over GBP 2,000 rose from 44 to 68 and brought GBP 84K of the increase. The 10 largest orders were 11.0 percent of September revenue, down from 12.0 percent. Existing customers added GBP 198.9K, guest orders added GBP 25.9K and first-time customers fell GBP 64.3K. More products lost sales (1,936) than gained (1,569). The Regency Cakestand fell GBP 14.8K (GBP 24.4K to GBP 9.6K), the Vintage Union Jack cushion cover and doorstop fell to almost nothing, and the biggest gainers had almost no sales in September 2010 (pantry tin sets, a Keep Calm hot water bottle, Spotty Bunting) | Growth came from bigger orders, not from a few giant orders. The split between new and existing customers is biased because September 2011 has a longer look-back than September 2010, which overstates the shift away from first-time customers. The data does not say why the product mix moved |

## Customers

| # | Question | Result | Meaning |
|---|---|---|---|
| C1 | How concentrated is revenue? | The top 10 percent of identified customers give 63.2 percent of identified revenue and the top 20 percent give 76.7 percent (5,851 customers) | The business depends on a small group |
| C2 | How much revenue has no customer ID? | Identified customers are about 87 percent of revenue; guest orders are about GBP 2.57M and include 4 of the 5 largest orders | Customer analysis misses some of the largest buyers |
| C3 | Do customers come back? | 72.3 percent of identified customers ordered at least twice | High repeat rate |
| C4 | How does retention behave? | Share of a cohort buying again: 21.2 percent in month 1, 22.2 in month 2, 22.1 in month 3, 18.5 in month 6, 19.6 in month 12. The Nov 2010 cohort dips to 9.5 percent in months 2-3 but reaches 25.1 percent at month 12 | Retention levels off near one in five and customers return in the autumn. Each figure is the share active in that month, not the share still customers |
| C5 | Are we acquiring new customers? | First-time customers: 3,285 in Jan-Nov 2010 versus 1,511 in Jan-Nov 2011 | Acquisition probably slowed, but early 2010 cohorts include customers active before the data starts, so the fall is overstated |
| C6 | Who are the best customers? | Champions: 25.0 percent of customers and 70.1 percent of revenue (GBP 11.70M). Loyal: 20.8 percent and 14.5 percent. At risk: 14.2 percent and 8.9 percent (GBP 1.49M, average 368 days since last order). Lost: 25.8 percent and 3.7 percent | Revenue sits in an active core. At-risk revenue is historic spend and only partly recoverable |

## Returns

| # | Question | Result | Meaning |
|---|---|---|---|
| R1 | What is the return rate? | Genuine refunds GBP 365,216, 1.9 percent of sales. Most months fall between 1.0 and 2.6 percent | Low overall |
| R2 | How concentrated are refunds? | 7,078 cancellation invoices averaging about GBP 52. The 10 largest are 19.7 percent of refund value; the top 1 percent (70 invoices) are 37.9 percent. Without the 10 largest the overall rate is 1.52 percent | A few large cancellations drive refund totals |
| R3 | Why the monthly spikes? | April 2011 (6.15 percent) falls to 1.68 percent without the 10 largest cancellations; one invoice (C550456, GBP 22,998) did it. August 2011 falls from 2.55 to 1.52 percent. May 2010 falls only from 4.24 to 3.58 percent | Most spikes were single bulk returns. May 2010 is unexplained |
| R4 | Do some countries return more? | Spain 13.3 percent: 95 percent comes from one customer (12454). Denmark 6.0 percent: 89 percent from one invoice. France 5.3 percent: 72 percent from one invoice | Do not conclude these countries return more; each is a single event |
| R5 | Which products are returned often? | White Cherry Lights 35.1 percent (123 cancellation invoices), Pink Cherry Lights 28.5 percent (85), Two Door Curio Cabinet 22.8 percent (37), Eau De Nil Diner Wall Clock 16.7 percent (22), 3 Tier Cake Tin 13.6 percent (21) | Repeated across many separate cancellations, but the cherry lights are concentrated in time (see R8), so they look like one episode and not a lasting problem. The cause is not visible in the data. Products with only 7 to 9 cancellation invoices are weaker evidence |
| R6 | Which product has the largest refund total? | Regency Cakestand: GBP 14,393 across 325 invoices, 4.4 percent of its sales | Large because it is the top seller; its 4.4 percent rate is more than double the 1.9 percent average |
| R7 | Do any high rates rest on one invoice? | Fairy Cake Flannel (21108) has 3 cancellation invoices and 99 percent of its refunds from one; Door Mat Fairy Cake (48185) has 97 percent from one | Not product problems |
| R8 | Why was the May 2010 return rate high (4.24 percent)? | There were 370 cancellation invoices against a median month of 283, averaging GBP 73 each against a median month of GBP 44. Refunds were GBP 26,868 against a median month of GBP 12,029. The 3 largest invoices were only 24.4 percent of the month. Five light-string products (four cherry lights variants and Willow Branch Lights) made up GBP 11,281, or 42.0 percent of May 2010 refunds. May 2010 also holds 67 percent of the White Cherry Lights refund value and 60 percent of the Pink Cherry Lights refund value | More and larger cancellations than usual, led by decorative lights, so a product-specific episode and not a single bulk return. The data does not show why customers returned them |

## Forecast

Method: last year's same month multiplied by a growth rate taken from the data (low = Jan-Aug, base = Jan-Nov, high = Sep-Nov growth of 2011 over 2010). Figures use the adjusted data and complete months. Chart: outputs/figures/09_forecast.png. Tables: outputs/tables/forecast_scenarios.csv and forecast_backtest.csv.

| # | Question | Result | Meaning |
|---|---|---|---|
| F1 | How accurate is the method? | Backtest: Sep-Nov 2011 forecast from data up to August using the Jan-Aug growth rate (-0.5 percent). The three-month total was 5.6 percent too low (GBP 3.36M against GBP 3.56M actual); repeating last year was 5.1 percent too low. September was 16.1 percent too low, October 0.9 percent and November 1.7 percent. Mean absolute monthly error 6.3 percent | The growth adjustment did not beat repeating last year, and the method cannot foresee a sudden jump like September 2011. This is one three-month window, a reasonableness check and not proof |
| F2 | What is the outlook for Dec 2011 to Mar 2012? | Same months last year total GBP 2.56M. Scenarios: low GBP 2.54M (growth of -0.5 percent), base GBP 2.60M (+1.8 percent), high GBP 2.70M (+5.4 percent). Base by month: December GBP 786K, January GBP 602K, February GBP 517K, March GBP 700K | Roughly flat. The range is a scenario range built from observed growth rates, not a statistical confidence interval |
| F3 | How is early December 2011 trading? | 1-8 Dec 2011 revenue was GBP 415,855 against GBP 357,473 for the same days of 2010 (+16.3 percent). Those days were 46.3 percent of December 2010. Applying the ratio to the full month gives GBP 898K, above the high scenario (GBP 814K) | Early December is running ahead of last year, but this rests on about seven trading days and assumes the rest of the month follows the 2010 pattern. Treat GBP 898K as an upper marker. The data ends on 9 December 2011, so the outcome is unknown |

## Open questions

1. Why did the Regency Cakestand, the best-selling product, fall about 60 percent in September 2011 (GBP 24.4K to GBP 9.6K)? Stock, demand or customers switching products cannot be told apart from this data.
2. Why were decorative light strings returned so heavily in spring 2010? The cause is not in the data.
3. Is the fall in first-time customers real? It needs a comparison using the same look-back window in both years.
4. Why are several of the largest November orders guest checkouts?

## Limitations

- Guest orders (no customer ID) cannot be matched to customers or refunds.
- Returns carry no link to the original sale, so the return rate compares refunds and sales in the same period.
- Cohort figures near the start of the data are inflated by customers who were already active.
- RFM segment rules are judgement calls and can be changed.
- The new versus existing customer split depends on how far back the data looks (9 months in September 2010 against 21 months in September 2011). This tends to overstate the fall in first-time customers and the rise in existing ones.
- The forecast uses only two years of data, so each month has one earlier example and trend cannot be separated from seasonality.
