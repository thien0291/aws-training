# SAA-C03 overlap cheat sheet

## Translate a requirement into a data architecture

| Requirement | Candidate design from this training | Ask before choosing |
| --- | --- | --- |
| Durable, large-scale raw/curated data | S3 lake with Parquet/Iceberg tables | What query engine, format, partitions, retention, and governance are needed? |
| SQL analytics over warehouse data | Redshift | Does the workload need warehouse performance or open lake access? |
| Ad hoc SQL over cataloged S3 data | Athena + Glue Data Catalog | Will scan cost and latency meet the requirement? |
| Low-latency event intake | Kinesis Data Streams | How many consumers, how much throughput, and what retention/replay needs? |
| Buffered stream delivery into S3 | Amazon Data Firehose | Is the buffering delay acceptable? |
| Central row/column governance | Lake Formation | Are IAM, storage encryption, and service permissions also configured? |
| Managed operational-to-analytics replication | Zero-ETL integration | What replication lag is tolerable? |
| Query in-place without an analytical copy | Federation | Can the source tolerate and serve the query reliably? |

## Do not overgeneralize from the course

- A SageMaker Lakehouse architecture is one workload pattern, not a substitute for SAA-wide compute, networking, availability, and cost knowledge.
- “One copy” and “one governance layer” describe the target analytical architecture. They do not remove source-system, IAM, network, or backup considerations.
- High performance means meeting a stated latency/throughput requirement; it does not mean always picking Redshift or always picking streaming.
- The official SAA guide includes storage, compute, database, network, resilient design, and cost decisions well beyond this cheat sheet.
