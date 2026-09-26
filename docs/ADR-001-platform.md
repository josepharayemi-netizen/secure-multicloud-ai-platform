# ADR-001: Kubernetes and GitOps Platform

## Decision

Use Kubernetes as the common workload layer and Argo CD for desired-state delivery across AWS EKS and Azure AKS.

## Rationale

This makes application packaging, security controls, health checks and observability portable while keeping cloud identity, networking and managed services provider-specific.

## Consequences

The platform gains portability and auditable rollback but introduces cluster operations, policy, capacity and upgrade responsibilities.
