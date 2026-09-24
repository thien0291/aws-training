---
title: "05. Zero-ETL Query"
weight: 50
---

::alert[**Welcome back!** Before you can complete this lab, ensure your Zero-ETL integration status has changed from **Creating** to **Active** before proceeding.]{type=info}

::alert[**Common Issue - Permissions Error:** Many users encounter a permissions error when querying Zero-ETL tables. If you see `GENERIC_INTERNAL_ERROR: Forbidden` with `glue:GetTable`, follow the [Quick Fix Guide](../source/static/LAB05_PERMISSIONS_QUICK_FIX.md) (5 minutes) or use the [automated CLI script](../source/static/fix_glue_permissions_cli.sh). See the [detailed troubleshooting guide](troubleshooting-unavailable.md) for more information.]{type=warning}

We will now validate that our initial data seeding was successful and confirm that the tables lacking primary keys were correctly filtered out as intended. After that, we will explore near real-time CDC by connecting, creating, and loading additional financial services data into our tables. All changes made to our source will sync almost immediately through the active Zero-ETL integration. 


### Validate fsidb

1. Within your SageMaker portal, from the top navigation, select *Build* and then select *Query Editor*.

![SageMaker Query Editor](../source/static/images/FSI-Images/Screenshot%202026-03-13%20at%203.46.06%E2%80%AFPM.png)

2. Change your connection type by clicking the "Connections" box (top right corner) and completing the following actions:
* Under Connections, select *Athena (Lakehouse)*
* Under Catalogs, select *rms-catalog*
* Under Databases, select the database beginning with *zetl_* (e.g., zetl_bdb1cad7-afba-43be-915d-96afb0cd7829)
* Under Schema, select *fsidb*

::alert[**Troubleshooting:** If you don't see the *rms-catalog* in the Catalogs dropdown or the *zetl_* database, ensure your Zero-ETL integration status is **Active** (not Creating). The catalog and database are created automatically by the Zero-ETL integration. If the integration is Active but you still don't see the catalog, try refreshing the page or check the [Troubleshooting Guide](troubleshooting-unavailable.md).]{type=warning}


3. Explore the schemas in the left hand *data explorer* panel by expanding the *rms-catalog* catalog, then expanding the database beginning with *zetl_* (the full database name will be something like zetl_c715089d-d521-4e3f-9b5a-11f834bc1182), and then expanding the *fsidb* schema. You should see that our five tables from the previous module have all been loaded. 

![SageMaker Query Editor](../source/static/images/FSI-Images/Screenshot%202026-03-13%20at%203.35.58%E2%80%AFPM.png)

4. Within your *data explorer* panel, click the ellipsis next to the *customers* table and select *preview*. Once the query is completed you should see multiple rows of customer data returned. 

::alert[**Troubleshooting Permissions Error:** If you receive a `GENERIC_INTERNAL_ERROR: Forbidden` error stating the user is not authorized to perform `glue:GetTable`, this means the DataZone user role needs additional Glue permissions. Follow the [Quick Fix Guide](../source/static/LAB05_PERMISSIONS_QUICK_FIX.md) (takes 5 minutes) or use the [automated CLI script](../source/static/fix_glue_permissions_cli.sh). See the [detailed fix guide](../source/static/fix_glue_permissions.md) for step-by-step instructions with screenshots.]{type=warning}

5.  Run the below SQL query in a new cell to check the count in a few of the tables. 

```sql
select '1. Customers' as Tablename,count(*) as Count from fsidb.customers union
select '2. Accounts',count(*) from fsidb.accounts union
select '3. Loans', count(*) from fsidb.loans order by 1;
```
![SageMaker Query result ](../source/static/images/FSI-Images/Screenshot%202026-03-13%20at%203.39.33%E2%80%AFPM.png)

You should get a result showing the count of records in each table, confirming that the financial services data has been successfully loaded through the Zero-ETL integration.

### Validate change data capture

One of the benefits of a zero-ETL integration is the instant change data capture that can occur. In this section we are going to validate that our change data capture is working as expected. All changes made to our source will sync almost immediately, with an active zero-ETL integration.

1. Navigate to the [Amazon EC2 Console](https://us-east-1.console.aws.amazon.com/ec2/home?region=us-east-1#Instances:)  from within your AWS console and select the checkbox next to ec2-rds-client and choose **Connect**.
**

![image shows selecting EC2 instance and selecting the connect button](../source/static/images/FSI-Images/Screenshot%202026-03-13%20at%201.46.13%E2%80%AFPM.png)

2. Select the option of Session manager and choose **Connect**.

![image shows Session Manager tab on the connection options for EC2](../source/static/images/FSI-Images/Screenshot%202026-03-13%20at%201.46.51%E2%80%AFPM.png)


3. Copy and run the below command to connect to the Aurora Mysql database from your EC2 instance.

```sql
AURORA_WRITER_ENDPOINT=$(aws rds describe-db-clusters --region us-east-1 --query 'DBClusters[0].Endpoint' --output text)

mysql -h $AURORA_WRITER_ENDPOINT -P 3306 -u awsuser -p 
```

When prompted, enter :code[Awsuser123]{showCopyAction=true} for the password.

![image shows connecting to mysql within an EC2 instance](../source/static/images/FSI-Images/Screenshot%202026-03-13%20at%201.48.19%E2%80%AFPM.png)

4. Once connected to your Aurora Mysql instance, copy and run the below SQL statements to create a new database with two tables for additional financial compliance data.

```sql
create database cdcdemo;

use cdcdemo;

CREATE TABLE compliance_alerts (
  alert_id varchar(50) not null,
  account_id varchar(50) not null,
  alert_type varchar(50) not null,
  created_date date not null,
  review_date date,
  status varchar(20) not null,
  PRIMARY KEY (alert_id)
);

CREATE TABLE transaction_flags (
  flag_id int8 not null AUTO_INCREMENT,
  alert_id varchar(50) not null,
  flag_timestamp timestamp not null,
  flag_amount decimal(15,2) not null,
  flag_reason varchar(100) not null,
  PRIMARY KEY (flag_id)
);

```

5. Run the below SQL statements to insert sample compliance alert and transaction flag data into the newly created tables.

```sql
-- Insert compliance alert data
INSERT INTO compliance_alerts (alert_id, account_id, alert_type, created_date, review_date, status) VALUES
('AML-ALERT-001', 'ACCT-1001', 'suspicious_activity', '2024-01-15', '2024-01-20', 'open'),
('AML-ALERT-002', 'ACCT-1002', 'suspicious_activity', '2024-01-18', '2024-01-25', 'open'),
('KYC-ALERT-001', 'ACCT-1001', 'kyc_expiry', '2024-02-01', '2024-02-10', 'open'),
('KYC-ALERT-002', 'ACCT-1003', 'kyc_expiry', '2024-02-05', '2024-02-15', 'open'),
('TXN-ALERT-001', 'ACCT-1004', 'large_transaction', '2024-02-10', '2024-02-12', 'open'),
('TXN-ALERT-002', 'ACCT-1005', 'large_transaction', '2024-02-12', '2024-02-14', 'open'),
('SAR-ALERT-001', 'ACCT-1002', 'sar_filing', '2024-02-15', '2024-02-20', 'open'),
('SAR-ALERT-002', 'ACCT-1006', 'sar_filing', '2024-02-18', '2024-02-25', 'open'),
('OFAC-ALERT-001', 'ACCT-1007', 'sanctions_screening', '2024-03-01', '2024-03-05', 'open'),
('OFAC-ALERT-002', 'ACCT-1008', 'sanctions_screening', '2024-03-05', '2024-03-10', 'open');

-- Insert transaction flag data
INSERT INTO transaction_flags (alert_id, flag_timestamp, flag_amount, flag_reason) VALUES
('AML-ALERT-001', '2024-01-15 09:30:00', 150000.00, 'Multiple large cash deposits within 24 hours'),
('AML-ALERT-001', '2024-01-15 14:15:00', 95000.00, 'Wire transfer to high-risk jurisdiction'),
('AML-ALERT-001', '2024-01-15 16:45:00', 48500.00, 'Structured deposit below reporting threshold'),
('AML-ALERT-002', '2024-01-18 10:00:00', 250000.00, 'Unusual wire transfer pattern detected'),
('AML-ALERT-002', '2024-01-18 11:30:00', 175000.00, 'Rapid movement of funds across accounts'),
('KYC-ALERT-001', '2024-02-01 08:00:00', 0.00, 'KYC documentation expired - 90 day review'),
('KYC-ALERT-002', '2024-02-05 08:00:00', 0.00, 'KYC documentation expired - annual review'),
('TXN-ALERT-001', '2024-02-10 13:22:00', 500000.00, 'Single transaction exceeds daily threshold'),
('TXN-ALERT-002', '2024-02-12 15:45:00', 750000.00, 'International wire exceeds monitoring limit'),
('SAR-ALERT-001', '2024-02-15 09:00:00', 320000.00, 'Pattern consistent with layering activity'),
('SAR-ALERT-002', '2024-02-18 10:30:00', 185000.00, 'Unusual account activity - dormant account reactivation'),
('OFAC-ALERT-001', '2024-03-01 08:15:00', 45000.00, 'Potential sanctions list match - beneficiary name'),
('OFAC-ALERT-002', '2024-03-05 09:45:00', 62000.00, 'Potential sanctions list match - originator country'),
('AML-ALERT-001', '2024-01-16 08:30:00', 72000.00, 'Follow-up transaction from flagged account'),
('AML-ALERT-002', '2024-01-19 11:00:00', 130000.00, 'Continued unusual transfer pattern'),
('TXN-ALERT-001', '2024-02-11 09:15:00', 425000.00, 'Second large transaction within 48 hours'),
('SAR-ALERT-001', '2024-02-16 14:00:00', 210000.00, 'Additional layering activity detected');

```

6. Let's test if the zero-ETL intergration has loaded the new data. Navigate back to the Query Editor within your open SageMaker Unified Studio Portal and run the below command in a new SQL cell. 

```sql
select '1. customers' as tablename,count(*) from fsidb.customers union
select '2. accounts',count(*) from fsidb.accounts union
select '3. loans', count(*) from fsidb.loans union
select '4. transactions', count(*) from fsidb.transactions union
select '5. employees',count(*) from fsidb.employees union
select '6. compliance_alerts',count(*) from cdcdemo.compliance_alerts union
select '7. transaction_flags',count(*) from cdcdemo.transaction_flags order by 1;
```

This query validates that all financial services tables from both the initial seeding and the newly created CDC demo tables are accessible through the Zero-ETL integration.

7. Run the below SQL statement in a new cell and make a note of the value under *status*. 

```sql
select * from cdcdemo.compliance_alerts where alert_id = 'AML-ALERT-001';
```

8. Navigate back to the EC2 session for your Aurora Mysql instance, execute the below DML command to update the compliance alert status.

```sql
update cdcdemo.compliance_alerts 
set status = 'under_review'
where alert_id = 'AML-ALERT-001';
```

9. Let's test if the zero-ETL intergration has captured the compliance alert status update. Navigate back to the Query Editor within your open SageMaker Unified Studio Portal and run the below command in a new SQL cell. 

```sql
select * from cdcdemo.compliance_alerts where alert_id = 'AML-ALERT-001';
```

You should see that the compliance alert status has been updated to 'under_review', confirming that the change data capture is working correctly through the Zero-ETL integration.

::alert[**Congratulations!** You have successfully validated your zero-ETL integration and confirmed that change data capture is being captured correctly. This completes the workshop, please feel free to continue exploring query capabilities with Unified studio or reach out to your AWS facilitator if you have any questions.]{type=success}
