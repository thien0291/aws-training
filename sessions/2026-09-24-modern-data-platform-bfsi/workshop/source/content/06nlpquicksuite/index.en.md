---
title: "06. Natural Language Data Analysis with Amazon Quick"
weight: 65
---

In this module, we will explore Amazon Quick, AWS's AI-powered digital workspace that enables business users to analyze financial services data using natural language—generating graphs, charts, insights, and automated workflows without requiring SQL or technical expertise

Amazon Quick is designed to empower any user, regardless of their role or technical expertise, to access instant answers by conversing naturally with their data—making it equally valuable for C-suite executives, analysts, and everyday business users

## What is Amazon Quick?

Amazon Quick is an agentic AI-powered workspace that:
- Answers questions using natural language conversations
- Analyzes data from databases, data warehouses, documents, and applications
- Generates insights with contextual understanding of your business
- Automates workflows from simple tasks to complex processes
- Searches across enterprise data and the web simultaneously
- Creates visualizations, reports, and summaries automatically

Unlike traditional BI tools, Amazon Quick is conversational and proactive—it's like having an AI data analyst on your team.

## Prerequisites

Before starting this module, ensure you have have completed all prior labs in this workshop to load data into Amazon S3 tables and in Amazon Redshift (RMS catalog) using Zero-ETL integration from Amazon Aurora mySQL.

## Setup Amazon Quick

::alert[**Note:** Amazon Quick is currently available in US East (N. Virginia) and US West (Oregon) regions. Ensure your Redshift cluster and data are in a supported region.]{type=info}

If you are conducting these lab as part of an AWS-Sponsored Immersion Day, a Quick lab account has been created with the required resources. Execute the following steps to complete the setup:

1. In the [AWS console](https://us-east-1.console.aws.amazon.com/console/home), type **Amazon Quick** as illustrated in the screenshot below

![Amazon Quick Home](/static/images/FSI-Images/Lab6-Quick1.png)

2. Once the Amazon Quick Suite console opens, click the **Manage Users** option, as illustrated in the screenshot below

![Amazon Quick Home](/static/images/FSI-Images/Lab6-Quick2.png)

3. From the options menu, select **Manage Role Groups**

![Amazon Quick Home](/static/images/FSI-Images/Lab6-Quick3.png)

4. Choose the **Add Admin Pro Group** option and add `anycompany-Salesmarketing` to the group list, as displayed below.

![Amazon Quick Home](/static/images/FSI-Images/Lab6-Quick5.png)

## Connect Amazon Quick to Your Financial Services Data

1. Connect to SageMaker Unified Studio using the **dg-corp-admin** user credentials with the password you created. Then, click on the **AnyCompany SM Unified Data AI** project, and under the **Actions menu**, choose **Open Quick Suite** as shown below

![Amazon Quick Home](/static/images/FSI-Images/Lab6-Quick7.png)

2. Amazon Quick Suite supports connectivity to multiple data sources. With Quick Suite access setup from Amazon SageMaker directly, you will have all the available datasets from SageMaker shared with Quick Suite automatically. We will select the data asset **project.athena-datasource** to leverage data from S3 Tables, along with the data replicated into the RMS catalog through Zero ETL.

![Amazon Quick Home](/static/images/FSI-Images/Lab6-Quick8.png)

3. Choose **Create dataset** as shown below

![Amazon Quick Home](/static/images/FSI-Images/Lab6-Quick9.png)

4. We will use the **Custom SQL** capability of Quick Suite for connecting to the source data:

![Amazon Quick Home](/static/images/FSI-Images/Lab6-Quick10.png)

5. For the custom SQL, we will use the below SQL. Before using the SQL, substitute **your_catalog_details** value with your Zero-ETL RMS catalog.

::alert[You can find your Zero-ETL RMS catalog name in your Amazon SageMaker project. Go to **Data** and expand **Lakehouse**. Then expand **rms-catalog** and select the catalog name starting with `zetl_`. Copy the catalog name and replace the value in the below SQL.]{type=info}

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
  JOIN "rms-catalog/<your_catalog_details>"."fsidb"."customers" c
    ON c.customer_id = r.customer_id
  JOIN "rms-catalog/<your_catalog_details>"."fsidb"."accounts" a
    ON c.customer_id = a.customer_id
  JOIN "rms-catalog/<your_catalog_details>"."fsidb"."loans" l
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

7. Enter the SQL in the **Custom SQL** field in Quick Suite, rename the SQL to :code[RiskMetrics_Custom_SQL]{showCopyAction=true}, and select **Confirm query**.

![Add Custom SQL](/static/images/FSI-Images/Lab6-Quick-01-Add-Custom-SQL-RiskMetrics.png)

8. In the pop-up to **Finish dataset creation**, select **Directly query your data** and select **Visualize**.

![Add Custom SQL](/static/images/FSI-Images/Lab6-Quick-02-Select-Direct-Query.png)

Selecting visualize option will redirect you to the **Analyses** feature of **Quick Sight**. 

**Analyses** feature in Quick Sight allows users to create visualization, by selecting the relevant data fields, or dragging the fields directly on to the visual canvas, or a combination of both actions. This allows users to build visuals to showcase relevant Business Key Performance Indicators (KPI) across attributes.

9. On being redirected to the **Analyses** console, if a pop-up shows up for **New sheet**, select **Create**.

10. Then, on the left pane for **Visuals**, choose the **Vertical bar chart** icon.

![Select Visual](/static/images/FSI-Images/Lab6-Quick-04-Select-visual.png)

11. From the **Fields** list pane, drag dimension `customer_type` to the X-axis field.

12. Next, drag `market_risk_score` to the value field. The default aggregation applied will be `Sum`. To change that, select the ellipsis next to the field and under **Aggregate**, select `Average`.

![Select average](/static/images/FSI-Images/Lab6-Quick-05-Select-average-marketriskscore.png)

13. Drag and drop `region` under **Group/Color**. Once the query executes in the backend, you will see the below visual being created.

![Show Visual](/static/images/FSI-Images/Lab6-Quick-06-Visual-created.png)

14. Next, to create a [Quick Sight Topics](https://docs.aws.amazon.com/quick/latest/userguide/topics.html) for the dataset, select **Manage Q&A** from the top right of the screen. 

15. Select the option to **Use a linked topic for Build visual and Q&A** and from the dropdown, select **Create Topic**

![Select create topic](/static/images/FSI-Images/Lab6-Quick-09-Select-create-topic.png)

16. In the screen for **New Topic**, for **Topic name** add :code[Risk_Metrics]{showCopyAction=true} and select **Apply changes**.

![Rename Topic](/static/images/FSI-Images/Lab6-Quick-11-Name-topic.png)

17. As the topic gets created, a notification will show on the **Analyses** console - `Preparing Risk_Metrics`.

18. Next, to publish the dashboard, from the top right corner, select **Publish**.

19. In the **Publish dashboard** screen, for **Dashboard name** add :code[RiskMetrics_Dashboard]{showCopyAction=true}. Keep the rest of the default settings. Ensure that **Allow Data Q&A** is enabled with the topic `Risk_Metrics` selected as the **Source** and choose **Publish dashboard**.

![Publish Dashboard](/static/images/FSI-Images/Lab6-Quick-13-Publish-Dashboard.png)

20. Your `RiskMetrics_Dashboard` dashboard will be successfully created and you will be redirected to the newly created **Dashboard**.

## Connect Amazon Quick to Your Financial Services Data

In the next 3 sections, we will use the following AI-powered natural language processing features to interact with and generate responses from the dataset:

  6.1 . [Perform Dashboard Q&A in Quick Sight](/06nlpquicksuite/06-01-dashboard-q-a)

  6.2. [Create and use Quick Suite Spaces with default chat agent](/06nlpquicksuite/06-02-default-chat-agent)

  6.3. [Build a personalized Risk Assessment Chat agent](/06nlpquicksuite/06-03-personalized-chat-optional) (Optional)

::alert[**Congratulations!** You've successfully set up Amazon Quick, created a visual and a linked topic, and published a dashboard. You are now ready to perform natural language querying.]{type=success}