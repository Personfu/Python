# Phase 08 — Cloud & DevOps Engineering
**Department:** Platform Engineering | **Course:** CIS 410 — Cloud & DevOps | **Status:** Complete

---

## Purpose

Automate FLLC's infrastructure provisioning, container packaging, and deployment pipeline — enabling reproducible, version-controlled infrastructure with zero-downtime deployments and automatic rollback.

## Deliverables

| File | Description | Key Concepts |
|------|------------|-------------|
| [`vpc_design.tf`](vpc_design.tf) | AWS VPC Infrastructure (Terraform) | VPC (10.0.0.0/16), 9 subnets (public/app/data × 3 AZs), Internet Gateway, NAT Gateway, 3 route tables, 4 security groups (ALB→ECS→RDS→Redis), VPC Flow Logs to CloudWatch, IAM roles, S3 remote backend with DynamoDB locking, variables, outputs |
| [`infrastructure.tf`](infrastructure.tf) | AWS Services (RDS, ECS, ALB) | RDS MySQL 8.0 Multi-AZ (encrypted, 30-day backups), ECS Fargate cluster with container insights, task definition with CloudWatch logging, ECS service (desired count 2, rolling update), ALB with TLS 1.3 listener, target group with health checks |
| [`Dockerfile`](Dockerfile) | Production Docker Image | 3-stage build (deps→build→production), `npm ci --omit=dev` for layer caching, Prisma client generation, non-root user (`appuser:appgroup`), `apk upgrade` for security patches, healthcheck (wget), OCI labels, 178 MB final image |
| [`docker-compose.yml`](docker-compose.yml) | Local Development Stack | 5 services: API (Node.js), MySQL 8.0, Redis 7, Nginx reverse proxy, Adminer (dev profile); custom bridge network, named volumes, secrets management, health checks on all services, resource limits (CPU/memory), structured logging, MySQL tuning flags |
| [`deploy.yml`](deploy.yml) | GitHub Actions CI/CD Pipeline | 6 stages: lint (ESLint + tsc), unit tests (Jest, 80% coverage gate), integration tests (MySQL + Redis service containers), Docker build + Scout security scan, ECS deploy (rolling update, 10-min stability wait), smoke test + automatic rollback on failure, concurrency control |

## Infrastructure Diagram

```
GitHub Push → Actions Pipeline → ECR → ECS Fargate (us-west-2)
                                         │
                              ┌──────────┼──────────┐
                              │          │          │
                           AZ-a        AZ-b       AZ-c
                           ┌───┐      ┌───┐      ┌───┐
                           │ALB│      │ALB│      │ALB│  ← Public subnets
                           └─┬─┘      └─┬─┘      └─┬─┘
                             │          │          │
                           ┌─┴─┐      ┌─┴─┐      ┌─┴─┐
                           │ECS│      │ECS│      │ECS│  ← App subnets
                           └─┬─┘      └─┬─┘      └─┬─┘
                             │          │          │
                           ┌─┴─┐      ┌─┴─┐      ┌─┴─┐
                           │RDS│      │RDS│      │RED│  ← Data subnets
                           │Pri│      │Stb│      │IS │
                           └───┘      └───┘      └───┘
```

## Enterprise Application

- VPC design from this phase hosts the **Phase 09** enterprise platform
- CI/CD pipeline automates deployment of every code change
- Docker Compose enables consistent local development matching production
- Terraform enables full environment recreation in < 15 minutes
