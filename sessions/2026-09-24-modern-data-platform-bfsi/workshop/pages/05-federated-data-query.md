---
title: "04. Federated Data Query"
weight: 38
---

In this module, we will explore the powerful federated query capabilities of SageMaker Catalog, showcasing the strength of the lakehouse architecture with Amazon SageMaker and demonstrating how to seamlessly work with data across multiple sources for financial services analytics.

First, we will create two S3 tables — market_data and risk_metrics — representing capital markets pricing and portfolio risk assessments. These complement the core banking data (customers, accounts, loans) already in our Aurora MySQL database.

Next, we will perform federated queries joining Aurora MySQL data (replicated via Zero-ETL integration) with S3 tables to answer a critical FSI question: when market prices drop, which customers see their risk scores spike, and do those customers have delinquent or defaulting loans?

Finally, we will explore how S3 tables leverage Apache Iceberg as the table format. With time travel and snapshot functionality, you can query historical versions of your risk data, track changes over time, and rollback when needed — essential for auditability and regulatory compliance in financial services.

### Prerequisites: Create market_data & risk_metrics S3 Tables

Before performing cross-catalog queries, we need to create two S3 tables that will be joined with Aurora MySQL data in the federated query examples.

**Data Architecture:**
- Aurora MySQL via Zero-ETL (`rms-catalog`): customers, accounts, loans — core banking data replicated automatically
- S3 Tables (`s3tablescatalog/s3-table` → `dev`): market_data, risk_metrics — capital markets and risk analytics
- Join key: `risk_metrics.customer_id` → `customers.customer_id` → `accounts` → `loans`
- Date alignment: `market_data` and `risk_metrics` share the same date partitions for temporal correlation

1. Navigate to your Amazon SageMaker portal. At the top of the portal, select "Data" from the *Current Project* dropdown.

2. Open a new query editor tab and change your connection type by clicking the Connections box in the top right corner:
* Under Connections, select *Athena (Lakehouse)*
* Under Catalogs, select *s3tablescatalog/s3-table*
* Under Databases, select *dev*
* Select **Choose**.

![SageMaker Query Editor](../source/static/images/FSI-Images/Screenshot%202026-03-10%20at%207.42.04%E2%80%AFPM.png)


### Create an S3 Table 

Now let's create an S3 Table to store real-time market data. In this example, we'll create a table for market data and risk metrics, which is critical for financial services operations to monitor trading activity, assess portfolio risk, and ensure regulatory compliance.

3. Copy and run the below SQL statement in the first cell to create the market_data table:

```sql
CREATE TABLE market_data (
  timestamp TIMESTAMP,
  instrument_id STRING,
  bid_price DOUBLE,
  ask_price DOUBLE,
  last_price DOUBLE,
  volume DOUBLE,
  open_price DOUBLE,
  high_price DOUBLE,
  low_price DOUBLE,
  vwap DOUBLE,
  year INT,
  month INT,
  day INT
)
PARTITIONED BY (year, month, day)
TBLPROPERTIES ('table_type'='ICEBERG');
```
![New table market_data has been created](../source/static/images/FSI-Images/Screenshot%202026-03-13%20at%2012.18.36%E2%80%AFPM.png)

4. Run the following query in a new SQL cell to load sample market data for financial instruments:

```sql
INSERT INTO market_data VALUES
  -- AAPL: Jan 10 (normal), Jan 15 (normal), Jan 20 (normal), Jan 22 (downturn), Feb 3 (weak), Feb 5 (weak), Feb 8 (partial recovery)
  (TIMESTAMP '2024-01-10 09:30:00', 'AAPL', 184.80, 185.00, 184.90, 1100000, 184.00, 185.50, 183.50, 184.70, 2024, 1, 10),
  (TIMESTAMP '2024-01-15 09:30:00', 'AAPL', 185.20, 185.30, 185.25, 1250000, 184.50, 186.10, 183.90, 185.05, 2024, 1, 15),
  (TIMESTAMP '2024-01-20 09:30:00', 'AAPL', 185.40, 185.55, 185.50, 1150000, 185.00, 186.00, 184.80, 185.30, 2024, 1, 20),
  (TIMESTAMP '2024-01-22 09:30:00', 'AAPL', 178.10, 178.30, 178.20, 2800000, 182.00, 182.50, 176.80, 178.90, 2024, 1, 22),
  (TIMESTAMP '2024-02-03 09:30:00', 'AAPL', 172.00, 172.20, 172.10, 3100000, 175.00, 175.50, 171.20, 173.00, 2024, 2, 3),
  (TIMESTAMP '2024-02-05 09:30:00', 'AAPL', 174.50, 174.70, 174.60, 2200000, 173.00, 175.80, 172.50, 174.20, 2024, 2, 5),
  (TIMESTAMP '2024-02-08 09:30:00', 'AAPL', 179.80, 180.10, 180.00, 1800000, 178.50, 181.00, 178.00, 179.60, 2024, 2, 8),

  -- MSFT: Jan 15 (normal), Jan 18 (normal), Jan 22 (downturn), Feb 5 (weak), Feb 8 (partial recovery)
  (TIMESTAMP '2024-01-15 09:30:00', 'MSFT', 388.10, 388.25, 388.15, 850000,  387.00, 389.50, 386.20, 387.90, 2024, 1, 15),
  (TIMESTAMP '2024-01-18 09:30:00', 'MSFT', 389.00, 389.20, 389.10, 780000,  388.00, 390.00, 387.50, 388.80, 2024, 1, 18),
  (TIMESTAMP '2024-01-22 09:30:00', 'MSFT', 371.50, 371.80, 371.60, 1900000, 380.00, 380.50, 370.00, 374.20, 2024, 1, 22),
  (TIMESTAMP '2024-02-05 09:30:00', 'MSFT', 370.20, 370.50, 370.40, 1600000, 372.00, 373.00, 369.50, 371.00, 2024, 2, 5),
  (TIMESTAMP '2024-02-08 09:30:00', 'MSFT', 375.00, 375.30, 375.20, 1200000, 373.50, 376.00, 373.00, 374.80, 2024, 2, 8),

  -- GOOGL: Jan 15 (normal), Jan 22 (downturn)
  (TIMESTAMP '2024-01-15 09:30:00', 'GOOGL', 141.50, 141.65, 141.55, 1500000, 140.80, 142.30, 140.10, 141.20, 2024, 1, 15),
  (TIMESTAMP '2024-01-22 09:30:00', 'GOOGL', 135.00, 135.30, 135.10, 2500000, 140.00, 140.20, 134.50, 136.80, 2024, 1, 22),

  -- BOND-001: Jan 15 (normal), Jan 22 (downturn - yields spike, prices drop)
  (TIMESTAMP '2024-01-15 10:00:00', 'BOND-001', 98.75, 98.82, 98.78, 50000, 98.50, 99.10, 98.30, 98.72, 2024, 1, 15),
  (TIMESTAMP '2024-01-22 10:00:00', 'BOND-001', 95.00, 95.15, 95.10, 85000, 97.50, 97.80, 94.80, 95.60, 2024, 1, 22),

  -- BOND-002: Feb 5 (weak market)
  (TIMESTAMP '2024-02-05 10:00:00', 'BOND-002', 101.20, 101.35, 101.25, 25000, 100.80, 101.60, 100.50, 101.15, 2024, 2, 5),

  -- EUR-USD: Feb 1
  (TIMESTAMP '2024-02-01 08:00:00', 'EUR-USD', 1.0825, 1.0828, 1.0826, 5200000, 1.0810, 1.0845, 1.0798, 1.0820, 2024, 2, 1),

  -- SPX-OPT: Feb 5 (weak market, volatility up)
  (TIMESTAMP '2024-02-05 09:30:00', 'SPX-OPT', 42.50, 42.80, 42.65, 320000, 41.90, 43.20, 41.50, 42.55, 2024, 2, 5);
```
![market_data records have been created](../source/static/images/FSI-Images/Screenshot%202026-03-13%20at%2012.19.05%E2%80%AFPM.png)

**Business Context:** This sample data captures market pricing for seven financial instruments across equities (AAPL, MSFT, GOOGL), fixed income (BOND-001, BOND-002), FX (EUR-USD), and derivatives (SPX-OPT). The data shows a clear market downturn pattern around January 22 — equity prices drop sharply (AAPL falls from $185 to $178, GOOGL from $141 to $135), bond prices decline as yields spike, and volatility increases. This downturn pattern is designed to correlate with elevated risk scores in the risk_metrics table for the same dates.


5. Create a table for risk metrics:

```sql
CREATE TABLE risk_metrics (
  timestamp TIMESTAMP,
  portfolio_id STRING,
  customer_id STRING COMMENT 'FK to Aurora fsidb.customers.customer_id',
  var_95 DOUBLE COMMENT 'Value at Risk 95% confidence in USD',
  var_99 DOUBLE COMMENT 'Value at Risk 99% confidence in USD',
  expected_shortfall DOUBLE COMMENT 'CVaR in USD',
  credit_exposure DOUBLE,
  market_risk_score DOUBLE COMMENT '0-100 scale',
  liquidity_risk_score DOUBLE COMMENT '0-100 scale',
  concentration_risk_pct DOUBLE COMMENT '0-100 percentage',
  compliance_status STRING COMMENT 'compliant, breach, or warning',
  year INT,
  month INT,
  day INT
)
PARTITIONED BY (year, month, day)
TBLPROPERTIES ('table_type'='ICEBERG');
```

![New table has been created](../source/static/images/FSI-Images/Screenshot%202026-03-13%20at%2012.19.21%E2%80%AFPM.png)


**Business Context:** Risk metrics are essential for financial services operations, providing real-time visibility into portfolio risk exposure, regulatory capital requirements, and compliance status. This table structure captures key metrics for monitoring Value at Risk (VaR), credit exposure, and liquidity risk across the firm's portfolios.

6. In the data panel, expand your s3tablescatalog and s3-table sub catalog. Within your *dev* database confirm you can now see a risk_metrics table.



7. Run the below query in a new SQL cell to load sample risk metrics data into your table. This data represents risk assessments for portfolios managed across the firm's institutional, retail, and wealth management divisions.

```sql
INSERT INTO risk_metrics VALUES
  -- CUST-001 (Alice Johnson) - low risk, all loans current
  (TIMESTAMP '2024-01-15 17:00:00', 'PORT-001', 'CUST-001', 125000.00, 187500.00, 210000.00, 500000.00,  25.0, 15.0, 8.0,  'compliant', 2024, 1, 15),
  (TIMESTAMP '2024-01-22 17:00:00', 'PORT-001', 'CUST-001', 145000.00, 210000.00, 240000.00, 520000.00,  38.0, 22.0, 10.0, 'compliant', 2024, 1, 22),
  (TIMESTAMP '2024-02-05 17:00:00', 'PORT-001', 'CUST-001', 135000.00, 195000.00, 225000.00, 510000.00,  32.0, 18.0, 9.0,  'compliant', 2024, 2, 5),

  -- CUST-002 (Bob Martinez) - LOAN-005 delinquent, risk scores elevated
  (TIMESTAMP '2024-01-15 17:00:00', 'PORT-002', 'CUST-002', 95000.00,  142000.00, 165000.00, 350000.00,  55.0, 40.0, 18.0, 'warning',   2024, 1, 15),
  (TIMESTAMP '2024-01-22 17:00:00', 'PORT-002', 'CUST-002', 140000.00, 210000.00, 245000.00, 380000.00,  78.0, 62.0, 28.0, 'breach',    2024, 1, 22),
  (TIMESTAMP '2024-02-05 17:00:00', 'PORT-002', 'CUST-002', 130000.00, 195000.00, 228000.00, 370000.00,  72.0, 55.0, 25.0, 'breach',    2024, 2, 5),

  -- CUST-003 (Pinnacle Holdings) - medium risk, all loans current
  (TIMESTAMP '2024-01-15 17:00:00', 'PORT-003', 'CUST-003', 850000.00, 1275000.00, 1430000.00, 5000000.00, 42.0, 30.0, 15.0, 'compliant', 2024, 1, 15),
  (TIMESTAMP '2024-01-22 17:00:00', 'PORT-003', 'CUST-003', 1100000.00, 1650000.00, 1850000.00, 5200000.00, 65.0, 48.0, 22.0, 'warning', 2024, 1, 22),
  (TIMESTAMP '2024-02-05 17:00:00', 'PORT-003', 'CUST-003', 980000.00, 1470000.00, 1650000.00, 5100000.00, 58.0, 42.0, 20.0, 'warning', 2024, 2, 5),

  -- CUST-004 (Dragon Capital) - high risk, large institutional
  (TIMESTAMP '2024-01-15 17:00:00', 'PORT-004', 'CUST-004', 1500000.00, 2250000.00, 2520000.00, 15000000.00, 62.0, 45.0, 25.0, 'warning',   2024, 1, 15),
  (TIMESTAMP '2024-01-22 17:00:00', 'PORT-004', 'CUST-004', 2200000.00, 3300000.00, 3700000.00, 16000000.00, 82.0, 68.0, 35.0, 'breach',    2024, 1, 22),
  (TIMESTAMP '2024-02-05 17:00:00', 'PORT-004', 'CUST-004', 1900000.00, 2850000.00, 3200000.00, 15500000.00, 75.0, 58.0, 30.0, 'breach',    2024, 2, 5),

  -- CUST-005 (Sarah Chen) - low risk, current loans
  (TIMESTAMP '2024-01-15 17:00:00', 'PORT-005', 'CUST-005', 80000.00,  120000.00, 135000.00, 300000.00,  20.0, 12.0, 5.0,  'compliant', 2024, 1, 15),
  (TIMESTAMP '2024-01-22 17:00:00', 'PORT-005', 'CUST-005', 95000.00,  142000.00, 160000.00, 320000.00,  35.0, 20.0, 8.0,  'compliant', 2024, 1, 22),
  (TIMESTAMP '2024-02-05 17:00:00', 'PORT-005', 'CUST-005', 88000.00,  132000.00, 148000.00, 310000.00,  28.0, 16.0, 6.0,  'compliant', 2024, 2, 5),

  -- CUST-006 (Meridian Trading) - high risk commercial
  (TIMESTAMP '2024-01-15 17:00:00', 'PORT-006', 'CUST-006', 600000.00, 900000.00, 1010000.00, 8000000.00, 58.0, 42.0, 20.0, 'warning',   2024, 1, 15),
  (TIMESTAMP '2024-01-22 17:00:00', 'PORT-006', 'CUST-006', 920000.00, 1380000.00, 1550000.00, 8500000.00, 85.0, 70.0, 32.0, 'breach',   2024, 1, 22),
  (TIMESTAMP '2024-02-05 17:00:00', 'PORT-006', 'CUST-006', 800000.00, 1200000.00, 1350000.00, 8200000.00, 78.0, 60.0, 28.0, 'breach',   2024, 2, 5),

  -- CUST-007 (James O'Brien) - LOAN-012 default, risk spiked
  (TIMESTAMP '2024-01-15 17:00:00', 'PORT-007', 'CUST-007', 45000.00,  67500.00,  75600.00,  100000.00,  30.0, 18.0, 6.0,  'compliant', 2024, 1, 15),
  (TIMESTAMP '2024-01-22 17:00:00', 'PORT-007', 'CUST-007', 72000.00,  108000.00, 121000.00, 115000.00,  75.0, 58.0, 22.0, 'breach',    2024, 1, 22),
  (TIMESTAMP '2024-02-05 17:00:00', 'PORT-007', 'CUST-007', 68000.00,  102000.00, 114000.00, 112000.00,  82.0, 65.0, 28.0, 'breach',    2024, 2, 5),

  -- CUST-008 (Global Sovereign Fund) - critical risk, very high scores
  (TIMESTAMP '2024-01-15 17:00:00', 'PORT-008', 'CUST-008', 3500000.00, 5250000.00, 5880000.00, 50000000.00, 68.0, 50.0, 30.0, 'warning', 2024, 1, 15),
  (TIMESTAMP '2024-01-22 17:00:00', 'PORT-008', 'CUST-008', 5200000.00, 7800000.00, 8740000.00, 55000000.00, 92.0, 78.0, 42.0, 'breach',  2024, 1, 22),
  (TIMESTAMP '2024-02-05 17:00:00', 'PORT-008', 'CUST-008', 4500000.00, 6750000.00, 7560000.00, 52000000.00, 88.0, 72.0, 38.0, 'breach',  2024, 2, 5),

  -- CUST-010 (Lakewood Industries) - low risk, current loans
  (TIMESTAMP '2024-01-15 17:00:00', 'PORT-010', 'CUST-010', 200000.00, 300000.00, 336000.00, 1200000.00, 22.0, 14.0, 7.0,  'compliant', 2024, 1, 15),
  (TIMESTAMP '2024-01-22 17:00:00', 'PORT-010', 'CUST-010', 250000.00, 375000.00, 420000.00, 1300000.00, 40.0, 25.0, 12.0, 'compliant', 2024, 1, 22),
  (TIMESTAMP '2024-02-08 17:00:00', 'PORT-010', 'CUST-010', 230000.00, 345000.00, 387000.00, 1250000.00, 35.0, 20.0, 10.0, 'compliant', 2024, 2, 8);
```
![risk_metrics records have been created](../source/static/images/FSI-Images/Screenshot%202026-03-13%20at%2012.21.16%E2%80%AFPM.png)

**Business Context:** This risk data covers 9 customers who hold loans in Aurora. Notice how market_risk_score spikes on January 22 (the same date as the market downturn in market_data). Customers with delinquent or defaulting loans — CUST-002 (LOAN-005 delinquent) and CUST-007 (LOAN-012 default) — show risk scores above 70 and compliance status of 'breach', while low-risk customers like CUST-001 and CUST-005 remain 'compliant'. This correlation is what our cross-catalog queries will surface.

8. Run the below query in a new SQL cell to view the contents of the table. 

```sql
SELECT * FROM risk_metrics ORDER BY timestamp, portfolio_id;
```

### Query Your Aurora MySQL Data via Zero-ETL Catalog

The Aurora MySQL data is available through the Zero-ETL integration catalog (`rms-catalog`), which automatically replicates data from your Aurora MySQL cluster into the SageMaker Lakehouse. This means you can query your core banking tables (customers, accounts, transactions, loans) using Athena SQL without any manual ETL pipelines.

1. Navigate to your Amazon SageMaker portal. At the top of the portal, select "Data" from the *Current Project* dropdown

2. In the data panel, under *Lakehouse*, expand the *rms-catalog* catalog and the Zero-ETL sub-catalog. Confirm you can see both your *fsidb* and *filter_missingpk* databases. 

3. Expand the *fsidb* database to review the tables. Select the ellipsis next to the *customers* table and select **preview data**.

![SageMaker Data Catalog showing preview option](../source/static/images/FSI-Images/Screenshot%202026-03-13%20at%201.00.51%E2%80%AFPM.png)

4. You have now been taken into the query editor within SageMaker Unified Studio. The SQL statement will run automatically for you in the first cell. You should get a preview of 10 rows within your *customers* table returned, showing financial services customers including institutional clients, retail banking customers, and wealth management accounts.

### Cross-Catalog Queries

Now let's demonstrate the true power of federated queries by combining data from both catalogs. We'll join S3 tables (market_data, risk_metrics) with Aurora MySQL tables replicated via Zero-ETL (customers, accounts, loans) to answer critical FSI questions that span operational banking data and capital markets risk analytics — all without moving data manually.

These queries reference two catalogs:
- `s3tablescatalog/s3-table` → S3 Tables (market_data, risk_metrics in the `dev` database)
- `rms-catalog/zetl_...` → Aurora MySQL data replicated via Zero-ETL integration (customers, accounts, loans in `fsidb`)

**Use Case 1: Identify At-Risk Borrowers During Market Stress**

1. Run the below query in a new SQL cell. When markets drop, which borrowers are most exposed? This query joins portfolio risk scores from S3 with loan and customer data from Aurora (replicated via Zero-ETL) to surface borrowers whose risk scores breached the 70-point threshold — and flags whether their loans are delinquent or in default.

```sql
SELECT
  c.customer_name,
  c.customer_type,
  l.loan_id,
  l.principal_amount,
  l.status AS loan_status,
  r.market_risk_score,
  r.compliance_status,
  md.instrument_id,
  md.last_price,
  md.open_price,
  ROUND((md.last_price - md.open_price) / md.open_price * 100, 2) AS daily_pct_change
FROM
  "s3tablescatalog/s3-table"."dev".risk_metrics r
  JOIN "rms-catalog/zetl_xxx"."fsidb"."customers" c
    ON c.customer_id = r.customer_id
  JOIN "rms-catalog/zetl_xxx"."fsidb"."accounts" a
    ON c.customer_id = a.customer_id
  JOIN "rms-catalog/zetl_xxx"."fsidb"."loans" l
    ON a.account_id = l.account_id
  JOIN "s3tablescatalog/s3-table"."dev".market_data md
    ON r.year = md.year AND r.month = md.month AND r.day = md.day
WHERE
  r.market_risk_score > 70
  AND md.instrument_id IN ('AAPL', 'MSFT', 'GOOGL')
ORDER BY
  r.market_risk_score DESC;
```
![Cross-catalog query joining S3 risk metrics with Aurora loans](../source/static/images/FSI-Images/Screenshot%202026-03-13%20at%2012.45.12%E2%80%AFPM.png)

**Business Value:** This federated query joins S3 Tables (risk_metrics, market_data) with Aurora MySQL data replicated via Zero-ETL (customers, accounts, loans) in a single statement — no manual ETL pipelines needed. It surfaces borrowers whose portfolios breached risk thresholds during the January 22 market downturn. Notice that CUST-002 (Bob Martinez) has a delinquent personal loan (LOAN-005) and CUST-007 (James O'Brien) has a defaulted loan (LOAN-012), both showing market_risk_scores above 75 and compliance_status of 'breach'. This is exactly the early warning signal a Chief Risk Officer needs.

**Use Case 2: Regulatory Compliance Dashboard — Breach Summary with Loan Exposure**

3. Run the below query in a new SQL cell. Regulators require firms to report aggregate exposure for portfolios in compliance breach. This query summarizes each customer's total loan exposure, number of problem loans, and worst-case Value at Risk — grouped by compliance status — giving the compliance team a single view of the firm's risk posture.

```sql
SELECT
  c.customer_name,
  c.customer_type,
  c.region,
  r.compliance_status,
  r.market_risk_score,
  r.liquidity_risk_score,
  r.concentration_risk_pct,
  COUNT(l.loan_id) AS total_loans,
  SUM(l.principal_amount) AS total_loan_exposure,
  SUM(CASE WHEN l.status IN ('delinquent', 'default') THEN l.principal_amount ELSE 0 END) AS problem_loan_exposure,
  MAX(r.var_99) AS worst_case_var,
  MAX(r.expected_shortfall) AS worst_case_cvar
FROM
  "s3tablescatalog/s3-table"."dev".risk_metrics r
  JOIN "rms-catalog/zetl_xxx"."fsidb"."customers" c
    ON c.customer_id = r.customer_id
  JOIN "rms-catalog/zetl_xxx"."fsidb"."accounts" a
    ON c.customer_id = a.customer_id
  JOIN "rms-catalog/zetl_xxx"."fsidb"."loans" l
    ON a.account_id = l.account_id
WHERE
  r.compliance_status = 'breach'
GROUP BY
  c.customer_name, c.customer_type, c.region,
  r.compliance_status, r.market_risk_score,
  r.liquidity_risk_score, r.concentration_risk_pct
ORDER BY
  total_loan_exposure DESC;
```
![Regulatory compliance breach summary with loan exposure](../source/static/images/FSI-Images/Screenshot%202026-03-13%20at%2012.49.16%E2%80%AFPM.png)

**Business Value:** This query produces a regulatory-ready compliance dashboard by aggregating loan exposure for every customer currently in 'breach' status. The problem_loan_exposure column isolates delinquent and defaulted loans, while worst_case_var and worst_case_cvar provide the tail-risk metrics regulators demand. For example, CUST-008 (Global Sovereign Fund) shows $3.2M in total loan exposure with a VaR-99 of $7.8M — exactly the kind of concentration risk that Basel III capital adequacy reporting requires. This single federated query replaces what would traditionally require multiple ETL jobs and manual data reconciliation.

### Apache Iceberg capabilities

Apache Iceberg provides powerful data management capabilities that are essential for financial services operations, where risk data accuracy and audit trail integrity are critical for regulatory compliance. Let's explore Iceberg's update and time travel features using our risk_metrics data.

1. Run the below SQL query in a new cell to use the `UPDATE` command to correct a risk metric compliance status. Suppose the compliance team has completed their review of PORT-007 (James O'Brien, whose LOAN-012 defaulted) and downgraded the compliance status:

```sql
UPDATE risk_metrics SET compliance_status='warning' WHERE portfolio_id='PORT-007' AND year=2024 AND month=1 AND day=15;
```

**Business Context:** In financial services operations, risk data may need corrections based on updated model outputs, compliance reviews, or regulatory reclassifications. Iceberg's ACID transaction support ensures data consistency during updates, which is critical for maintaining accurate risk reporting.

2. Run the below SQL query in a new cell to verify that the compliance status has changed from 'compliant' to 'warning' for PORT-007 on January 15:

```sql
SELECT * FROM risk_metrics WHERE portfolio_id='PORT-007';
```

![Preview S3 Table data](../source/static/images/FSI-Images/Screenshot%202026-03-13%20at%201.18.16%E2%80%AFPM.png)

3. Run the below SQL query in a new cell to list the table operations performed (i.e., insert and update) and their corresponding snapshot IDs. This demonstrates Iceberg's versioning capabilities, which are crucial for auditing and regulatory compliance in financial services.

```sql
SELECT * FROM "risk_metrics$snapshots";
```

![Preview S3 Table snapshot data](../source/static/images/FSI-Images/Screenshot%202026-03-13%20at%201.18.44%E2%80%AFPM.png)

**Business Context:** Regulatory compliance in financial services requires maintaining complete audit trails of all data changes. Iceberg's snapshot functionality provides a full history of table modifications, enabling compliance reporting, data lineage tracking, and satisfying regulatory requirements such as SOX, Basel III, and MiFID II.

4. To demonstrate Iceberg's time travel capabilities, copy the **snapshot_id** of the append operation that doesn't have a parent_id. This snapshot_id corresponds to the insert operation we performed in above steps. Run the below query in a new SQL cell, replacing `<snapshot_id>` with the actual snapshot ID you copied.

```sql
SELECT * FROM "risk_metrics" FOR VERSION AS OF <snapshot_id>;
```

![Preview S3 Table data](../source/static/images/FSI-Images/Screenshot%202026-03-13%20at%201.23.54%E2%80%AFPM.png)

**Business Value:** Time travel queries allow you to analyze historical risk data at specific points in time. This is invaluable for financial services operations when investigating compliance incidents, validating risk model changes, or performing end-of-day reconciliation. You can query the exact state of your risk metrics before the compliance status update, enabling audit reviews and regulatory reporting with full data provenance.

::alert[**Congratulations!** You have successfully performed cross-catalog queries combining financial services customer data with market and risk analytics, and witnessed Apache Iceberg's powerful capabilities for data versioning and time travel. These features enable financial institutions to build robust data platforms that support portfolio analytics, transaction monitoring, regulatory compliance, and enterprise risk management. You can now proceed to testing your Zero-ETL integration.]{type=success}
