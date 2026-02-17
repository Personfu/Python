# Network Topology Design
## CIS 350 — Network & Cybersecurity | Preston Furulie

## Enterprise Network Topology

**Design:** Hub-and-spoke with DMZ segmentation

## Network Segments

- **VLAN 10 — Management:** 10.0.10.0/24 (switches, APs, admin)
- **VLAN 20 — Corporate:** 10.0.20.0/24 (employee workstations)
- **VLAN 30 — Servers:** 10.0.30.0/24 (internal app/DB servers)
- **VLAN 40 — Guest:** 10.0.40.0/24 (isolated guest Wi-Fi)
- **DMZ:** 172.16.0.0/24 (web servers, reverse proxy)

## Core Equipment

- Cisco Catalyst 9300 Core Switch (Layer 3 routing)
- Palo Alto PA-850 Next-Gen Firewall
- Cisco Meraki MR46 Wireless Access Points
- Redundant ISP connections with BGP failover

## Security Zones

- **Untrusted:** Internet-facing (DMZ)
- **Semi-trusted:** Corporate network (VLAN 20)
- **Trusted:** Server farm (VLAN 30), Management (VLAN 10)
