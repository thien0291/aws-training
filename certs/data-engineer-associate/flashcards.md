# DEA-C01 flashcards from this session

Try all fronts before reading the backs. Source links are in the [training extract](training-extract.md).

## Fronts

1. What lives in S3, and what lives in the Glue Data Catalog?
2. Why use Parquet and partitions for large analytical tables?
3. What is the difference between the raw and curated lake zones?
4. Which service in the demo infers table schema from S3 files?
5. Why choose Iceberg for curated tables instead of plain files alone?
6. Which component ingests a continuous stream, and which delivers buffered records to S3?
7. When would you choose Zero-ETL replication instead of federated query?
8. What maintenance action addresses too many small Iceberg files?
9. What happens to old time-travel queries after their snapshots are expired?
10. How can two personas see different columns from the same table?
11. What does data lineage answer that a table schema cannot?
12. Why is a business catalog different from a technical table catalog?

## Backs

1. S3 holds objects/data; Glue Data Catalog holds table/schema/partition metadata that engines use to find and interpret them.
2. Parquet is columnar, and suitable partitions let an engine read fewer files/columns for selective queries.
3. Raw preserves landed source data; curated contains cleaned, modeled data ready for trusted reuse.
4. An AWS Glue crawler.
5. Iceberg adds transactional table metadata, snapshots/time travel, and schema/partition evolution.
6. Kinesis Data Streams ingests; Amazon Data Firehose buffers and delivers to S3 in this demo.
7. When a managed analytical copy and repeated low-latency analytics on replicated data are preferable to querying the operational source in place; account for replication lag.
8. Compaction (`OPTIMIZE` in the Athena demo).
9. They can no longer read a snapshot that has been expired and cleaned up.
10. Lake Formation column permissions/filters restrict each persona's visible data.
11. Where the data came from and how it was transformed, so a report can be traced and audited.
12. The technical catalog registers tables and schemas; the business catalog adds meaning, owners, glossary, discovery, and subscription workflows.
