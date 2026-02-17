# FLLC Information Security Policy
**Author:** Preston Furulie | **Classification:** Internal | **Version:** 1.0

---

## 1. Policy Statement

FLLC is committed to protecting the confidentiality, integrity, and availability of all information assets. This policy establishes the minimum security standards for all systems, applications, and data under FLLC management.

**Compliance Framework:** NIST Cybersecurity Framework (CSF) + OWASP Top 10

---

## 2. Access Control

### 2.1 Authentication

| Requirement | Standard |
|------------|----------|
| Password minimum length | 12 characters |
| Password complexity | Uppercase + lowercase + digit + special character |
| Password hashing | bcrypt (cost factor 12) or PBKDF2 (600K iterations, SHA-256) |
| Session timeout | 30 minutes of inactivity |
| Account lockout | After 5 consecutive failed attempts |
| Token format | JWT with RS256 asymmetric signing |
| Access token TTL | 15 minutes |
| Refresh token TTL | 7 days (httpOnly cookie) |
| Multi-factor authentication | Required for admin accounts |

### 2.2 Authorization (RBAC)

Four-tier role hierarchy enforced at the API middleware layer:

| Role | Access Level |
|------|-------------|
| **Viewer** | Read-only access to product catalog and public data |
| **Staff** | Viewer + stock intake, order processing |
| **Manager** | Staff + product management, purchase orders, reporting |
| **Admin** | Manager + user management, system configuration, deletions |

### 2.3 Principle of Least Privilege
- Users receive the minimum permissions required for their role
- Admin access is granted only when necessary and logged
- Service accounts use dedicated IAM roles with scoped policies
- Database users have table-level permissions (no `GRANT ALL`)

---

## 3. Data Protection

### 3.1 Encryption Standards

| Data State | Method | Standard |
|-----------|--------|----------|
| At Rest | AES-256 | AWS RDS encryption, S3 default encryption, EBS encryption |
| In Transit | TLS 1.3 | All HTTP traffic, database connections, Redis connections |
| Passwords | bcrypt/PBKDF2 | Never stored in plaintext; salted with cryptographic random |
| API Keys | SHA-256 hash | Stored hashed; displayed once on creation |
| Secrets | AWS Secrets Manager | Auto-rotated every 90 days |

### 3.2 Data Classification

| Level | Description | Examples | Controls |
|-------|------------|----------|----------|
| **Confidential** | Sensitive business data | Passwords, API keys, financial data | Encrypted at rest + transit, access logged |
| **Internal** | Business operations data | Inventory levels, order details | Encrypted in transit, RBAC enforced |
| **Public** | Publicly available | Product catalog, pricing | Standard web security headers |

### 3.3 Data Handling
- PII (email, addresses) encrypted at column level in the database
- Credit card data is NEVER stored — payment processing delegated to PCI-compliant gateway
- Logs are scrubbed of sensitive data before storage (no passwords, tokens, or PII in logs)
- Database backups are encrypted and stored in a separate AWS account

---

## 4. Network Security

### 4.1 Segmentation
- **DMZ** for public-facing services (reverse proxy only)
- **Application tier** in private subnets (no public IP)
- **Data tier** in isolated subnets (no internet route)
- **Guest network** completely isolated from internal resources
- **IoT/camera network** blocked from internet access

### 4.2 Firewall Policy
- **Default deny** — all traffic blocked unless explicitly allowed
- Zone-based firewall (Palo Alto PA-850) with 10 rules
- Security groups as secondary firewall (AWS)
- NACLs for subnet-level stateless filtering

### 4.3 Monitoring
- VPC Flow Logs enabled on all subnets
- IDS/IPS signatures updated daily
- Anomalous traffic patterns trigger alerts
- SNMP v3 only (v1/v2c disabled — community strings are insecure)

---

## 5. Application Security

### 5.1 OWASP Top 10 Mitigations

| # | Vulnerability | Mitigation |
|---|-------------|-----------|
| A01 | Broken Access Control | RBAC middleware, JWT validation, resource ownership checks |
| A02 | Cryptographic Failures | TLS 1.3, AES-256, bcrypt, no MD5/SHA1 for passwords |
| A03 | Injection | Parameterized queries (Prisma ORM), input validation (Zod) |
| A04 | Insecure Design | Threat modeling during Phase 06, secure defaults |
| A05 | Security Misconfiguration | Infrastructure as Code, automated security scanning |
| A06 | Vulnerable Components | Dependabot alerts, Docker Scout in CI/CD |
| A07 | Auth Failures | Rate limiting, account lockout, secure token storage |
| A08 | Software Integrity | Signed commits, Docker image scanning, SBOM |
| A09 | Logging Failures | Structured logging, CloudWatch, audit trail |
| A10 | SSRF | Input validation, egress filtering, no user-controlled URLs |

### 5.2 Security Headers

```
Strict-Transport-Security: max-age=31536000; includeSubDomains
Content-Security-Policy: default-src 'self'; script-src 'self'
X-Content-Type-Options: nosniff
X-Frame-Options: DENY
X-XSS-Protection: 0
Referrer-Policy: strict-origin-when-cross-origin
Permissions-Policy: camera=(), microphone=(), geolocation=()
```

---

## 6. Incident Response

### 6.1 Severity Levels

| Level | Definition | Response Time | Example |
|-------|-----------|--------------|---------|
| **P1 — Critical** | System compromise, data breach | 15 minutes | Unauthorized access, ransomware |
| **P2 — High** | Service degradation, vulnerability exploited | 1 hour | DDoS, critical CVE in production |
| **P3 — Medium** | Non-critical vulnerability discovered | 24 hours | Medium CVE, misconfiguration |
| **P4 — Low** | Informational finding | 7 days | Best practice deviation, minor exposure |

### 6.2 Response Procedure
1. **Detect** — Monitoring alert or manual report
2. **Contain** — Isolate affected systems (revoke tokens, block IPs, disable accounts)
3. **Investigate** — Analyze logs, determine scope and root cause
4. **Remediate** — Patch vulnerability, rotate credentials, deploy fix
5. **Recover** — Restore services, verify integrity
6. **Post-mortem** — Document timeline, root cause, and prevention measures

---

## 7. Vulnerability Management

| Activity | Frequency | Tool | Owner |
|----------|-----------|------|-------|
| Automated dependency scanning | Every push | Dependabot / Docker Scout | CI/CD |
| Internal network scan | Quarterly | Nessus Professional | Security |
| Penetration testing | Annually | External firm | Security |
| Security code review | Per pull request | Manual + SAST | Engineering |
| Patch management | Weekly (critical: 24h) | OS package managers | Operations |

---

## 8. Compliance Mapping

| Control Area | NIST CSF | CIS Controls | Implementation |
|-------------|----------|--------------|----------------|
| Asset Management | ID.AM | Control 1, 2 | Terraform state, inventory |
| Access Control | PR.AC | Control 4, 5, 6 | RBAC, MFA, least privilege |
| Data Security | PR.DS | Control 3 | Encryption at rest/transit |
| Network Security | PR.AC-5 | Control 12, 13 | Segmentation, firewall |
| Monitoring | DE.CM | Control 8 | CloudWatch, flow logs |
| Incident Response | RS.RP | Control 17 | Documented procedures |
| Recovery | RC.RP | Control 17 | Backups, DR plan |
