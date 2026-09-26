# FinOps Notes

## Cost drivers

Kubernetes worker nodes, NAT gateways, observability retention, registry storage, cross-zone traffic, model inference compute and replicated artifacts.

## Controls

- Mandatory project and environment tags.
- Autoscaling with explicit minimum and maximum capacity.
- Short log retention for the portfolio environment.
- Scheduled shutdown for non-production environments.
- Budgets and anomaly alerts configured outside this public repository.
- Destroy temporary cloud demonstrations after use.

Local Docker Compose is the default no-cloud-cost demonstration path.
