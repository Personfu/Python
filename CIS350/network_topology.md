# Network Topology Design Document
## CIS 350 — Network & Cybersecurity | Preston Furulie

---

## 1. Network Overview

### 1.1 Design Philosophy
This enterprise network uses a **hub-and-spoke topology with DMZ segmentation** following defense-in-depth principles. Network segments are isolated by function using VLANs, with inter-VLAN traffic controlled by firewall policies. The design supports 200+ endpoints across one headquarters and two branch offices.

### 1.2 Addressing Scheme

| Segment            | VLAN ID | Subnet           | Usable Hosts | Gateway       | Purpose                      |
|--------------------|---------|------------------|--------------|---------------|-------------------------------|
| Management         | 10      | 10.0.10.0/24     | 254          | 10.0.10.1     | Network devices, admin access |
| Corporate          | 20      | 10.0.20.0/24     | 254          | 10.0.20.1     | Employee workstations         |
| Servers            | 30      | 10.0.30.0/24     | 254          | 10.0.30.1     | Internal application/DB servers|
| VoIP               | 40      | 10.0.40.0/24     | 254          | 10.0.40.1     | IP phones and conferencing    |
| Guest              | 50      | 10.0.50.0/24     | 254          | 10.0.50.1     | Isolated guest Wi-Fi          |
| IoT / Cameras      | 60      | 10.0.60.0/24     | 254          | 10.0.60.1     | Security cameras, sensors     |
| DMZ                | 100     | 172.16.0.0/24    | 254          | 172.16.0.1    | Public-facing web servers     |
| WAN / Internet     | —       | ISP-assigned /30 | 2            | ISP gateway   | Internet uplink               |

### 1.3 Network Diagram (Logical)

```
                        ┌──────────────┐
                        │   INTERNET   │
                        └──────┬───────┘
                               │ ISP Uplink (1 Gbps Fiber)
                               │ + Backup (500 Mbps Cable)
                               ▼
                    ┌──────────────────────┐
                    │  Palo Alto PA-850    │
                    │  Next-Gen Firewall   │
                    │  (Zone-based FW)     │
                    └──────┬──────┬───────┘
                           │      │
              ┌────────────┘      └────────────┐
              ▼                                 ▼
    ┌─────────────────┐              ┌─────────────────┐
    │   DMZ Switch    │              │   Core Switch   │
    │   (VLAN 100)    │              │  Cisco Cat 9300 │
    │                 │              │  (Layer 3)      │
    │  - Web Server   │              └──┬──┬──┬──┬──┬──┘
    │  - Rev Proxy    │                 │  │  │  │  │
    │  - Mail Relay   │                 │  │  │  │  │
    └─────────────────┘                 │  │  │  │  │
                           ┌────────────┘  │  │  │  └────────────┐
                           ▼               ▼  │  ▼               ▼
                    ┌───────────┐  ┌────────┐ │ ┌────────┐ ┌───────────┐
                    │  VLAN 10  │  │VLAN 20 │ │ │VLAN 40 │ │  VLAN 50  │
                    │Management │  │Corporate│ │ │  VoIP  │ │  Guest    │
                    └───────────┘  └────────┘ │ └────────┘ └───────────┘
                                              │
                                       ┌──────┘
                                       ▼
                                ┌───────────┐
                                │  VLAN 30  │
                                │  Servers  │
                                │           │
                                │ App Server│
                                │ DB Server │
                                │ File Srv  │
                                └───────────┘
```

---

## 2. Core Equipment Specifications

### 2.1 Hardware Inventory

| Device                          | Qty | Role              | Key Specs                                    |
|---------------------------------|-----|-------------------|----------------------------------------------|
| Palo Alto PA-850                | 1   | Perimeter Firewall| 1.9 Gbps throughput, IPS, URL filtering, SSL decrypt |
| Cisco Catalyst 9300-48P         | 2   | Core/Distribution | 48-port PoE+, Layer 3, stacking, 480 Gbps    |
| Cisco Catalyst 9200-24P         | 4   | Access Switches   | 24-port PoE+, Layer 2, 128 Gbps              |
| Cisco Meraki MR46               | 8   | Wireless APs      | Wi-Fi 6 (802.11ax), 3.5 Gbps, cloud managed  |
| Cisco ISR 4331                   | 1   | WAN Router        | Dual WAN, BGP/OSPF, 300 Mbps throughput       |
| APC Smart-UPS 3000              | 3   | UPS               | 2700W, 30-min runtime at 50% load             |

### 2.2 Server Infrastructure

| Server            | OS              | CPU         | RAM   | Storage          | Function          |
|-------------------|-----------------|-------------|-------|------------------|-------------------|
| Web Server (DMZ)  | Ubuntu 22.04    | 8 vCPU      | 16 GB | 500 GB SSD       | Nginx reverse proxy|
| App Server        | Ubuntu 22.04    | 16 vCPU     | 32 GB | 1 TB SSD         | Node.js API        |
| Database Server   | Ubuntu 22.04    | 16 vCPU     | 64 GB | 2 TB NVMe RAID10 | MySQL 8.0          |
| File Server       | Windows Server  | 8 vCPU      | 16 GB | 4 TB RAID5       | SMB file shares    |
| Domain Controller | Windows Server  | 4 vCPU      | 8 GB  | 500 GB SSD       | AD DS, DNS, DHCP   |

---

## 3. Security Zones

### 3.1 Zone Definitions

| Zone       | Trust Level | Description                                     | Allowed Outbound        |
|------------|-------------|-------------------------------------------------|------------------------|
| Outside    | 0 (Untrusted) | Internet / WAN                               | N/A (source)           |
| DMZ        | 25          | Public-facing services with limited access       | Outside (HTTP/S only)  |
| Guest      | 30          | Visitor network, isolated from internal          | Outside (filtered)     |
| Corporate  | 70          | Employee workstations                            | Outside, Servers       |
| Servers    | 80          | Internal application and database servers        | Corporate (response)   |
| Management | 90          | Network devices and admin interfaces             | All (admin access)     |

### 3.2 Inter-Zone Policy Summary

| Source Zone  | Dest Zone    | Allowed                                      | Denied           |
|-------------|-------------|----------------------------------------------|------------------|
| Outside     | DMZ         | TCP 80, 443 (web only)                        | Everything else  |
| Outside     | Corporate   | VPN tunnel only (IPSec)                       | Direct access    |
| DMZ         | Servers     | TCP 3306 (MySQL), TCP 6379 (Redis)            | All other        |
| Corporate   | Servers     | TCP 80, 443, 3389 (RDP), 22 (SSH), 3306      | P2P, Torrents    |
| Corporate   | Outside     | TCP 80, 443, 53 (DNS), 587 (mail)             | IRC, Torrents    |
| Guest       | Outside     | TCP 80, 443 (web browsing only)               | All internal     |
| Guest       | Corporate   | **DENY ALL**                                   | Complete block   |
| Management  | All         | Full access (admin)                           | None             |
| IoT         | Servers     | TCP 443 (API only, camera feeds)              | All other        |
| IoT         | Outside     | **DENY ALL**                                   | No internet      |

---

## 4. Wireless Design

### 4.1 SSIDs

| SSID            | VLAN | Security      | Band    | Purpose              |
|-----------------|------|---------------|---------|----------------------|
| CORP-SECURE     | 20   | WPA3-Enterprise| 5 GHz  | Employee devices     |
| CORP-VOIP       | 40   | WPA3-Enterprise| 5 GHz  | IP phones            |
| GUEST-WIFI      | 50   | WPA3-Personal | 2.4/5  | Visitors (captive portal)|

### 4.2 AP Placement
- One AP per 2,500 sq ft with 30% overlap for roaming
- Channel planning: non-overlapping channels (1, 6, 11 for 2.4 GHz)
- Transmit power: auto-adjusted by Meraki cloud controller
- Band steering: prefer 5 GHz for capable clients

---

## 5. Redundancy & High Availability

| Component       | Redundancy Method                        | Failover Time |
|-----------------|------------------------------------------|---------------|
| Internet        | Dual ISP with BGP failover               | < 30 seconds  |
| Core Switch     | VSS stack (2x Catalyst 9300)             | Sub-second    |
| Firewall        | Active/Passive HA pair                   | < 5 seconds   |
| Power           | Dual PSU + UPS + Generator               | 0 (seamless)  |
| Database        | Primary/Replica with auto-failover       | < 60 seconds  |
| DNS             | Primary DC + Secondary DC                | Automatic     |

---

## 6. Monitoring & Management

| Tool                | Function                              | Protocol      |
|---------------------|---------------------------------------|---------------|
| PRTG Network Monitor| Bandwidth, uptime, health             | SNMP v3       |
| Palo Alto Panorama  | Centralized firewall management       | HTTPS         |
| Cisco Meraki Dashboard | Wireless AP management             | Cloud API     |
| Syslog Server (Graylog)| Centralized log aggregation        | Syslog/TLS    |
| Nessus Professional | Vulnerability scanning                | Agent-based   |
| Wireshark           | Packet capture and analysis           | SPAN port     |
