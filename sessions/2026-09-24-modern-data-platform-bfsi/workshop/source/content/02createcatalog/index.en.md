---
title: "02. Create catalogs and connections"
weight: 10
---

In this module, we will explore data cataloging and federated querying capabilities within Amazon SageMaker by creating two managed catalogs and one federated data connection. A data catalog serves as a centralized metadata repository that makes data discoverable and queryable across your organization. Amazon SageMaker supports both managed catalogs, where metadata is stored directly in SageMaker, and federated catalogs, which connect to external metadata sources like AWS Glue.

For our FSI data platform, we need to integrate two types of data:
- **Structured banking data**: Customer accounts, transactions, loans, employee compliance data, and operational metrics stored in Aurora MySQL
- **Trading and risk data**: Trade executions, market data snapshots, and risk metrics stored in S3

By creating these catalogs, financial institutions can unify their operational data sources, enabling risk officers and analysts to perform federated queries that combine real-time trading and market data with historical customer records, transaction histories, and loan performance data. This unified view supports critical use cases such as transaction monitoring, portfolio risk analytics, and regulatory compliance reporting.

In this module we will create:
1. **RMS Catalog**: A managed catalog using Redshift Managed Storage (RMS) to support zero-ETL integration, enabling seamless data replication from Aurora to Redshift for FSI banking data analytics without custom ETL pipelines. This catalog will store replicated customer, account, transaction, employee, and loan data.
2. **S3 Tables Catalog**: A managed catalog utilizing S3 tables for direct querying of trading and market data stored in S3 using Apache Iceberg format. This catalog will enable SQL queries against trade execution, market data, and risk metrics.
3. **Aurora MySQL Connection**: A federated query connection to Aurora MySQL database, enabling direct querying of customer and operational data without data movement. This connection provides real-time access to banking data.

### 1. Create a managed Redshift Managed Storage catalog in Amazon SageMaker

The RMS catalog will serve as the destination for zero-ETL integration, automatically replicating your FSI banking data from Aurora MySQL. This enables high-performance analytics on customer information, account records, financial transactions, and loan metrics without building custom ETL pipelines.

1. Navigate back to your Amazon SageMaker portal. From the top of the portal, choose "Data" from the *Current Project* dropdown.

2. In the data panel, review the current data catalog and choose the **+ Add** button.

![Current project in Amazon Sagemaker](/static/images/currentdata.png)

3. In the pop-up that appears, choose *Create Lakehouse catalog* and complete the below actions:
* Choose *Redshift* as the Source
* Enter :code[rms-catalog]{showCopyAction=true} for the Catalog name
* Choose **Create catalog**.

Back within the data panel, you can now see your catalog being created under the *Lakehouse* catalog. Please note, the catalog creation takes 2-3 minutes. You may proceed to the next step while it builds. 

## 2. Create a managed S3 Table catalog in Amazon SageMaker

The S3 Tables catalog enables direct SQL querying of trading and market data stored in S3. Using Apache Iceberg table format, you can query trade executions, market data snapshots, and risk metrics without moving or transforming the data.

1. Within your data panel, choose the **+ Add** button.

2. In the pop-up that appears, choose *Create Lakehouse catalog* and complete the below actions:
* Choose *S3 Tables* as the Source
* Enter :code[s3-table]{showCopyAction=true} for the Catalog name
* Enter :code[dev]{showCopyAction=true} for the Database name
* Select the checkbox acknowledging S3 Table integration will be enabled.
* Choose **Create catalog**.

Back within the data panel, you can now see your catalog being created under the *Lakehouse* catalog. Please note, the catalog creation takes 2-3 minutes. You may proceed to the next step while it builds. 

### 3. Create a connection in Amazon SageMaker

The Aurora MySQL connection provides federated query access to your FSI banking database. This connection enables you to query the `fsidb` database containing customers, accounts, transactions, employee data, and loans information directly from SageMaker without data replication.

1. Within your data panel, choose the **+ Add** button.

2. In the pop-up that appears, choose *Add connection*, select *Aurora MySQL* as your data connection type and choose **Next**.

3. On the *Add data* page, complete the below actions:
* Enter :code[aurora-mysql]{showCopyAction=true} for the name
* Enter your pre-created Aurora MySQL endpoint by navgiating to the [Amazon RDS and Aurora Console](https://us-east-1.console.aws.amazon.com/rds/home?region=us-east-1) and copying down your Aurora Mysql writer endpoint named *zetlsagemaker-*
* Enter :code[3306]{showCopyAction=true} for the Port
* Enter :code[fsidb]{showCopyAction=true} for the Database (this is the database containing your FSI banking data including customers, accounts, transactions, employees, and loans tables)
* Enter :code[awsuser]{showCopyAction=true} for the Username
* Enter :code[Awsuser123]{showCopyAction=true} for the Password

4. Your settings should look similar to the below screenshot. Once you have reviewed it, choose **Add data**.

![image shows adding aurora mysql as a federated data source](/static/images/FSI-Images/Screenshot%202026-03-10%20at%207.37.38 PM.png)

Back within the data panel, you can now see your connection being created under the *Lakehouse* catalog. Please note, this creation takes 2-5 minutes. You may proceed to the next step while it builds. 

### 4. Grant permissions to your rms-catalog managed catalog

To enable querying of your FSI banking data through the RMS catalog, you need to configure Lake Formation permissions. This ensures that SageMaker can access the replicated customer, account, transaction, employee, and loan data.

1. In a separate tab, navigate to [AWS Lake Formation.](https://us-east-1.console.aws.amazon.com/lakeformation/home?region=us-east-1)

2. In the left navigation menu, choose *Administrative roles and tasks*. 

3. In the *Data lake administrators* box, choose **Add**. 

![Adding admins](/static/images/lf.png)

4. Set Access type as *Data lake administrator* and use the drop down to search for and choose, :code[WSParticipantRole] before choosing **Confirm**. 

5. Once completed, you should now see four data lake administrators within your Lake Formation envrionment, similar to the below screenshot. 

![image shows lake formation adding AWSServiceRoleForRedshift as a read only admin](/static/images/admins.png)

6. Choose *Catalogs* from the left navigation menu and choose your newly created catalog, *rms-catalog*. 
**Note: If you do not see the catalog on the menu then please hit the refresh button.**

7. Switch to the "Permissions" tab and choose the **Grant** button.

![image shows Lake Formation granting permissions to the catalog.](/static/images/grantp.png)

8. In the *Grant permissions* page, complete the below:
* Under Principal type, leave *Principals* selected
* Under Principals, search for and choose, *SageMakerNextGenImmersionRole* as well as the role beginning with, *datazone_usr_role_*
* Under LF-Tags or catalog resources, choose *Named Data Catalog resources* and in the catalogs dropdown, select the checkbox next to your *rms-catalog* catalog
* Under Catalog permissions, select the checkbox next to *Super user*
* Choose the **Grant** button.

![image shows Lake Formation granting permissions to the catalog.](/static/images/permissionsoncatalog.png)



Your Lake Formation Data permissions should now look similar to the below screenshot.

![image shows Lake Formation final permissions on the catalog](/static/images/updated.png)

::alert[Congratulations! You have successfully created your catalog in Amazon SageMaker and granted the necessary permissions. You can now proceed to create your Zero-ETL integration.]{header="Success!" type="success"}

[def]: static/images/FSI-Images/