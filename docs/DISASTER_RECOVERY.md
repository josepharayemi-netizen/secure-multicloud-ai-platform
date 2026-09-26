# Disaster Recovery

- RTO: 30 minutes; RPO: 15 minutes.
- Replicate approved model artifacts to a secondary region.
- Store Terraform state in a locked, encrypted remote backend.
- Back up GitOps configuration, audit logs and registry metadata.
- Test restoration quarterly using a clean cluster.
- Keep DNS failover and certificate procedures documented and access-controlled.

The portfolio configuration does not automatically create multi-region resources to avoid unnecessary cost.
