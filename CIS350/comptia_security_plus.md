# CompTIA Security+ (SY0-701) Study Guide
## CIS 350 — Network Security & Cybersecurity | FLLC Enterprise
## Author: Preston Furulie | Spring 2026

---

## Exam Overview

| Field | Value |
|-------|-------|
| **Exam Code** | SY0-701 |
| **Questions** | Maximum of 90 |
| **Duration** | 90 minutes |
| **Passing Score** | 750 (on a scale of 100-900) |
| **Format** | Multiple choice + performance-based |

---

## Domain 1: General Security Concepts (12%)

### 1.1 Security Controls

| Control Type | Purpose | Examples |
|-------------|---------|---------|
| **Technical** | Implemented via technology | Firewalls, encryption, IDS/IPS, antivirus |
| **Managerial** | Policies and procedures | Security policies, risk assessments, training |
| **Operational** | Day-to-day processes | Change management, incident response, patrols |
| **Physical** | Protect physical assets | Locks, cameras, mantraps, fencing, guards |

| Category | Description |
|----------|-------------|
| **Preventive** | Stop incidents before they occur (firewall rules, access controls) |
| **Detective** | Identify incidents that have occurred (IDS, log monitoring, SIEM) |
| **Corrective** | Fix issues after detection (patching, restoring from backup) |
| **Deterrent** | Discourage attacks (warning banners, security cameras) |
| **Compensating** | Alternative when primary control isn't feasible |

### 1.2 CIA Triad

- **Confidentiality** — Only authorized users can access data (encryption, RBAC, MFA)
- **Integrity** — Data is accurate and unmodified (hashing, digital signatures, checksums)
- **Availability** — Systems are accessible when needed (redundancy, backups, load balancing)

### 1.3 Zero Trust Model

> "Never trust, always verify"

- Verify every request regardless of source location
- Least privilege access by default
- Microsegmentation of networks
- Continuous authentication and monitoring
- Data-centric security approach

### 1.4 AAA Framework

- **Authentication** — Prove who you are (passwords, biometrics, tokens)
- **Authorization** — What you're allowed to do (RBAC, ABAC, ACLs)
- **Accounting** — Logging what you did (audit trails, SIEM)

---

## Domain 2: Threats, Vulnerabilities, and Mitigations (22%)

### 2.1 Threat Actors

| Actor | Motivation | Sophistication | Funding |
|-------|-----------|----------------|---------|
| Script kiddies | Fun, notoriety | Low | None |
| Hacktivists | Ideology, political | Medium | Variable |
| Organized crime | Financial gain | High | Significant |
| Nation-state (APT) | Espionage, warfare | Very high | Government |
| Insider threats | Revenge, profit, negligence | Variable | N/A |

### 2.2 Attack Types

| Attack | Description | Mitigation |
|--------|-------------|------------|
| **Phishing** | Deceptive emails/sites for credentials | User training, email filtering, MFA |
| **Spear phishing** | Targeted phishing at specific individuals | Executive awareness training |
| **Ransomware** | Encrypts data, demands payment | Backups, endpoint protection, segmentation |
| **Man-in-the-Middle** | Intercepts communication | TLS/HTTPS, certificate pinning |
| **SQL injection** | Malicious SQL via user input | Parameterized queries, input validation |
| **XSS** | Inject scripts into web pages | Output encoding, CSP headers |
| **DDoS** | Overwhelm resources with traffic | WAF, CDN, rate limiting, ISP scrubbing |
| **Brute force** | Try all possible passwords | Account lockout, rate limiting, MFA |
| **Privilege escalation** | Gain higher access than authorized | Least privilege, patching, monitoring |
| **Social engineering** | Manipulate people to bypass security | Security awareness training |

### 2.3 Vulnerability Types

- **Software** — Unpatched OS, outdated libraries, buffer overflow, zero-day
- **Configuration** — Default credentials, open ports, unnecessary services
- **Architectural** — Flat networks, single point of failure, missing segmentation
- **Human** — Weak passwords, social engineering susceptibility, insider error

---

## Domain 3: Security Architecture (18%)

### 3.1 Network Security

```
Internet
    │
    ▼
┌──────────┐
│   WAF    │  ← Web Application Firewall
└────┬─────┘
     │
┌────▼─────┐
│ Firewall │  ← Stateful inspection, NGFW
└────┬─────┘
     │
┌────▼─────┐
│   DMZ    │  ← Web servers, reverse proxy
└────┬─────┘
     │
┌────▼─────┐
│  IDS/IPS │  ← Intrusion Detection/Prevention
└────┬─────┘
     │
┌────▼─────┐
│ Internal │  ← Application servers, databases
│ Network  │     (segmented by VLAN)
└──────────┘
```

### 3.2 Encryption Standards

| Algorithm | Type | Key Size | Use Case |
|-----------|------|----------|----------|
| AES-256 | Symmetric | 256-bit | Data at rest, VPN |
| RSA | Asymmetric | 2048/4096-bit | Key exchange, digital signatures |
| SHA-256 | Hash | 256-bit output | Integrity verification |
| TLS 1.3 | Protocol | Various | Data in transit |
| ECDSA | Asymmetric | 256-bit | Digital certificates |
| bcrypt | Hash + KDF | Configurable | Password hashing |

### 3.3 PKI (Public Key Infrastructure)

- **Certificate Authority (CA)** — Issues and signs digital certificates
- **Certificate types** — DV, OV, EV (Domain, Organization, Extended Validation)
- **Certificate lifecycle** — Request → Issue → Use → Renew/Revoke
- **CRL** — Certificate Revocation List
- **OCSP** — Online Certificate Status Protocol (real-time validation)

---

## Domain 4: Security Operations (28%)

### 4.1 Incident Response Steps

1. **Preparation** — Policies, tools, training, communication plan
2. **Detection & Analysis** — Monitoring, alerting, triage, scope assessment
3. **Containment** — Isolate affected systems (short-term and long-term)
4. **Eradication** — Remove threat, patch vulnerabilities, reset credentials
5. **Recovery** — Restore systems, verify integrity, monitor for recurrence
6. **Lessons Learned** — Post-incident review, update procedures, document

### 4.2 Log Management & SIEM

| Source | Data |
|--------|------|
| Firewall logs | Allowed/denied connections, source/dest IPs |
| System logs | Login attempts, service starts/stops, errors |
| Application logs | User actions, API calls, errors |
| DNS logs | Resolution requests, blocked domains |
| IDS/IPS logs | Alert events, blocked attacks |

**SIEM Functions:** Log aggregation → Normalization → Correlation → Alerting → Dashboarding → Reporting

### 4.3 Vulnerability Management Lifecycle

1. **Discover** — Asset inventory (what do we have?)
2. **Assess** — Vulnerability scanning (Nessus, Qualys)
3. **Prioritize** — CVSS score + business context
4. **Remediate** — Patch, configure, or accept risk
5. **Verify** — Re-scan to confirm fix
6. **Report** — Document findings and compliance status

---

## Domain 5: Security Program Management & Oversight (20%)

### 5.1 Governance Frameworks

| Framework | Focus | Use |
|-----------|-------|-----|
| **NIST CSF** | Cybersecurity risk | US government and private sector |
| **ISO 27001** | ISMS (Information Security Management System) | International certification |
| **CIS Controls** | Prioritized security actions | Practical implementation guide |
| **COBIT** | IT governance | Enterprise IT management |
| **PCI-DSS** | Payment card data | Anyone processing credit cards |
| **HIPAA** | Healthcare data | Healthcare organizations |
| **SOC 2** | Service organization controls | Cloud/SaaS providers |

### 5.2 Risk Management

| Term | Definition |
|------|------------|
| **Risk** | Likelihood × Impact of a threat exploiting a vulnerability |
| **Threat** | Potential cause of harm (hacker, natural disaster, insider) |
| **Vulnerability** | Weakness that can be exploited |
| **Asset** | Anything of value (data, systems, people, reputation) |
| **Risk acceptance** | Acknowledge and accept the risk |
| **Risk avoidance** | Eliminate the activity that causes risk |
| **Risk transference** | Shift risk to third party (insurance, SLA) |
| **Risk mitigation** | Reduce likelihood or impact (controls) |

### 5.3 Security Awareness Training

- Phishing simulation campaigns
- Annual security awareness training
- Role-specific training (developers: secure coding; admins: hardening)
- Incident reporting procedures
- Clean desk policy
- Social media guidelines

---

## FLLC Enterprise Mapping

| Security+ Domain | FLLC Phase Implementation |
|-------------------|--------------------------|
| General Concepts | Phase 07: encryption_hashing.py (CIA, hashing) |
| Threats & Vulns | Phase 07: vulnerability_assessment.md (Nessus, CVEs) |
| Architecture | Phase 07: network_topology.md + firewall_rules.conf |
| Operations | Phase 08: deploy.yml (CI/CD security scanning) |
| Program Mgmt | docs/security-policy.md (governance, incident response) |
