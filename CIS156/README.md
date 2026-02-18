# Phase 10 — Computer Science Concepts

| Field        | Detail                                          |
|--------------|-------------------------------------------------|
| **Department** | Computer Information Systems                  |
| **Course**     | CIS 156 — Computer Science Concepts           |
| **Term**       | Spring 2026                                    |
| **Author**     | Preston Furulie                                |
| **Organization** | FLLC Enterprise                             |
| **Certification** | CompTIA ITF+ (IT Fundamentals+) Aligned   |
| **Status**     | In Progress                                    |

---

## Overview

Phase 10 integrates core computer science theory into the FLLC Enterprise IT
infrastructure initiative. This coursework bridges the gap between hands-on
technical skills acquired in earlier phases and the foundational CS concepts
that underpin every layer of modern IT systems — from how operating systems
manage resources, to how data traverses networks, to how databases persist
information securely.

Every module is aligned with CompTIA ITF+ exam objectives so that completion
of this phase simultaneously prepares for industry certification.

---

## Deliverables

| # | File                          | Topic                           | Lines  | ITF+ Domain            |
|---|-------------------------------|---------------------------------|--------|------------------------|
| 1 | `computational_thinking.py`   | Computational Thinking          | 200+   | Software Development   |
| 2 | `operating_systems.py`        | Operating System Concepts       | 180+   | Infrastructure          |
| 3 | `networking_fundamentals.py`  | Networking Fundamentals         | 180+   | Infrastructure          |
| 4 | `security_fundamentals.py`    | Security Fundamentals           | 150+   | Security               |
| 5 | `database_concepts.py`        | Database Concepts               | 150+   | Software Development   |
| 6 | `CIS156_complete.txt`         | Course Summary & Review         | —      | All Domains            |

---

## Enterprise Application Notes

These modules directly support the FLLC Enterprise IT stack:

- **Computational Thinking** — Provides the problem-solving methodology used
  when designing automation scripts, troubleshooting workflows, and
  architecting system integrations across the enterprise.

- **Operating Systems** — Understanding process scheduling, memory management,
  and file-system internals is essential for server administration, container
  orchestration, and workstation deployment within FLLC infrastructure.

- **Networking** — The OSI model, TCP/IP stack, DNS, and socket programming
  knowledge maps directly to FLLC's network topology design, firewall rules,
  and service-to-service communication patterns.

- **Security** — CIA triad principles, authentication mechanisms, and threat
  awareness form the baseline security posture for every FLLC system, user
  account, and data store.

- **Databases** — Relational database design and SQL fluency support FLLC's
  inventory tracking, user management, and reporting systems built on SQLite
  and PostgreSQL backends.

---

## How to Run

Each `.py` file is a standalone module. Run from the project directory:

```bash
python computational_thinking.py
python operating_systems.py
python networking_fundamentals.py
python security_fundamentals.py
python database_concepts.py
```

All output is printed to the console — no external dependencies required
beyond the Python 3.10+ standard library.

---

*FLLC Enterprise — Building infrastructure through education.*
