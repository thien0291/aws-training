# ML Engineer Associate flashcards from this session

## Fronts

1. Why are historical transaction labels useful for fraud training but unavailable at scoring time?
2. Name three kinds of fraud features built in the NovaBanco demo.
3. What is the difference between SageMaker Lakehouse and a SageMaker AI inference endpoint?
4. Why can a Zero-ETL-fed feature be unsuitable for a sub-second fraud decision?
5. What is the online inference path in the demo?
6. Why must online features match the definitions used during training?
7. What does an Iceberg snapshot help with when reconstructing model input data?
8. How does Lake Formation help the fraud team use data without broad PII access?
9. In the RAG slide, why attach metadata and lineage to document chunks?
10. What ML engineering work remains after building an endpoint and alert threshold?

## Backs

1. A label is the known outcome from historical cases; a new transaction has not yet been confirmed as fraud or legitimate.
2. Examples: transaction count in one hour, total amount in 24 hours, foreign merchant flag, high-value online flag, customer risk tier.
3. Lakehouse/Catalog manages and governs data; an AI endpoint runs a deployed model for inference.
4. Managed replication can lag the operational source by minutes, while fraud scoring may need fresh event context now.
5. Kinesis transaction → Lambda feature enrichment → SageMaker endpoint → score → stored result and/or SNS alert.
6. Mismatched feature calculation or freshness can make live inputs unlike the training data and degrade decisions.
7. It identifies a historical table state, provided the relevant snapshot and files are retained.
8. Column/row permissions let the team use allowed risk signals while restricting identity fields.
9. They help retrieve relevant source passages, filter/attribute results, and trace generated answers to their inputs.
10. Train/tune/evaluate the model, choose deployment and threshold strategies, monitor quality/drift/latency, secure it, and plan retraining/rollback.
