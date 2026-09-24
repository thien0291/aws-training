# ML Engineer Associate session practice test

These six original questions cover the fraud and RAG examples in the training. They are not AWS-authored or live exam questions. Choose one answer per question. Question 6 is particularly relevant to the updated C02 beta.

## Questions

**1.** A fraud model is trained from historical transactions. The team wants a feature that captures unusual transaction frequency. Which course feature is most directly useful?

- A. Count of transactions for an account in the previous hour
- B. Number of Kinesis shards carrying all customers' events
- C. An account's lifetime transaction total with no time window
- D. The average size of the Parquet objects in S3

**2.** The team trains on a field called `total_amount_24h`. The online scoring service instead calculates amount over seven days. What is the main ML risk?

- A. No risk if both columns have numeric values
- B. Training-serving feature mismatch
- C. A label-leakage problem caused only by table encryption
- D. A model-registry version mismatch that fixes itself at inference

**3.** Transactions must receive a fraud score during the live event path. Which course component hosts the deployed scoring model?

- A. An AWS Glue crawler
- B. SageMaker AI inference endpoint
- C. A SageMaker business glossary entry
- D. A SageMaker model-registry record without a deployment

**4.** Customer risk context arrives in the lakehouse from DynamoDB through Zero-ETL with a refresh delay. The fraud decision has a tight latency/freshness requirement. What should the team verify first?

- A. That the feature's replication lag is acceptable for live scoring
- B. That the offline model used the largest possible instance
- C. That the business glossary contains a fraud term
- D. That every Iceberg snapshot is kept forever

**5.** The fraud team needs transaction patterns but should not read customer national IDs. Which course control supports this separation?

- A. A common S3 read policy for all analysts
- B. Lake Formation column-level permissions
- C. A KMS key policy alone, without a data-level filter
- D. More Kinesis shards to separate customer identities

**6. (C02-oriented)** A RAG pipeline processes financial filings. To help users trace an answer to the filing that supplied it, what should be attached to chunks?

- A. Source identifiers and relevant document metadata
- B. Larger chunks with no source identifiers
- C. Only the generation model's temperature
- D. More embedding dimensions but no source identifiers

## Answers and why

1. **A.** The demo's one-hour count is a transaction-velocity feature. [Phase 3, step 3.2](../../sessions/2026-09-24-modern-data-platform-bfsi/source/docs/phase3.md#step-32--use-case-1-real-time-fraud-detection).
2. **B.** A different aggregation window changes what the model receives. Matching offline and online feature semantics is an ML-engineering extension of the demo's feature definition. [Phase 3, step 3.2](../../sessions/2026-09-24-modern-data-platform-bfsi/source/docs/phase3.md#step-32--use-case-1-real-time-fraud-detection).
3. **B.** The endpoint serves the model; the catalog and dashboard serve different purposes. [Phase 3, step 3.2](../../sessions/2026-09-24-modern-data-platform-bfsi/source/docs/phase3.md#step-32--use-case-1-real-time-fraud-detection).
4. **A.** A replicated copy may be minutes behind, which can be too stale for a live feature. [Phase 2, step 2.3](../../sessions/2026-09-24-modern-data-platform-bfsi/source/docs/phase2.md#step-23--zero-etl-from-dynamodb).
5. **B.** The course uses Lake Formation grants to separate PII access by persona. [Phase 1, step 1.3](../../sessions/2026-09-24-modern-data-platform-bfsi/source/docs/phase1.md#step-13--govern-access-with-lake-formation).
6. **A.** The RAG example enriches chunks with metadata and lineage so retrieval can preserve context and attribution. [Module 3, slide 15](../../sessions/2026-09-24-modern-data-platform-bfsi/slides/module-3.md#slide-15).
