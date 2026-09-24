# DEA-C01 session practice test

These eight questions are original, based on the NovaBanco training. They focus on the part of DEA-C01 covered by this session; they are not AWS exam questions. Choose one answer unless stated otherwise.

## Questions

**1.** NovaBanco lands Parquet files in S3. Analysts need to discover their schemas and query them in Athena without manually defining every new table. What should the team add?

- A. An AWS Glue ETL job that runs whenever an analyst opens Athena
- B. An AWS Glue crawler and the Glue Data Catalog
- C. Only a SageMaker business glossary entry for each file
- D. An S3 lifecycle rule to transition the files

**2.** Transaction events must be ingested continuously and delivered to S3 in buffered batches with minimal custom delivery code. Which pairing matches the course design?

- A. Kinesis Data Streams for ingestion and Amazon Data Firehose for S3 delivery
- B. Amazon EventBridge for ingestion and a Glue crawler for delivery
- C. An AWS Glue crawler for ingestion and Athena for delivery
- D. Amazon Redshift for ingestion and Lake Formation for delivery

**3.** The curated transactions table needs transactional writes, schema evolution, and historical snapshots. Which table format is used in the course?

- A. Plain Parquet files registered as a nontransactional external table
- B. Apache Iceberg
- C. An Athena view over raw JSON files
- D. An S3 prefix alone

**4.** An analyst should query customer counts but should not see `national_id` or `email`. Compliance must see those columns. The same governed table is used by both. What is the course's main access-control mechanism?

- A. Use an S3 bucket policy alone, without data-level filters
- B. Apply QuickSight row-level security only, even for Athena users
- C. Apply Lake Formation column-level grants/filters
- D. Use a KMS key policy to hide specific columns inside a table

**5.** A team wants to query a source where it already lives, without first copying it into the lakehouse. Which pattern best matches?

- A. Zero-ETL replication
- B. Federated query
- C. AWS DMS replication
- D. Firehose delivery into S3

**6.** Frequent writes leave an Iceberg table with many small files and slow scans. What is the most direct maintenance action in the Athena demo?

- A. `OPTIMIZE ... REWRITE DATA USING BIN_PACK`
- B. Run `VACUUM` alone without combining active small files
- C. Re-run a Glue crawler without changing the files
- D. Add a high-cardinality partition on customer ID

**7.** A regulator asks which version of the curated data produced a report. What should the engineer retain or record to support reproducibility?

- A. Only the SQL text of the current query
- B. The relevant Iceberg snapshot/version and lineage
- C. Only the present table schema
- D. Only the latest S3 object timestamp

**8.** A DynamoDB-to-lakehouse Zero-ETL integration is configured. The team writes a new item and immediately queries the analytics table. Which expectation is safest?

- A. The query must show it in the same millisecond
- B. The integration always refreshes only once each night
- C. The analytical copy can lag the source; check the integration's freshness behavior
- D. S3 versioning guarantees the new item appears immediately

## Answers and why

1. **B.** A crawler infers schema and registers tables in the technical catalog. [Phase 1, step 1.2](../../sessions/2026-09-24-modern-data-platform-bfsi/source/docs/phase1.md#step-12--make-the-data-discoverable-with-the-glue-catalog).
2. **A.** The demo uses a stream for ingestion and Firehose for buffered S3 delivery. [Phase 1, step 1.5](../../sessions/2026-09-24-modern-data-platform-bfsi/source/docs/phase1.md#step-15--real-time-streaming).
3. **B.** Iceberg adds the requested table semantics. [Phase 1, step 1.4](../../sessions/2026-09-24-modern-data-platform-bfsi/source/docs/phase1.md#step-14--build-the-curated-layer-with-glue-etl).
4. **C.** Lake Formation governs column visibility by persona. [Phase 1, step 1.3](../../sessions/2026-09-24-modern-data-platform-bfsi/source/docs/phase1.md#step-13--govern-access-with-lake-formation).
5. **B.** Federation queries data in place; Zero-ETL moves/replicates data into an analytics target. [Module 2, slides 24–25](../../sessions/2026-09-24-modern-data-platform-bfsi/slides/module-2.md#slide-24).
6. **A.** The Athena demo's `OPTIMIZE` compacts small files. [Phase 2, step 2.5](../../sessions/2026-09-24-modern-data-platform-bfsi/source/docs/phase2.md#step-25--iceberg-maintenance).
7. **B.** A retained snapshot identifies a table state, while lineage records its inputs and transformations. [Phase 3, step 3.3](../../sessions/2026-09-24-modern-data-platform-bfsi/source/docs/phase3.md#step-33--use-case-2-regulatory-compliance).
8. **C.** Managed replication has lag; the demo describes an approximately 15-minute cadence for this source. [Phase 2, step 2.3](../../sessions/2026-09-24-modern-data-platform-bfsi/source/docs/phase2.md#step-23--zero-etl-from-dynamodb).
