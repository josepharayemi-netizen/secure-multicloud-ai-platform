# Threat Model

## Protected assets

Model artifacts, training data, inference inputs, cloud identities, container images, audit logs, deployment manifests, and customer decisions.

## Trust boundaries

1. Developer workstation to GitHub.
2. GitHub Actions to container registry.
3. Argo CD to Kubernetes API.
4. Ingress to inference service.
5. Workload to cloud storage and telemetry.

## Priority threats and controls

| Threat | Control |
|---|---|
| Stolen deployment credential | GitHub OIDC and short-lived workload identity |
| Malicious dependency or image | Locked dependencies, Trivy, SBOM and provenance attestation |
| Privileged container escape | Non-root UID, dropped capabilities, seccomp and read-only filesystem |
| Lateral movement | Default-deny NetworkPolicy and dedicated namespace |
| Model replacement | Immutable registry tags, artifact digest and controlled GitOps promotion |
| Data poisoning | Schema validation, lineage, quality gates and approved training sources |
| Model extraction or abuse | Authentication gateway, rate limiting, monitoring and response playbook |
| Telemetry leakage | Redaction, access control and prohibited sensitive labels |

Residual risks and exceptions require a named owner, expiry date and documented approval.
