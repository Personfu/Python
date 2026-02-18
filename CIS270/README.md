# Phase 11 — Computer Networking

| Field            | Detail                                      |
|------------------|---------------------------------------------|
| **Department**   | Network Engineering                         |
| **Course**       | CIS 270 — Computer Networking               |
| **Institution**  | Portland Community College                  |
| **Term**         | Spring 2026                                 |
| **Author**       | Preston Furulie                             |
| **Organization** | FLLC Enterprise                             |
| **Certification**| CompTIA Network+ (N10-009) Aligned          |
| **Status**       | In Progress                                 |

---

## Overview

Phase 11 covers foundational and intermediate computer networking concepts aligned
with the CompTIA Network+ (N10-009) certification exam. Topics span the OSI and
TCP/IP models, IP addressing and subnetting, network protocols, infrastructure
devices, and systematic troubleshooting methodology.

---

## Deliverables

| #  | File                          | Description                                              | Status      |
|----|-------------------------------|----------------------------------------------------------|-------------|
| 1  | `osi_tcp_model.py`            | OSI 7-layer & TCP/IP 4-layer models, encapsulation sim   | Complete    |
| 2  | `ip_subnetting.py`            | IPv4/IPv6 addressing, subnetting, VLSM, CIDR             | Complete    |
| 3  | `network_protocols.py`        | DHCP, DNS, ARP, HTTP/S, FTP, SSH, SMTP — port reference   | Complete    |
| 4  | `network_devices.md`          | Hub/Switch/Router, wireless, firewalls, enterprise layout | Complete    |
| 5  | `network_troubleshooting.py`  | 7-step methodology, CLI tools, cable types, metrics       | Complete    |
| 6  | `CIS270_complete.txt`         | Full course summary — FLLC enterprise format              | Complete    |

---

## CompTIA Network+ (N10-009) Domain Mapping

| Domain | Weight | Covered In                        |
|--------|--------|-----------------------------------|
| 1.0 Networking Concepts       | 23% | `osi_tcp_model.py`, `ip_subnetting.py`  |
| 2.0 Network Implementation    | 19% | `network_devices.md`, `network_protocols.py` |
| 3.0 Network Operations        | 16% | `network_protocols.py`, `network_devices.md` |
| 4.0 Network Security          | 19% | `network_devices.md`, `network_protocols.py` |
| 5.0 Network Troubleshooting   | 23% | `network_troubleshooting.py`       |

---

## Enterprise Notes — FLLC

- All Python modules follow PEP 8 and run standalone via `python <file>.py`.
- Each `.py` file includes the FLLC Enterprise header block.
- Content is structured for both exam preparation and practical lab reference.
- ASCII network diagrams are provided for visual learners.
- Phase 11 integrates into the broader FLLC Enterprise IT curriculum track.

---

## How to Run

```bash
# Run any module standalone
python osi_tcp_model.py
python ip_subnetting.py
python network_protocols.py
python network_troubleshooting.py
```

Each module prints a comprehensive breakdown of its topic area to the console.

---

*FLLC Enterprise IT — Portland Community College — Spring 2026*
