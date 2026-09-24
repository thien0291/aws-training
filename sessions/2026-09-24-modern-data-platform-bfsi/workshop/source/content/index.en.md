---
chapter: true
title: "Accelerating Financial Analytics: Lakehouse, Amazon SageMaker Unified Studio & Amazon Quick"
weight: 1
---

In this workshop, use generative AI to revolutionize how business users access financial data — no SQL required. Explore an end-to-end process for breaking down data silos using Zero-ETL integrations from Aurora to  Amazon Redshift, unifying financial data through a lakehouse architecture on Amazon S3, and building a conversational analytics layer powered by Amazon Quick.

### What to expect from this workshop?

By the end of this workshop, you will learn how to break down financial data silos using **Zero-ETL integrations** from Aurora MySQL to Amazon Redshift, unify structured and unstructured financial data through a **lakehouse architecture** on Amazon S3, and build a **conversational analytics layer** powered by Amazon Quick — enabling business users to ask questions in natural language without writing SQL.

The workshop demonstrates real-world financial services use cases including:

- **Zero-ETL Data Integration**: Automatically replicate core banking data from Aurora MySQL to Amazon Redshift without building ETL pipelines
- **Lakehouse Architecture**: Unify structured banking data with market data and risk metrics using S3 Tables with Apache Iceberg
- **Federated Queries**: Query across multiple data catalogs and storage systems using standard SQL
- **Conversational Analytics**: Enable business users to explore financial data using natural language through Amazon Quick

The workshop contains modules that must be completed in the order shown in the left navigation menu, as each module builds upon the previous one. Your workshop accounts come with **pre-created resources**, including an **Aurora MySQL database** with financial services enterprise data and an **Amazon SageMaker domain**.


## Target Audience

Below are the personas who can directly benefit from this workshop:

1. **CFO/Finance Executives** - Leverage unified analytics for financial oversight, strategic decision-making, and performance monitoring across business lines
2. **Risk Officers** - Monitor portfolio risk exposure, credit risk, and market risk using integrated data from core banking and trading systems
3. **Compliance Officers** - Ensure regulatory compliance by querying transaction data, audit trails, and compliance alerts across multiple data sources
4. **Financial Data Engineers** - Design unified data platforms that integrate core banking systems with trading and risk management data

## How Zero-ETL and Federated Queries Solve Financial Services Challenges

Financial institutions face unique data integration challenges that traditional ETL approaches struggle to address:

### The Challenge: Fragmented Data Landscape

Financial institutions operate with data scattered across multiple systems:
- **Core Banking Systems**: Customer accounts, transactions, loans, and employee records stored in operational databases with strict transactional requirements
- **Trading & Market Data**: Real-time trade executions, market data snapshots, and instrument pricing across equities, bonds, FX, and derivatives
- **Risk & Compliance Platforms**: Portfolio risk metrics, compliance alerts, regulatory reporting data, and audit trails requiring cross-system correlation

Traditional approaches require building and maintaining complex ETL pipelines to move data between these systems, leading to:
- **Fragmented Banking Systems**: Analytics teams can't easily access data across core banking, trading, and risk platforms
- **Delayed Risk Reporting**: ETL pipelines introduce latency between data generation and risk analysis, impacting timely decision-making
- **Regulatory Data Silos**: Compliance teams struggle to generate comprehensive regulatory reports when data is scattered across systems
- **Limited Agility**: Adding new data sources requires significant engineering effort

### The Solution: Zero-ETL Integration and Federated Queries

This workshop demonstrates how AWS services eliminate these challenges:

**Zero-ETL Integration** automatically replicates data from Aurora MySQL to Amazon Redshift Managed Storage without writing custom ETL code. This enables:
- Real-time data availability for analytics without impacting operational databases
- Automatic schema evolution handling as your data models change
- Reduced engineering overhead by eliminating custom pipeline maintenance

**Glue Catalog Federation** enables querying data across multiple catalogs and storage systems using standard SQL. This allows you to:
- Join structured core banking data (Aurora MySQL) with trading and market data (S3 Tables with Apache Iceberg)
- Query data where it lives without moving or copying it
- Use familiar SQL syntax to access diverse data sources through a single interface

**S3 Tables with Apache Iceberg** provides a high-performance table format for querying trading and market data in S3:
- Query trade executions, market data, and risk metrics using SQL without data transformation
- Leverage partitioning for efficient queries over time-series financial data
- Support schema evolution as financial data models change

### Workshop Objectives

By completing this workshop, you will:

1. **Build a Unified Financial Data Platform**: Create a lakehouse architecture that integrates core banking data with trading and risk management systems
2. **Implement Zero-ETL Pipelines**: Set up automatic data replication from Aurora MySQL to Redshift Managed Storage
3. **Execute Federated Queries**: Write SQL queries that join data across Aurora MySQL and S3 Tables
4. **Analyze Real-World FSI Use Cases**: Explore transaction monitoring, portfolio risk analytics, and regulatory compliance scenarios
5. **Accelerate Time to Insights**: Learn techniques to reduce the time from data generation to actionable financial insights

### Workshop Modules

This workshop consists of 7 modules that must be completed in order:

**Module 00: Introduction** - Workshop overview and objectives

**Module 01: Setup** - Configure your AWS environment and SageMaker domain

**Module 02: Create Catalog** - Set up data catalogs and connections to Aurora MySQL

**Module 03: Create Zero-ETL Integration** - Configure automatic data replication from Aurora to Redshift

**Module 04: Data Federation** - Execute federated queries joining Aurora and S3 Tables data

**Module 05: Zero-ETL Validation** - Verify data replication and query replicated data

**Module 06: Natural Language Data Analysis with Amazon Quick** - Enable business users to analyze data using conversational AI without SQL

**Workshop Summary** - Review what you've learned and explore next steps


### Workshop Architecture

The diagram below shows the complete end-to-end architecture for this workshop, including data sources, Zero-ETL integration, catalog federation, and analytics layer.

![Architecture diagram showing end-to-end integration](/static/images/Architecture.png)

**Architecture Components:**

**1. Data Sources Layer**
- **Aurora MySQL**: Core banking operational data (fsidb database with 5 tables: customers, accounts, transactions, employees, loans)
- **Amazon S3**: Trading and market data (trade executions, market data snapshots, risk metrics)

**2. Unified Platform (Amazon SageMaker Unified Studio)**
- Single workspace for data, analytics, and AI workflows
- Data connections to Aurora and S3
- Query editor for SQL interface
- IAM integration for secure access

**3. Catalog Layer**
- **AWS Glue Catalog**: Metadata for Aurora MySQL tables (schema, relationships, foreign keys)
- **SageMaker Catalog**: Metadata for S3 Tables (Apache Iceberg format, partitions, schema evolution)
- **Catalog Federation**: Unified metadata access enabling cross-catalog queries

**4. Zero-ETL Integration**
- Automatic replication: Aurora MySQL → Amazon Redshift Managed Storage
- No custom ETL code required
- Near real-time data availability
- Automatic schema evolution handling

**5. Analytics Layer**
- **Amazon Redshift**: Replicated enterprise data (zetl_* database) optimized for analytics
- **S3 Tables with Apache Iceberg**: SQL queries on trading and market data with ACID transactions
- **Federated Queries**: Join data across Aurora, S3, and Redshift without data movement

**6. Agentic AI Interface**
- **Amazon Quick**: Conversational AI workspace for data analysis
- **Natural Language Understanding**: Ask questions in plain English
- **Automated Insights**: AI-powered analysis and recommendations


