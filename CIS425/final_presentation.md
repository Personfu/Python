# Capstone Final Presentation
## CIS 425 — Capstone | Preston Furulie

## Project Overview

**Guitar Shop Enterprise Platform** — a full-stack, cloud-deployed e-commerce solution for music retailers.

## Key Achievements

- Designed and implemented a normalized MySQL schema (3NF) with 6 core tables
- Built a RESTful API with CRUD operations, authentication, and input validation
- Developed a responsive React frontend with product catalog, cart, and checkout
- Containerized with Docker (multi-stage builds) for consistent deployments
- Deployed to AWS with auto-scaling ECS, RDS Multi-AZ, and CloudFront CDN
- CI/CD pipeline via GitHub Actions — automated testing, building, and deployment

## Metrics

- **API Response Time:** < 50ms (p95)
- **Page Load:** < 1.2s (Lighthouse 95+)
- **Test Coverage:** 87%
- **Uptime:** 99.95% over 30-day monitoring period

## Lessons Learned

- Infrastructure as Code (Terraform) drastically reduces deployment errors
- Database indexing strategy improved query performance by 10x on reporting queries
- Docker multi-stage builds reduced image size from 1.2GB to 180MB
- Implementing RBAC early prevents security retrofitting later

## Technologies Used

Python, JavaScript, React, Node.js, MySQL, Redis, Docker, AWS (ECS, RDS, ALB, CloudFront), Terraform, GitHub Actions
