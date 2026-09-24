# SAA-C03 flashcards from this session

## Fronts

1. What makes S3 a good base for a data lake, and what does S3 alone not provide?
2. When does Athena fit better than a dedicated warehouse in this course?
3. When does Redshift fit better than S3/Athena alone?
4. What is the role of the Glue Data Catalog in an S3 analytics design?
5. What is the key difference between Kinesis Data Streams and Data Firehose in the demo?
6. How can one table serve analysts and compliance with different data visibility?
7. What is the key tradeoff between Zero-ETL replication and federated query?
8. Why can small Iceberg files make a design slower despite scalable S3 storage?
9. What course pattern separates real-time fraud decisions from historical BI?
10. What major SAA architectural areas would you still need to study after this session?

## Backs

1. S3 offers durable, scalable object storage; the design still needs cataloging, query/processing, access controls, and lifecycle choices.
2. For SQL exploration of cataloged data in S3 when its scan economics and latency are acceptable.
3. For SQL-oriented warehouse analytics when that serving/performance model better fits the workload.
4. It stores technical metadata so engines can find and interpret S3-backed tables.
5. Data Streams accepts and retains stream records for consumers; Firehose buffers and delivers records to S3 in this course.
6. Lake Formation row/column permissions can restrict each persona while they use one underlying table.
7. Zero-ETL moves/replicates data with lag; federation leaves data at its source and queries it there.
8. Many small files increase metadata and per-file overhead; compaction can improve scans.
9. Stream → enrichment/scoring/alerting handles immediate decisions; curated S3 tables and BI handle later analysis.
10. VPC networking, compute and scaling, highly available application design, disaster recovery, other storage types, and broad cost optimization.
