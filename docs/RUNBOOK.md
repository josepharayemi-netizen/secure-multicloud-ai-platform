# Operations Runbook

## High error rate

1. Confirm the alert and affected model version.
2. Check pod health, recent GitOps sync and dependency failures.
3. Compare error rate and latency with the previous version.
4. Roll back the Git commit or Helm image tag through GitOps.
5. Preserve logs, traces, model digest and deployment evidence.

## Suspected compromise

1. Revoke affected workload identity and pause promotion.
2. Isolate the namespace and preserve audit evidence.
3. Verify image digest, SBOM, provenance and artifact hash.
4. Rotate secrets through the cloud secret manager.
5. Rebuild from an approved commit and document lessons learned.

## Model-quality degradation

1. Check input schema and feature distributions.
2. Compare live outcomes with the approved baseline.
3. Route uncertain decisions to human review.
4. Retrain only from an approved dataset and promote after evaluation.
