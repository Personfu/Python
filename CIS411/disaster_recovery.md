# Disaster Recovery and Business Continuity — Comprehensive Guide

## CIS 411 | Portland Community College | Spring 2026

| Field             | Value                              |
|-------------------|------------------------------------|
| **Author**        | Preston Furulie                    |
| **Organization**  | FLLC Enterprise                    |
| **Department**    | Platform Engineering               |
| **Alignment**     | CompTIA Server+ (SK0-005)          |

---

## 1. Business Continuity Planning (BCP) vs Disaster Recovery (DR)

### 1.1 Definitions

| Concept                       | Focus                                              |
|-------------------------------|----------------------------------------------------|
| **Business Continuity (BCP)** | Keeping the entire business operational during and after a disruption |
| **Disaster Recovery (DR)**    | Restoring IT systems and data after a disruption   |

BCP is the broader discipline. DR is a subset of BCP focused specifically on
technology recovery.

### 1.2 BCP vs DR Comparison

| Aspect              | BCP                                  | DR                                   |
|---------------------|--------------------------------------|--------------------------------------|
| Scope               | Entire organization                  | IT infrastructure and data           |
| Focus               | People, processes, and technology    | Technology restoration               |
| Timeframe           | During and after the event           | After the event                      |
| Key Document        | Business Continuity Plan             | Disaster Recovery Plan               |
| Stakeholders        | All departments                      | IT department primarily              |
| Testing             | Tabletop exercises, full simulations | Backup restores, failover tests      |
| Example Actions     | Relocate staff, alternate workflows  | Restore servers, activate DR site    |

### 1.3 BCP Lifecycle

1. **Project Initiation** — Gain executive sponsorship and define scope
2. **Business Impact Analysis (BIA)** — Identify critical functions and dependencies
3. **Risk Assessment** — Evaluate threats and vulnerabilities
4. **Strategy Development** — Design recovery strategies for each critical function
5. **Plan Development** — Document detailed procedures
6. **Testing and Exercises** — Validate the plan works
7. **Maintenance** — Review and update regularly (annually at minimum)

---

## 2. Key Metrics — RPO, RTO, MTTR, MTBF

### 2.1 Definitions and Relationships

| Metric   | Full Name                       | Definition                                              |
|----------|---------------------------------|---------------------------------------------------------|
| **RPO**  | Recovery Point Objective        | Maximum acceptable data loss measured in time           |
| **RTO**  | Recovery Time Objective         | Maximum acceptable downtime before services must resume |
| **MTTR** | Mean Time to Repair             | Average time to restore a failed component              |
| **MTBF** | Mean Time Between Failures      | Average operational time between system failures        |

### 2.2 Visual Timeline

```
Last Good Backup          Disaster Occurs          Service Restored
       |                        |                        |
       |<--- RPO (data loss) -->|<------- RTO ---------->|
       |                        |                        |
  Data saved here         Systems fail          Systems operational
```

### 2.3 Practical Examples

| System               | RPO           | RTO          | Justification                        |
|----------------------|---------------|--------------|--------------------------------------|
| E-commerce website   | 1 hour        | 15 minutes   | Revenue loss per minute of downtime  |
| Email server         | 4 hours       | 2 hours      | Productivity impact, not revenue     |
| File server          | 24 hours      | 8 hours      | Non-critical, can use local copies   |
| Financial database   | 0 (real-time) | 5 minutes    | Regulatory compliance, transactions  |
| Development server   | 24 hours      | 24 hours     | Developers have local copies         |
| FLLC Lab Environment | 4 hours       | 4 hours      | Training impact, scheduled sessions  |

### 2.4 MTBF and MTTR Calculations

**MTBF Example:**
A server ran for 8,760 hours (1 year) and experienced 3 failures.
MTBF = 8,760 / 3 = **2,920 hours** between failures

**MTTR Example:**
The 3 failures took 2h, 4h, and 6h to repair respectively.
MTTR = (2 + 4 + 6) / 3 = **4 hours** average repair time

**Availability = MTBF / (MTBF + MTTR)**
Availability = 2,920 / (2,920 + 4) = **99.86%**

---

## 3. Backup Strategies

### 3.1 Backup Types

| Backup Type    | What It Backs Up                 | Speed     | Restore Speed | Storage   |
|----------------|----------------------------------|-----------|---------------|-----------|
| Full           | All selected data                | Slowest   | Fastest       | Most      |
| Incremental    | Changes since last backup (any)  | Fastest   | Slowest       | Least     |
| Differential   | Changes since last full backup   | Moderate  | Moderate      | Moderate  |

### 3.2 Backup Schedule Examples

**Weekly Full + Daily Incremental:**
```
Sun    Mon    Tue    Wed    Thu    Fri    Sat
Full   Inc    Inc    Inc    Inc    Inc    Inc
```
Restore Wednesday: Need Sunday Full + Mon Inc + Tue Inc + Wed Inc (4 tapes)

**Weekly Full + Daily Differential:**
```
Sun    Mon    Tue    Wed    Thu    Fri    Sat
Full   Diff   Diff   Diff   Diff   Diff   Diff
```
Restore Wednesday: Need Sunday Full + Wed Diff only (2 tapes)

### 3.3 The 3-2-1 Backup Rule

| Component | Requirement                                          |
|-----------|------------------------------------------------------|
| **3**     | Keep at least **3 copies** of your data              |
| **2**     | Store backups on **2 different media types**         |
| **1**     | Keep **1 copy offsite** (or in the cloud)            |

**Extended 3-2-1-1-0 Rule:**
- 3 copies of data
- 2 different media types
- 1 offsite copy
- 1 offline (air-gapped) copy
- 0 errors (verified restores)

### 3.4 Backup Verification

| Test Type              | Description                                   | Frequency     |
|------------------------|-----------------------------------------------|---------------|
| Backup job logs        | Review completion status and errors           | Daily         |
| Checksum verification  | Validate data integrity of backup files       | Weekly        |
| File-level restore     | Restore individual files and verify content   | Monthly       |
| Full system restore    | Restore entire server to test environment     | Quarterly     |
| DR site activation     | Full failover to DR environment               | Annually      |

---

## 4. High Availability

### 4.1 Availability Tiers

| Availability   | Annual Downtime | Common Name     | Example Technology               |
|----------------|-----------------|-----------------|----------------------------------|
| 99%            | 3.65 days       | Two nines       | Single server                    |
| 99.9%          | 8.76 hours      | Three nines     | Basic redundancy                 |
| 99.99%         | 52.6 minutes    | Four nines      | Active-passive cluster           |
| 99.999%        | 5.26 minutes    | Five nines      | Active-active, multi-site        |
| 99.9999%       | 31.5 seconds    | Six nines       | Carrier-grade, extreme redundancy|

### 4.2 High Availability Technologies

| Technology           | Description                                        |
|----------------------|----------------------------------------------------|
| **Clustering**       | Multiple servers acting as a single system         |
| **Load Balancing**   | Distributing requests across multiple servers      |
| **Failover**         | Automatic switching to standby when primary fails  |
| **Replication**      | Maintaining synchronized copies of data            |
| **Redundant Components** | Dual PSU, dual NIC, RAID storage              |
| **Geographic Distribution** | Multiple datacenters in different regions   |

### 4.3 Cluster Types

| Cluster Type     | Description                                         | Use Case                      |
|------------------|-----------------------------------------------------|-------------------------------|
| Active-Active    | All nodes serve traffic simultaneously              | Web servers, load balancing   |
| Active-Passive   | Standby node activates when primary fails           | Databases, file servers       |
| N+1              | One spare node for N active nodes                   | Cost-effective redundancy     |
| N+M              | M spare nodes for N active nodes                    | Higher redundancy guarantee   |

### 4.4 Load Balancing Algorithms

| Algorithm              | Description                                      |
|------------------------|--------------------------------------------------|
| Round Robin            | Distributes requests sequentially across servers |
| Weighted Round Robin   | More requests to higher-capacity servers         |
| Least Connections      | Sends to server with fewest active connections   |
| IP Hash                | Same client IP always hits the same server       |
| Health-Based           | Routes only to healthy servers                   |

---

## 5. Recovery Site Types

| Site Type   | Equipment | Data        | Activation Time | Cost      |
|-------------|-----------|-------------|-----------------|-----------|
| **Hot Site** | Installed | Replicated  | Minutes to hours | Highest  |
| **Warm Site**| Partial   | Recent backup| Hours to days  | Moderate  |
| **Cold Site**| None      | None on-site | Days to weeks  | Lowest    |
| **Cloud DR** | On-demand | Replicated  | Minutes to hours | Variable |
| **Mobile Site**| Portable | Backup media| Hours to days  | Moderate  |

### 5.1 Site Selection Criteria

| Factor                | Consideration                                    |
|-----------------------|--------------------------------------------------|
| Distance from primary | Far enough to avoid same disaster, close enough for data sync |
| Network connectivity  | Sufficient bandwidth for replication             |
| Power reliability     | Redundant power feeds, generator backup          |
| Environmental risks   | Different flood zone, earthquake zone, etc.      |
| Regulatory compliance | Data residency requirements                      |
| Cost vs risk          | Balance between investment and acceptable risk   |

---

## 6. DR Testing

### 6.1 Test Types

| Test Type            | Description                                    | Impact | Confidence |
|----------------------|------------------------------------------------|--------|------------|
| **Checklist Review** | Walk through plan documentation                | None   | Low        |
| **Tabletop Exercise**| Scenario discussion with stakeholders          | None   | Moderate   |
| **Walkthrough**      | Step-by-step review of procedures              | None   | Moderate   |
| **Simulation**       | Simulate disaster without actual failover      | Low    | High       |
| **Parallel Test**    | Activate DR site alongside production          | Low    | High       |
| **Full Interruption**| Shut down production, activate DR site         | High   | Highest    |

### 6.2 DR Test Plan Template

```
FLLC Enterprise — DR Test Plan
================================
Test Date:      ____________________
Test Type:      [ ] Tabletop  [ ] Simulation  [ ] Full Interruption
Test Lead:      ____________________
Participants:   ____________________

Objectives:
1. ________________________________________
2. ________________________________________

Scenario:
________________________________________

Success Criteria:
1. ________________________________________
2. ________________________________________

Results:
[ ] Pass  [ ] Partial Pass  [ ] Fail

Lessons Learned:
________________________________________

Action Items:
1. ________________________________________
2. ________________________________________
```

---

## 7. Incident Response Plan

### 7.1 Incident Response Phases

| Phase              | Activities                                          |
|--------------------|-----------------------------------------------------|
| **1. Preparation**  | Policies, tools, training, contact lists           |
| **2. Identification**| Detect and confirm the incident                   |
| **3. Containment** | Limit damage (short-term and long-term)             |
| **4. Eradication** | Remove the root cause                               |
| **5. Recovery**    | Restore systems to normal operations                 |
| **6. Lessons Learned** | Post-incident review and plan updates           |

### 7.2 Incident Severity Levels

| Severity | Impact                                  | Response Time | Example                       |
|----------|-----------------------------------------|---------------|-------------------------------|
| P1       | Complete service outage                 | Immediate     | Production database down      |
| P2       | Major functionality degraded            | 30 minutes    | Email server intermittent     |
| P3       | Minor functionality impacted            | 4 hours       | Single printer offline        |
| P4       | Cosmetic or informational              | Next business day | UI display issue          |

### 7.3 Communication Plan

| Audience            | Method                  | Frequency               | Owner          |
|---------------------|-------------------------|-------------------------|----------------|
| Incident Team       | War room / chat channel | Continuous               | Incident Lead  |
| IT Management       | Email + phone           | Every 30 min (P1/P2)    | Incident Lead  |
| Executive Team      | Email summary           | Hourly (P1)             | IT Director    |
| Affected Users      | Status page / email     | Every update             | Communications |
| External Customers  | Public status page      | Every major update       | PR Team        |

---

## 8. FLLC Enterprise Disaster Recovery Plan

### 8.1 Plan Overview

| Field                    | Value                                        |
|--------------------------|----------------------------------------------|
| Organization             | FLLC Enterprise                              |
| Plan Owner               | Platform Engineering Department              |
| Last Updated             | Spring 2026                                  |
| Next Review Date         | Fall 2026                                    |
| Primary Contact          | Preston Furulie, Platform Engineering Lead   |
| Classification           | Internal — Confidential                      |

### 8.2 Critical Systems Inventory

| System                | Priority | RPO     | RTO       | DR Strategy              |
|-----------------------|----------|---------|-----------|--------------------------|
| Active Directory      | P1       | 0       | 30 min    | Multi-DC replication     |
| Production Database   | P1       | 1 hour  | 1 hour    | Synchronous replication  |
| Web Application       | P1       | 1 hour  | 15 min    | Load-balanced, multi-AZ  |
| Email System          | P2       | 4 hours | 4 hours   | Cloud-hosted (M365)      |
| File Server           | P2       | 4 hours | 8 hours   | Daily backup to cloud    |
| Development Environment| P3      | 24 hours| 24 hours  | Weekly backup             |
| Lab Systems           | P4       | 48 hours| 48 hours  | Rebuild from templates   |

### 8.3 Emergency Contact List

```
FLLC Enterprise — Emergency Contacts
======================================
Role                    | Name              | Phone          | Email
Incident Commander      | [Designated Lead] | (xxx) xxx-xxxx | ____@fllc.com
Platform Engineering    | Preston Furulie   | (xxx) xxx-xxxx | ____@fllc.com
Network Operations      | [Team Lead]       | (xxx) xxx-xxxx | ____@fllc.com
Security Team           | [Team Lead]       | (xxx) xxx-xxxx | ____@fllc.com
Executive Sponsor       | [Director]        | (xxx) xxx-xxxx | ____@fllc.com
Vendor Support (Cloud)  | AWS/Azure Support | 1-800-xxx-xxxx | support@____
```

### 8.4 Recovery Procedures Summary

| Step | Action                                           | Responsible        | Time Target |
|------|--------------------------------------------------|--------------------|-------------|
| 1    | Assess scope of disaster                         | Incident Commander | 15 min      |
| 2    | Activate DR plan, notify stakeholders            | Incident Commander | 30 min      |
| 3    | Initiate failover for P1 systems                 | Platform Engineering| 1 hour     |
| 4    | Verify P1 system functionality                   | QA / App Owners    | 1.5 hours   |
| 5    | Restore P2 systems from backups                  | Platform Engineering| 4 hours    |
| 6    | Verify P2 system functionality                   | App Owners         | 6 hours     |
| 7    | Communicate status to all stakeholders           | Communications     | Ongoing     |
| 8    | Begin P3/P4 restoration                          | Platform Engineering| 24 hours   |
| 9    | Plan failback to primary site                    | Platform Engineering| TBD        |
| 10   | Conduct post-incident review                     | All Teams          | Within 1 week|

---

## References

- CompTIA Server+ SK0-005 Exam Objectives
- NIST SP 800-34: Contingency Planning Guide
- ISO 22301: Business Continuity Management
- FEMA Business Continuity Planning Suite

---

*FLLC Enterprise — Platform Engineering Division*
*Author: Preston Furulie | Portland Community College | Spring 2026*
