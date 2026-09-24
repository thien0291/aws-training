# SAA-C03 data-architecture practice test

These six original scenarios practice only the SAA-C03 slice found in this training. They are not AWS-authored or recalled live exam questions. Choose one answer per question.

## Questions

**1.** A bank wants a durable, scalable landing zone for varied raw exports before choosing how analysts will query them. Which storage service from the course is the best starting point?

- A. Amazon S3
- B. Amazon EBS attached to one EC2 instance
- C. Amazon EFS mounted by application servers
- D. Amazon DynamoDB for each raw export file

**2.** A team already stores historical transactions as Iceberg tables in S3. Analysts need occasional SQL queries and accept scan-based latency. What is the simplest query pattern shown in the course?

- A. Provision a new Aurora cluster solely for the occasional scans
- B. Athena querying cataloged S3 tables
- C. Use a Glue crawler alone as the SQL engine
- D. Copy every object to DynamoDB before querying

**3.** A fraud service must process a continuous transaction feed and retain a stream that consumers can read. The same events should later land in S3 for analysis. Which course pairing fits?

- A. Kinesis Data Streams plus Amazon Data Firehose
- B. Data Firehose alone, with no retained stream for independent consumers
- C. S3 Event Notifications plus a Glue crawler
- D. AWS DataSync plus a nightly export

**4.** Analysts should see customer segment but not national ID, while compliance users need both. Which design uses one table and applies data-level least privilege?

- A. Give both groups the same S3 read policy and hide the column in a dashboard
- B. Lake Formation column-level permissions by persona
- C. Use QuickSight row security only, including for Athena access
- D. Use only a KMS key policy to filter table columns

**5.** The operational database must remain the system of record. The analytics team can tolerate replication lag and wants a continuously updated analytical copy without building a custom ETL job. Which integration pattern matches?

- A. Zero-ETL replication into an analytics target
- B. Federated query that leaves all data at the source
- C. A one-time export of the operational data to S3
- D. A Glue crawler that only updates schema metadata

**6.** A lakehouse design has good object-storage scalability but queries slow down as thousands of tiny Iceberg files accumulate. Which change directly addresses that bottleneck?

- A. Compact the data files
- B. Re-run the Glue crawler without rewriting files
- C. Increase Redshift compute for an Athena-on-S3 query
- D. Add CloudFront caching for the Iceberg metadata files

## Answers and why

1. **A.** S3 stores the lake's raw and curated objects; processing, catalog, and access remain separate choices. [Phase 1, step 1.1](../../sessions/2026-09-24-modern-data-platform-bfsi/source/docs/phase1.md#step-11--the-data-lake-zones).
2. **B.** Athena queries the Glue-cataloged S3 data in the course. [Phase 1, step 1.2](../../sessions/2026-09-24-modern-data-platform-bfsi/source/docs/phase1.md#step-12--make-the-data-discoverable-with-the-glue-catalog).
3. **A.** Data Streams is the stream; Firehose delivers buffered events to S3. [Phase 1, step 1.5](../../sessions/2026-09-24-modern-data-platform-bfsi/source/docs/phase1.md#step-15--real-time-streaming).
4. **B.** Lake Formation controls column visibility per persona. IAM and encryption still need correct configuration in the full architecture. [Phase 1, step 1.3](../../sessions/2026-09-24-modern-data-platform-bfsi/source/docs/phase1.md#step-13--govern-access-with-lake-formation).
5. **A.** A managed replication path makes an analytical copy, subject to freshness lag. Federation would query the source in place instead. [Module 2, slides 24–25](../../sessions/2026-09-24-modern-data-platform-bfsi/slides/module-2.md#slide-24).
6. **A.** File compaction reduces the small-file overhead. [Phase 2, step 2.5](../../sessions/2026-09-24-modern-data-platform-bfsi/source/docs/phase2.md#step-25--iceberg-maintenance).

Next, take the [official SAA sample questions](official-practice.md). Most of those test architecture topics this session does not cover.
