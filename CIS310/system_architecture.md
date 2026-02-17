# System Architecture Proposal
## CIS 310 — Systems Analysis & Design | Preston Furulie

## Architecture: Three-Tier Design

### Presentation Layer (Frontend)

- React.js SPA with responsive design
- Deployed on CDN (edge caching)
- JWT-based authentication

### Application Layer (Backend)

- Node.js + Express REST API
- Input validation with Joi
- Rate limiting: 100 req/min per user
- Deployed on AWS ECS (auto-scaling)

### Data Layer

- MySQL 8.0 on AWS RDS (Multi-AZ)
- Redis cache for session storage and hot queries
- Daily automated backups with 30-day retention

## Security

- All traffic over HTTPS (TLS 1.3)
- OWASP Top 10 mitigations implemented
- Role-based access control (RBAC)
- SQL injection prevention via parameterized queries
