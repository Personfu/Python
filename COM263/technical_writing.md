# Technical Writing — Comprehensive Guide

## COM 263 | Portland Community College | Spring 2026

| Field             | Value                                    |
|-------------------|------------------------------------------|
| **Author**        | Preston Furulie                          |
| **Organization**  | FLLC Enterprise                          |
| **Department**    | Professional Development                 |
| **Course**        | COM 263 — Interpersonal Communication    |

---

## 1. Technical Documentation Best Practices

### 1.1 Core Principles

| Principle        | Description                                            |
|------------------|--------------------------------------------------------|
| Clarity          | Use precise language; avoid ambiguity                  |
| Conciseness      | Say what needs to be said — nothing more               |
| Accuracy         | Verify all facts, commands, and procedures             |
| Consistency      | Use the same terms, formats, and structures throughout |
| Accessibility    | Write for the reader's level of understanding          |
| Maintainability  | Structure documents so they're easy to update          |
| Completeness     | Include all information the reader needs to act        |

### 1.2 Documentation Lifecycle

| Phase            | Activities                                             |
|------------------|--------------------------------------------------------|
| Planning         | Define scope, audience, purpose, and outline           |
| Drafting         | Write initial content following the outline            |
| Review           | Peer review for accuracy and clarity                   |
| Testing          | Have someone follow the document to verify steps       |
| Publishing       | Format, version, and distribute to audience            |
| Maintenance      | Review quarterly; update after every system change     |

### 1.3 Formatting Standards

| Element            | Guideline                                            |
|--------------------|------------------------------------------------------|
| Headings           | Use hierarchical headers (H1 > H2 > H3), max 4 levels|
| Lists              | Numbered for sequential steps; bullets for unordered |
| Code blocks        | Monospaced font, syntax highlighting when possible   |
| Tables             | Use for comparing options or displaying structured data|
| Screenshots        | Annotate with arrows/boxes; include alt text         |
| Cross-references   | Link to related docs instead of duplicating content  |
| Version info       | Include date, author, and version number             |

---

## 2. Audience Analysis for Technical Writing

### 2.1 Audience Categories

| Audience Level  | Technical Knowledge | Wants to Know                      | Writing Style                    |
|-----------------|--------------------|------------------------------------|----------------------------------|
| Executive       | Low to moderate    | Business impact, cost, timeline    | High-level, visual, brief        |
| Manager         | Moderate           | Progress, risks, resource needs    | Summary with details available   |
| Technical peer  | High               | Implementation details, code       | Detailed, precise, technical     |
| End user        | Low                | How to accomplish their task       | Step-by-step, simple language    |
| Auditor         | Moderate           | Compliance evidence, controls      | Formal, evidence-based           |

### 2.2 Audience Analysis Questions

Before writing any document, answer these questions:

| Question                                      | Impact on Writing                        |
|-----------------------------------------------|------------------------------------------|
| Who is the primary reader?                    | Determines vocabulary and detail level   |
| What do they already know?                    | Avoid over-explaining known concepts     |
| What do they need to do with this information?| Determines document type and structure   |
| What is their attitude toward the topic?      | Influences tone (persuasive vs neutral)  |
| How will they access the document?            | Affects formatting (print vs screen)     |
| What decisions will this document support?    | Focus content on decision-relevant info  |

### 2.3 Adjusting Technical Depth

| Original (Too Technical)                             | Revised (For Executive Audience)                |
|------------------------------------------------------|-------------------------------------------------|
| "The RAID 5 array experienced a URE during rebuild"  | "A storage disk failed, risking data loss"      |
| "Latency increased to 450ms on p99"                  | "The system became noticeably slower for users" |
| "We need to refactor the authentication microservice" | "We need to improve login reliability"         |

---

## 3. Document Types

### 3.1 Standard Operating Procedure (SOP)

**Purpose:** Step-by-step guide for a routine, repeatable process.

**SOP Template:**

```
FLLC Enterprise — Standard Operating Procedure
================================================
Title:          [Procedure Name]
SOP Number:     FLLC-SOP-XXXX
Version:        1.0
Effective Date: [Date]
Author:         [Name]
Approved By:    [Manager Name]
Review Date:    [Date + 1 year]

1. PURPOSE
   [Why this procedure exists]

2. SCOPE
   [What systems/processes this covers]

3. PREREQUISITES
   - [Required access/tools]
   - [Required knowledge]

4. PROCEDURE
   Step 1: [Action]
   Step 2: [Action]
   Step 3: [Action]
   ...

5. VERIFICATION
   [How to confirm the procedure succeeded]

6. TROUBLESHOOTING
   [Common issues and resolutions]

7. REVISION HISTORY
   | Version | Date | Author | Changes |
   |---------|------|--------|---------|
   | 1.0     |      |        | Initial |
```

### 3.2 Runbook

**Purpose:** Operational guide for responding to specific events or performing
maintenance tasks, typically used by on-call engineers.

| Section                | Content                                          |
|------------------------|--------------------------------------------------|
| Overview               | What this runbook covers and when to use it      |
| Detection              | How the issue is identified (alert, user report) |
| Diagnosis              | Steps to determine root cause                    |
| Resolution             | Actions to fix the issue                         |
| Escalation             | When and how to escalate                         |
| Post-Resolution        | Cleanup, monitoring, follow-up tasks             |
| Related Runbooks       | Links to related procedures                      |

### 3.3 Incident Report

**Purpose:** Document what happened during an incident for learning and
compliance.

| Section                  | Content                                        |
|--------------------------|------------------------------------------------|
| Incident Summary         | One-paragraph overview                         |
| Timeline                 | Chronological events with timestamps           |
| Impact                   | Who/what was affected, duration, severity      |
| Root Cause               | Technical explanation of why it happened        |
| Resolution               | What was done to fix it                        |
| Lessons Learned          | What went well, what didn't                    |
| Action Items             | Preventive measures with owners and deadlines  |

### 3.4 Project Proposal

**Purpose:** Convince stakeholders to approve a project by presenting the
business case.

| Section               | Content                                          |
|-----------------------|--------------------------------------------------|
| Executive Summary     | One-page overview of the proposal                |
| Problem Statement     | What issue this project addresses                |
| Proposed Solution     | What you plan to do and why                      |
| Alternatives Considered| Other options and why they were rejected         |
| Cost-Benefit Analysis | Investment required vs expected returns          |
| Timeline              | Major milestones and deadlines                   |
| Risks                 | Potential issues and mitigation strategies        |
| Resource Requirements | People, hardware, software, budget               |

---

## 4. Email Etiquette for Professional IT Communication

### 4.1 Email Structure

| Component      | Best Practice                                       |
|----------------|-----------------------------------------------------|
| Subject Line   | Specific and actionable: "[Action Needed] Server Patch Schedule" |
| Greeting       | Professional: "Hi [Name]," or "Hello Team,"        |
| Opening        | State purpose immediately: "I'm writing to request..."|
| Body           | One topic per email; use bullets for multiple points|
| Closing        | Clear next step: "Please respond by Friday."        |
| Signature      | Name, title, contact info, organization             |

### 4.2 Email Do's and Don'ts

| Do                                           | Don't                                        |
|----------------------------------------------|----------------------------------------------|
| Use a descriptive subject line               | Leave subject blank or write "Hi"            |
| Keep it concise (under 5 paragraphs)         | Write walls of text                          |
| Proofread before sending                     | Send with typos or wrong recipient           |
| Use CC for awareness, TO for action needed   | CC everyone "just in case"                   |
| Respond within 24 hours (business days)      | Leave emails unanswered for days             |
| Use BCC for large distribution lists         | Expose everyone's email via CC               |
| Include attachments mentioned in the body    | Reference attachments you forgot to attach   |
| Use a professional tone                      | Use sarcasm or passive-aggressive language   |

### 4.3 Escalation Email Template

```
Subject: [ESCALATION] [System] — [Brief Issue Description]

Hi [Manager/Team Lead],

I'm escalating [issue description] because [reason for escalation].

Current Status:
- Impact: [who/what is affected]
- Duration: [how long it's been ongoing]
- Actions Taken: [what has been tried]

Request:
- [Specific help or decision needed]

Timeline: [Urgency — when this needs to be resolved]

Please let me know if you need additional information.

Best regards,
[Your Name]
```

---

## 5. Meeting Facilitation and Agendas

### 5.1 Meeting Agenda Template

```
FLLC Enterprise — Meeting Agenda
==================================
Meeting:     [Meeting Name]
Date/Time:   [Date] at [Time] ([Duration])
Location:    [Room / Video Link]
Facilitator: [Name]
Attendees:   [Names]

AGENDA
------
1. [Topic] — [Owner] — [Time Allotment]
   Purpose: [Inform / Discuss / Decide]

2. [Topic] — [Owner] — [Time Allotment]
   Purpose: [Inform / Discuss / Decide]

3. Action Item Review — [Facilitator] — [5 min]

4. Open Floor / Parking Lot — [5 min]

PREPARATION
-----------
- Please review [document/link] before the meeting
- Bring [relevant materials]
```

### 5.2 Meeting Facilitation Tips

| Phase         | Best Practice                                       |
|---------------|-----------------------------------------------------|
| Before        | Send agenda 24+ hours in advance                    |
| Opening       | State purpose and expected outcomes                 |
| During        | Keep discussion on track; manage time               |
| Participation | Invite quieter members to contribute                |
| Decisions     | Summarize decisions clearly before moving on        |
| Parking Lot   | Capture off-topic items for later discussion        |
| Closing       | Review action items: who, what, by when             |
| After         | Send meeting notes within 24 hours                  |

### 5.3 Meeting Types in IT

| Meeting Type       | Purpose                            | Frequency   | Duration     |
|--------------------|------------------------------------|-------------|--------------|
| Daily Standup      | Team sync on progress/blockers     | Daily       | 15 minutes   |
| Sprint Planning    | Plan upcoming work                 | Biweekly    | 1-2 hours    |
| Retrospective      | Reflect on process improvements    | Biweekly    | 1 hour       |
| Architecture Review| Evaluate design decisions          | As needed   | 1-2 hours    |
| Incident Review    | Learn from production incidents    | After P1/P2 | 1 hour       |
| 1-on-1              | Manager/report relationship       | Weekly      | 30 minutes   |

---

## 6. Presentation Design Principles

### 6.1 Slide Design Guidelines

| Principle           | Guideline                                          |
|---------------------|----------------------------------------------------|
| One idea per slide  | Don't overcrowd; split complex topics              |
| 6x6 Rule           | Max 6 bullet points with max 6 words each          |
| Visual hierarchy    | Use size, color, and position to guide the eye     |
| High contrast       | Ensure text is readable against background         |
| Consistent theme    | Use the same fonts, colors, and layout throughout  |
| Minimal text        | Slides support your talk — they don't replace it   |
| Quality images      | Use high-resolution, relevant images               |

### 6.2 Data Visualization in Presentations

| Data Type               | Best Chart Type                              |
|-------------------------|----------------------------------------------|
| Trends over time        | Line chart                                   |
| Category comparison     | Bar chart (vertical or horizontal)           |
| Part-to-whole           | Pie chart (max 5-6 segments) or stacked bar  |
| Correlation             | Scatter plot                                 |
| Geographic data         | Map/heat map                                 |
| Process flow            | Flowchart or diagram                         |

---

## 7. Writing for Different Stakeholders

### 7.1 Adapting the Same Information

**Scenario:** A database migration is required.

| Audience          | Message Focus                                       |
|-------------------|-----------------------------------------------------|
| CTO               | "This migration reduces licensing costs by 40% and improves scalability." |
| Dev Team          | "We're moving from MySQL 5.7 to PostgreSQL 15. Here's the migration plan and timeline." |
| End Users         | "The system will be unavailable Saturday 2-6 AM for a scheduled upgrade." |
| Finance           | "The new database saves $50K/year in licensing while supporting 3x growth." |
| Compliance Team   | "The new platform meets SOC 2 requirements. Here's the data handling documentation." |

### 7.2 The Inverted Pyramid (for Technical Reports)

```
┌─────────────────────────────────────┐  ← Most important: conclusion/recommendation
│         Key Finding / Action        │
├─────────────────────────────────────┤  ← Supporting details and evidence
│      Supporting Details             │
│      Data and Analysis              │
├─────────────────────────────────────┤  ← Background for those who want full context
│   Background / Methodology          │
│   Detailed Technical Information    │
└─────────────────────────────────────┘
```

This structure allows executives to read only the top and still understand the message,
while technical readers can continue for full detail.

---

## 8. FLLC Documentation Standards

### 8.1 Required Document Elements

| Element               | Requirement                                       |
|-----------------------|---------------------------------------------------|
| Header                | Title, author, date, version, organization        |
| Classification        | Public, Internal, Confidential, or Restricted     |
| Table of Contents     | Required for documents over 5 pages               |
| Version History       | Required; track all changes                       |
| Review/Approval       | Documented reviewer and approver                  |
| References            | Cite sources, related docs, and external links    |

### 8.2 FLLC Naming Convention

```
Format: FLLC-[DocType]-[System]-[Subject]-v[Version].[ext]

Examples:
  FLLC-SOP-AD-UserProvisioning-v2.1.md
  FLLC-RB-WEB-DeploymentRollback-v1.0.md
  FLLC-IR-DB-OutageJan2026-v1.0.md
  FLLC-PP-CLOUD-AWSMigration-v1.0.md

Document Type Codes:
  SOP  = Standard Operating Procedure
  RB   = Runbook
  IR   = Incident Report
  PP   = Project Proposal
  AR   = Architecture Review
  TG   = Training Guide
```

### 8.3 FLLC Review Process

| Step | Action                               | Responsible          | Timeline      |
|------|--------------------------------------|----------------------|---------------|
| 1    | Author creates/updates document      | Author               | —             |
| 2    | Technical review                     | Subject matter expert | 3 business days|
| 3    | Editorial review                     | Team lead or peer    | 2 business days|
| 4    | Approval                             | Department manager   | 2 business days|
| 5    | Publication                          | Author               | 1 business day |
| 6    | Announcement                         | Author               | Same day       |

### 8.4 Documentation Quality Checklist

| Category         | Checklist Item                                       |
|------------------|------------------------------------------------------|
| Accuracy         | All commands and procedures tested and verified      |
| Completeness     | All prerequisite steps included                      |
| Clarity          | No ambiguous language or undefined acronyms          |
| Formatting       | Consistent headings, lists, and code formatting      |
| Links            | All internal and external links verified             |
| Versioning       | Version number and date updated                      |
| Accessibility    | Screenshots have descriptive alt text                |
| Spelling/Grammar | Proofread; no typos or grammatical errors            |

---

## References

- Markel, M. & Selber, S. — *Technical Communication*
- Microsoft Writing Style Guide
- Google Developer Documentation Style Guide
- Red Hat Documentation Style Guide

---

*FLLC Enterprise — Professional Development Division*
*Author: Preston Furulie | Portland Community College | Spring 2026*
