# Deployment Architecture
## CIS 425 — Capstone | Preston Furulie

## Production Environment

**Cloud Provider:** AWS (us-west-2)
**Infrastructure:** Terraform-managed
**CI/CD:** GitHub Actions

## Components

| Component   | Technology                         | Spec                              |
|-------------|------------------------------------|------------------------------------|
| Frontend    | React SPA on CDN                   | Auto-deploy from main branch       |
| API         | Node.js on ECS Fargate             | 2 tasks, auto-scaling 2-8          |
| Database    | RDS MySQL 8.0 Multi-AZ             | db.t3.medium, 50GB encrypted       |
| Cache       | ElastiCache Redis                  | cache.t3.micro                     |
| Storage     | S3                                 | File uploads and report PDFs       |
| DNS         | Route 53                           | Health-checked A/AAAA records      |

## Network Architecture

- VPC 10.0.0.0/16 with public/private subnet pairs in 2 AZs
- Application Load Balancer in public subnets (TLS termination)
- ECS tasks in private subnets (no direct internet access)
- RDS in isolated private subnets (access only from app SG)
- NAT Gateway for outbound traffic from private subnets

## CI/CD Pipeline

1. **Push to main** triggers GitHub Actions workflow
2. **Test** — linting, unit tests, integration tests
3. **Build** — Docker image built and pushed to ECR
4. **Security Scan** — container vulnerability scan
5. **Deploy** — rolling update to ECS (zero-downtime)
6. **Smoke Test** — automated health check after deploy

## Monitoring & Observability

- **CloudWatch Metrics** — CPU, memory, request count, 5xx rate
- **CloudWatch Alarms** — auto-notify on threshold breach
- **CloudWatch Logs** — centralized logging with 90-day retention
- **Uptime Monitoring** — external checks every 60 seconds
- **Custom Dashboards** — real-time API performance and error rates

## Scaling Strategy

- ECS auto-scaling: scale out at 70% CPU, scale in at 30%
- RDS read replicas for heavy reporting queries
- Redis caching for hot product catalog queries (TTL: 5 min)
- CDN caching for static assets (TTL: 24 hours)

## Disaster Recovery

- **RPO:** 1 hour (continuous RDS backups)
- **RTO:** 15 minutes (automated failover)
- Multi-AZ RDS provides automatic database failover
- S3 cross-region replication for critical assets
- Terraform state enables full infrastructure rebuild
