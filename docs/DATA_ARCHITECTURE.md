# Data architecture

The local reference uses immutable JSONL micro-batches so validation and idempotency can run without paid infrastructure. In production, the same event contract maps to Kafka or Azure Event Hubs and a Bronze/Silver/Gold lakehouse on Amazon S3 or Azure Data Lake Storage.

## Processing contract

1. Ingest versioned `TransactionEvent` records.
2. Reject malformed timestamps and invalid business fields.
3. Deduplicate by `event_id` for replay-safe processing.
4. Persist immutable raw data in Bronze.
5. Apply feature transformations in Silver.
6. Publish curated features and prediction outcomes to Gold.
7. Record batch checksum, schema version, row count and model version for lineage.

For large-scale deployment, Apache Iceberg supplies schema evolution, time travel and snapshot isolation while Spark or Flink performs batch or streaming computation. Object storage remains cloud-portable; access is controlled through workload identity and customer-managed encryption keys.

## Data quality gates

- Contract and range validation before persistence
- Deterministic deduplication for at-least-once delivery
- Schema-version compatibility checks
- Row-count and checksum lineage
- Quarantine path for rejected events
- Retention, classification and deletion policies applied per data zone
