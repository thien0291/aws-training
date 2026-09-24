# DEA-C01 overlap cheat sheet

## Choose the data path

| Need | Start with | Why / constraint |
| --- | --- | --- |
| Keep raw batch files cheaply | S3 raw zone | Preserve source data; catalog it separately. |
| Analyze columns over large files | Parquet plus appropriate partitions | Column pruning and partition pruning reduce scan work. |
| Discover S3 tables by schema | Glue crawler and Data Catalog | Catalog metadata describes files; it is not the files. |
| Clean and structure raw records | Glue ETL → curated Iceberg | Repeatable transformation plus transactional table features. |
| Capture a real-time event stream | Kinesis Data Streams | Consumers can process stream records; Firehose can deliver buffered records to S3. |
| Query lake data with SQL | Athena | SQL on cataloged S3 data, including Iceberg tables in the demo. |
| Serve warehouse analytics | Redshift | SQL-oriented analytics storage and processing. |
| Read remote data without copying it | Federated query | Source stays in place; source performance and availability still matter. |
| Replicate operational data into analytics storage | Zero-ETL integration | AWS manages data movement; freshness depends on the source/integration. |
| Restrict PII by persona | Lake Formation grants/filters | Define table/column/row permissions; still understand the underlying IAM and encryption layers. |

## Remember the boundaries

- S3 object data, Glue catalog metadata, and SageMaker business catalog descriptions solve different problems.
- Iceberg snapshots enable history only while the required snapshots/files are retained; expiration reduces the window for time travel.
- Compaction improves read performance by combining small files. It is not the same as partitioning or schema evolution.
- A data stream and a delivery service are separate: Kinesis Data Streams ingests records; Data Firehose buffers and writes them to a destination in the course demo.
- A Lake Formation grant is for governed data access. IAM permissions, KMS keys, and S3 policies still matter in a full solution.

## Beyond this session

Practice end-to-end scenarios with failure handling, retries/replay, orchestration, data quality, monitoring, encryption, and cost tuning. The [DEA-C01 guide](https://docs.aws.amazon.com/aws-certification/latest/data-engineer-associate-01/data-engineer-associate-01.html) has the full scope.
