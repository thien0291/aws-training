---
title: "03. Create a zero-ETL integration"
weight: 30
---

In this module, we will navigate through the zero-ETL setup process using the Amazon RDS console. The zero-ETL wizard makes this integration straightforward by automatically configuring essential components, including the required parameter groups for our source Aurora MySQL database and the necessary settings in our destination AWS Glue Data Catalog.

Zero-ETL integration enables financial institutions to replicate core banking data from Aurora MySQL (containing customers, accounts, transactions, and loans) to Amazon Redshift Managed Storage without building custom ETL pipelines. This allows data engineers to combine structured banking data with market data and trade executions for comprehensive real-time analytics. 

### Create a Zero-ETL integration


1. Navigate to the [Amazon RDS and Aurora Console](https://us-east-1.console.aws.amazon.com/rds/home?region=us-east-1), choose **Zero-ETL integrations** from the left navigation pane. Choose the **Create zero-ETL integration** button as shown below.

![rds console zero-etl integration tab](/static/images/Image44.png)

2. Under Step 1: *Getting started*, for your integration identifier, enter an integration name of your choice, for example :code[zero-etl-aurora-mysql-lakehouse]{showCopyAction=true} and choose **Next**.

![zero-etl integration step1](/static/images/ztl_s1lakehouse.png)

3. Under Step 2: *Select source*, select **Browse RDS databases** and choose the source Aurora MySQL cluster named *zetlsagemaker*. 

![zero-etl integration step2 choose](/static/images/db.png)

4. Check the "Customize data filtering options" checkbox under **Data filtering options** and complete the below actions:
* For **Include** filter type, use :code[*.*]{showCopyAction=true} as the filter expression to replicate all FSI operational data. 
* Click the **Add Filter** button to add an exclusion criteria: :code[filter_missingpk.*]{showCopyAction=true} to exclude the demonstration database that intentionally contains tables without primary keys.

5. Choose **Next**.

![zero-etl integration wizard_datafilter](/static/images/ztl_s2checks.png)

6. Under Step 3: *Select target*, complete the below actions: 
* For AWS account: Choose *Use the current account.* 
* For Target resource type: Choose **AWS Glue Catalog.**
* Within the **AWS Glue catalog** drop down: Choose **rms-catalog** (the catalog you created in Module 02). 
* For **Target IAM role**: Search for and choose **SageMakerNextGenImmersionRole**. 
* Since our target does not have the correct resource policy, we will get an error message along with a *Fix it for me* checkbox. Select the *fix it for me* checkbox

::alert[**Important:** Make sure to select **rms-catalog** from the AWS Glue catalog dropdown. This is the Redshift Managed Storage catalog you created in Module 02. The Zero-ETL integration will automatically create a database within this catalog with a name starting with *zetl_*.]{type=info}

7. Choose **Next**.

![Target in Zero ETL Integration](/static/images/targ.png)

8. On the review pop-up that appears, choose **Continue**.

9. Under Step 4: *Add tags and encryption* (optional), choose **Next**.

![zero-etl integration step4](/static/images/ztl_s4.png)

8. Under Step 5:, *Review and create*, review all fields to ensure pre-requisites are completed before choosing **Create zero-ETL integration**.

![zero-etl integration progress](/static/images/Imagewait.png)


::alert[The zero-ETL integration will take approximately **15-30 minutes** to change from "creating" to "active" status. You may proceed to the next module, Federated Query, while waiting.]{type=info}