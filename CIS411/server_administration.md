# Server Administration — Comprehensive Guide

## CIS 411 | Portland Community College | Spring 2026

| Field             | Value                              |
|-------------------|------------------------------------|
| **Author**        | Preston Furulie                    |
| **Organization**  | FLLC Enterprise                    |
| **Department**    | Platform Engineering               |
| **Alignment**     | CompTIA Server+ (SK0-005)          |

---

## 1. Server Hardware Fundamentals

### 1.1 Rack Units and Form Factors

Enterprise servers are measured in **rack units (U)**, where 1U = 1.75 inches (44.45mm)
of vertical space in a standard 19-inch equipment rack.

| Form Factor  | Height | Typical Use Case                          |
|--------------|--------|-------------------------------------------|
| 1U           | 1.75"  | Web servers, lightweight applications      |
| 2U           | 3.5"   | Database servers, storage-heavy workloads  |
| 4U           | 7.0"   | GPU compute, high-density storage          |
| Blade        | Varies | High-density virtualization hosts          |
| Tower        | N/A    | Small office / branch office               |

### 1.2 Server Components

| Component         | Server-Grade Feature                            |
|-------------------|------------------------------------------------|
| CPU               | Multi-socket, ECC support, higher core counts   |
| RAM               | ECC (Error-Correcting Code), registered DIMMs   |
| Storage           | SAS drives, NVMe, hardware RAID controllers     |
| NIC               | Dual or quad-port, 10GbE/25GbE, teaming support |
| Power Supply      | Redundant (1+1), hot-swappable                  |
| Cooling           | Redundant fans, hot/cold aisle design            |
| Management        | BMC/IPMI, iDRAC (Dell), iLO (HPE), IMM (Lenovo)|

### 1.3 RAID Levels

RAID (Redundant Array of Independent Disks) provides fault tolerance and/or
performance improvements for server storage.

| RAID Level | Min Disks | Fault Tolerance | Usable Capacity      | Performance    | Use Case                    |
|------------|-----------|-----------------|----------------------|----------------|-----------------------------|
| RAID 0     | 2         | None            | 100% (N disks)       | Highest read/write | Temporary data, scratch     |
| RAID 1     | 2         | 1 disk failure  | 50% (N/2)           | Good read, normal write | OS drives, critical data   |
| RAID 5     | 3         | 1 disk failure  | (N-1) disks          | Good read, slower write | File servers, general use  |
| RAID 6     | 4         | 2 disk failures | (N-2) disks          | Good read, slowest write | Large arrays, archives     |
| RAID 10    | 4         | 1 per mirror    | 50% (N/2)           | Excellent read/write | Databases, high I/O        |

**Key Terms:**
- **Hot spare**: A standby disk automatically used when an active disk fails
- **Cold spare**: A replacement disk kept on-site but not installed until needed
- **Rebuild time**: Duration to reconstruct data onto a replacement disk
- **Write penalty**: Additional I/O operations for parity-based RAID (5, 6)

### 1.4 Storage Technologies

| Technology | Interface | Typical Speed   | Use Case                   |
|------------|-----------|-----------------|----------------------------|
| HDD (SAS)  | SAS       | 200-250 MB/s    | Bulk storage, backups      |
| HDD (SATA) | SATA      | 150-200 MB/s    | Cold storage, archives     |
| SSD (SATA) | SATA      | 500-550 MB/s    | General purpose, OS drives |
| SSD (NVMe) | PCIe      | 3,000-7,000 MB/s| Databases, high-performance|

---

## 2. Server Roles and Services

### 2.1 Common Server Roles

| Server Role       | Function                                      | Example Software                  |
|-------------------|-----------------------------------------------|-----------------------------------|
| File Server       | Centralized file storage and sharing           | Windows File Services, Samba, NFS |
| Print Server      | Manages network printers and print queues      | Windows Print Services, CUPS      |
| Web Server        | Hosts websites and web applications            | Apache, Nginx, IIS                |
| Database Server   | Stores and manages structured data             | SQL Server, MySQL, PostgreSQL     |
| Mail Server       | Handles email sending, receiving, storage      | Exchange, Postfix, Dovecot        |
| DNS Server        | Resolves domain names to IP addresses          | Windows DNS, BIND, Unbound        |
| DHCP Server       | Assigns IP addresses dynamically               | Windows DHCP, ISC DHCP, Kea       |
| Directory Server  | Centralized authentication and authorization   | Active Directory, OpenLDAP, FreeIPA|
| Proxy Server      | Intermediary for client requests               | Squid, HAProxy, Nginx             |
| Monitoring Server | Collects and analyzes system metrics           | Nagios, Zabbix, Prometheus        |

### 2.2 Service Dependencies

Understanding dependencies prevents cascading failures:

```
DNS Server
  └── Active Directory (requires DNS)
        └── DHCP (can integrate with AD)
        └── File Server (uses AD authentication)
        └── Print Server (uses AD authentication)
        └── Web Server (can use AD SSO)
```

---

## 3. Windows Server vs Linux Server

### 3.1 Feature Comparison

| Feature              | Windows Server                  | Linux Server                    |
|----------------------|---------------------------------|---------------------------------|
| License Cost         | Per-core licensing, CALs        | Free (most distributions)       |
| GUI                  | Full GUI or Server Core         | CLI-first, optional GUI         |
| Directory Service    | Active Directory                | OpenLDAP, FreeIPA, Samba AD     |
| Package Management   | Windows Update, WSUS            | apt, yum/dnf, zypper            |
| Shell/Scripting      | PowerShell, CMD                 | Bash, Zsh, Python               |
| Remote Management    | RDP, WinRM, PowerShell Remoting | SSH, Cockpit, Webmin            |
| File System          | NTFS, ReFS                      | ext4, XFS, Btrfs, ZFS          |
| Containerization     | Windows Containers, WSL2        | Native Docker, Podman, LXC      |
| Market Share         | ~72% (enterprise desktops/AD)   | ~96% (web servers, cloud)       |
| Typical Workloads    | AD, Exchange, SQL Server, .NET  | Web, databases, containers, HPC |

### 3.2 Administration Commands Comparison

| Task                    | Windows (PowerShell)                | Linux (Bash)                      |
|-------------------------|-------------------------------------|-----------------------------------|
| List services           | `Get-Service`                       | `systemctl list-units`            |
| Start service           | `Start-Service <name>`              | `systemctl start <name>`          |
| Check disk space        | `Get-PSDrive`                       | `df -h`                           |
| View processes          | `Get-Process`                       | `ps aux` or `top`                 |
| Network config          | `Get-NetIPAddress`                  | `ip addr show`                    |
| User management         | `New-ADUser`                        | `useradd`                         |
| Firewall rules          | `New-NetFirewallRule`               | `firewall-cmd` or `iptables`      |
| View event logs         | `Get-EventLog`                      | `journalctl`                      |

---

## 4. Active Directory Concepts

### 4.1 Active Directory Structure

Active Directory Domain Services (AD DS) is the cornerstone of Windows enterprise
identity management.

**Logical Components:**

| Component        | Description                                              |
|------------------|----------------------------------------------------------|
| **Domain**       | Security boundary with shared authentication database    |
| **Forest**       | Collection of one or more domains sharing a schema       |
| **Tree**         | Hierarchy of domains sharing a contiguous namespace      |
| **OU**           | Organizational Unit — container for organizing objects   |
| **Site**         | Physical network location for replication optimization   |
| **Trust**        | Relationship enabling cross-domain authentication        |

**Physical Components:**

| Component              | Description                                        |
|------------------------|----------------------------------------------------|
| Domain Controller (DC) | Server running AD DS, hosts a copy of the database |
| Global Catalog (GC)    | Partial replica of all objects in the forest       |
| FSMO Roles             | Five specialized operations master roles           |
| AD Database (NTDS.dit) | The physical database file storing all AD objects  |

### 4.2 Group Policy

Group Policy Objects (GPOs) enforce configuration across domain-joined machines.

**GPO Processing Order (LSDOU):**
1. **L**ocal Policy
2. **S**ite-linked GPOs
3. **D**omain-linked GPOs
4. **O**U-linked GPOs (nested OUs processed parent to child)

**Common GPO Settings:**

| Category             | Example Settings                                  |
|----------------------|---------------------------------------------------|
| Password Policy      | Minimum length, complexity, history, max age      |
| Account Lockout      | Threshold, duration, reset counter                |
| Software Deployment  | MSI package installation/removal                  |
| Drive Mapping        | Map network drives based on group membership      |
| Desktop Restrictions | Disable Control Panel, restrict removable media   |
| Security Settings    | Audit policies, user rights assignment            |

### 4.3 FSMO Roles

| Role                          | Scope   | Function                                |
|-------------------------------|---------|-----------------------------------------|
| Schema Master                 | Forest  | Controls schema modifications           |
| Domain Naming Master          | Forest  | Manages adding/removing domains         |
| PDC Emulator                  | Domain  | Password changes, time sync, GPO master |
| RID Master                    | Domain  | Allocates RID pools to DCs              |
| Infrastructure Master         | Domain  | Resolves cross-domain references        |

---

## 5. User and Group Management

### 5.1 Account Types

| Account Type      | Description                                    |
|-------------------|------------------------------------------------|
| Local User        | Exists on a single machine only                |
| Domain User       | Exists in AD, can authenticate across domain   |
| Service Account   | Used by applications/services, not humans      |
| Managed Service   | gMSA — AD manages password rotation            |
| Computer Account  | Represents a domain-joined machine             |

### 5.2 Group Types and Scopes

| Group Scope     | Members Can Include                        | Can Access Resources In        |
|-----------------|--------------------------------------------|--------------------------------|
| Domain Local    | Any account in the forest                  | Same domain only               |
| Global          | Accounts from same domain                  | Any domain in the forest       |
| Universal       | Any account in the forest                  | Any domain in the forest       |

**Best Practice — AGDLP Model:**
- **A**ccounts → **G**lobal groups → **D**omain **L**ocal groups → **P**ermissions

### 5.3 Permission Models

**NTFS Permissions:**

| Permission       | Files                          | Folders                         |
|------------------|--------------------------------|---------------------------------|
| Read             | View contents, attributes      | List contents                   |
| Write            | Modify contents                | Create files/subfolders         |
| Read & Execute   | Read + run executables         | Read + traverse folder          |
| Modify           | Read + Write + Delete          | Read + Write + Delete           |
| Full Control     | All permissions + change perms | All permissions + change perms  |

**Share Permissions:**

| Permission  | Description                                           |
|-------------|-------------------------------------------------------|
| Read        | View files and subfolders                             |
| Change      | Read + Add/Modify/Delete files                        |
| Full Control| Change + Modify permissions                           |

**Effective Permissions:** When both NTFS and share permissions apply, the most
restrictive combination wins.

---

## 6. Server Monitoring

### 6.1 Performance Counters (Windows)

| Counter                          | Threshold          | Action if Exceeded           |
|----------------------------------|--------------------|------------------------------|
| Processor: % Processor Time      | > 85% sustained    | Add CPU, optimize workload   |
| Memory: Available MBytes         | < 10% of total     | Add RAM, check for leaks     |
| Disk: % Disk Time                | > 90% sustained    | Upgrade to SSD, add spindles |
| Disk: Avg Disk Queue Length      | > 2 per disk       | Storage bottleneck           |
| Network: Bytes Total/sec         | > 70% of bandwidth | Upgrade NIC, add bandwidth   |
| Network: Output Queue Length     | > 2                | Network congestion           |

### 6.2 Event Logs

| Log              | Contents                                           |
|------------------|----------------------------------------------------|
| System           | OS events, driver issues, service status changes   |
| Application      | Application-specific events and errors             |
| Security         | Login attempts, audit events, policy changes       |
| Setup            | Windows Update and component installation          |
| Forwarded Events | Events collected from remote systems               |

**Event Severity Levels:**
- **Critical**: Unrecoverable failure
- **Error**: Significant problem, functionality lost
- **Warning**: Potential issue, not yet critical
- **Information**: Normal operational events
- **Verbose**: Detailed diagnostic information

### 6.3 SNMP (Simple Network Management Protocol)

| Component       | Role                                             |
|-----------------|--------------------------------------------------|
| Manager (NMS)   | Polls agents, receives traps, stores data        |
| Agent           | Runs on managed device, responds to queries      |
| MIB             | Management Information Base — defines metrics    |
| OID             | Object Identifier — unique metric address        |
| Community String| Authentication credential (v1/v2c)               |
| Trap            | Unsolicited alert from agent to manager          |

**SNMP Versions:**
- **v1**: Basic, community string auth, no encryption
- **v2c**: Improved performance, still no encryption
- **v3**: Authentication + encryption (recommended)

---

## 7. Capacity Planning and Baselining

### 7.1 Baselining Process

1. **Identify metrics**: CPU, memory, disk I/O, network throughput
2. **Collect data**: Minimum 30 days during normal operations
3. **Establish thresholds**: Define normal vs abnormal ranges
4. **Document baseline**: Record results with timestamps and conditions
5. **Review regularly**: Update baselines quarterly or after major changes

### 7.2 Capacity Planning Methodology

| Phase          | Activities                                          |
|----------------|-----------------------------------------------------|
| Assessment     | Inventory current resources and utilization          |
| Forecasting    | Project growth based on business plans and trends    |
| Modeling       | Simulate scenarios (what-if analysis)                |
| Planning       | Determine procurement timeline and budget            |
| Implementation | Deploy additional resources before saturation        |
| Validation     | Confirm new capacity meets projected demand          |

### 7.3 Key Metrics for Planning

| Resource  | Planning Metric                    | Growth Trigger          |
|-----------|------------------------------------|-------------------------|
| CPU       | Average utilization trend          | > 70% sustained average |
| Memory    | Peak usage vs installed            | Peak > 80% installed    |
| Storage   | Growth rate (GB/month)             | < 20% free remaining    |
| Network   | Peak bandwidth utilization         | > 60% sustained peak    |
| Users     | Concurrent sessions trend          | Within 80% of license   |

### 7.4 FLLC Enterprise Baseline Template

```
FLLC Enterprise — Server Baseline Report
=========================================
Server Name:     ____________________
Date:            ____________________
Collected By:    ____________________
Collection Period: 30 days (start: ____ end: ____)

CPU Utilization:    Avg: ____%   Peak: ____%
Memory Usage:       Avg: ____MB  Peak: ____MB / ____MB Total
Disk I/O (Read):    Avg: ____MB/s  Peak: ____MB/s
Disk I/O (Write):   Avg: ____MB/s  Peak: ____MB/s
Disk Space Used:    ____GB / ____GB Total (___%)
Network In:         Avg: ____Mbps  Peak: ____Mbps
Network Out:        Avg: ____Mbps  Peak: ____Mbps
Active Connections: Avg: ____  Peak: ____

Notes: ____________________________________________
Recommendations: __________________________________
```

---

## 8. Server Hardening Checklist

| Category          | Action                                              |
|-------------------|-----------------------------------------------------|
| OS Updates        | Apply all security patches within 30 days           |
| Services          | Disable unnecessary services and roles              |
| Accounts          | Rename default admin, enforce strong passwords      |
| Firewall          | Enable host firewall, allow only required ports     |
| Remote Access     | Use encrypted protocols only (SSH, RDP with NLA)    |
| Auditing          | Enable logon, object access, and policy change audits|
| Antivirus         | Install and update endpoint protection              |
| Encryption        | Enable BitLocker (Windows) or LUKS (Linux) at rest  |
| Backup            | Configure and test regular backup schedule          |
| Documentation     | Maintain current as-built and change records        |

---

## References

- CompTIA Server+ SK0-005 Exam Objectives
- Microsoft Windows Server Documentation
- Red Hat Enterprise Linux System Administration Guide
- NIST SP 800-123: Guide to General Server Security

---

*FLLC Enterprise — Platform Engineering Division*
*Author: Preston Furulie | Portland Community College | Spring 2026*
