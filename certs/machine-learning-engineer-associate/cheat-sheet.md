# ML Engineer Associate overlap cheat sheet

## Fraud-scoring path in this course

1. **Historical source:** curated customer and transaction tables in S3/Iceberg, plus risk context from warehouse data.
2. **Features:** transaction velocity over time, amount, channel/merchant-country flags, and customer risk context.
3. **Labels:** historical fraud labels are used for supervised model development; an online inference event has no known label yet.
4. **Online path:** Kinesis transaction → Lambda enrichment → SageMaker AI endpoint → score → durable record/alert.
5. **Business action:** a threshold can route high-risk transactions to review or block; threshold selection is a business/model-evaluation decision, not supplied by the data-platform course.

## Key distinctions

| Concept | What it means here |
| --- | --- |
| SageMaker Lakehouse/Catalog | Data storage, discovery, and governance for analytics/AI inputs. |
| SageMaker AI endpoint | Deployed model interface for inference. |
| Training feature vs. online feature | They must represent the same concept; freshness, availability, and leakage matter. |
| Batch preparation vs. stream scoring | Curated historical data supports training; streaming events support immediate decisions. |
| RAG | Retrieve relevant external content using chunks/embeddings/metadata before generation. The session only sketches this pattern. |

## Beyond this session

Learn train/validation/test splits, class imbalance, precision/recall and false-positive cost, model monitoring, drift, retraining, deployment modes, CI/CD, and the official exam version's GenAI scope. The course presents a SageMaker endpoint but does not teach how to train, tune, deploy, or operate the model in depth.
