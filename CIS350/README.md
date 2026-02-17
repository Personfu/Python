# Phase 07 — Information Security
**Department:** Cybersecurity | **Course:** CIS 350 — Network & Cybersecurity | **Status:** Complete

---

## Purpose

Establish FLLC's complete cybersecurity posture — from encryption primitives and password security through enterprise network design, vulnerability management, and firewall policy. These controls protect all assets across every phase.

## Deliverables

| File | Description | Key Concepts |
|------|------------|-------------|
| [`encryption_hashing.py`](encryption_hashing.py) | Encryption & Hashing Toolkit (9 sections) | Hash algorithm comparison (MD5→SHA-512), avalanche effect demo, salted password hashing, PBKDF2 key derivation (600K iterations), HMAC message authentication, password strength analyzer (scoring + entropy), Caesar cipher (encrypt/decrypt/brute-force), XOR encryption, file integrity checking, secure random generation |
| [`network_topology.md`](network_topology.md) | Enterprise Network Topology Design | Hub-and-spoke with DMZ, 8 VLANs (addressing scheme), ASCII network diagram, equipment specs (Palo Alto PA-850, Cisco Cat 9300, Meraki MR46), server inventory (5 servers), security zones (6 trust levels), inter-zone policy matrix, wireless design (3 SSIDs, WPA3), redundancy (dual ISP, HA, dual PSU), monitoring stack |
| [`vulnerability_assessment.md`](vulnerability_assessment.md) | Vulnerability Assessment Report | Nessus scan methodology (NIST SP 800-115), results overview (60 findings), scan configuration, 3 critical CVEs (FortiOS RCE, XZ backdoor, HTTP/2 DoS), 8 high-severity findings, medium summary by category, remediation priority matrix, recommended order with owners/ETAs, compliance mapping (NIST CSF, CIS Controls, PCI-DSS), next assessment schedule |
| [`firewall_rules.conf`](firewall_rules.conf) | Palo Alto Firewall Configuration | Zone definitions (8 zones), 10 rules: outside→DMZ (web), DMZ→servers (API), server→server (MySQL/Redis), corporate→outside (filtered), corporate→servers, management→all (admin), guest→outside (isolated), VoIP (QoS), IoT (restricted, no internet), VPN (IPSec/SSL), implicit deny-all with logging |

## Enterprise Application

- Encryption patterns from this phase secure authentication in **Phase 09** API
- Network topology designs inform AWS VPC segmentation in **Phase 08**
- Firewall rules translate to AWS Security Group rules in Terraform
- Vulnerability assessment methodology applies to quarterly security reviews
- Security policy (`docs/security-policy.md`) codifies all findings into organizational policy
