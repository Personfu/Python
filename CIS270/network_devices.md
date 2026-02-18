# Network Devices & Infrastructure

**FLLC Enterprise IT — Phase 11: Computer Networking**
**CIS 270 — Computer Networking | Preston Furulie**
**Spring 2026 | Portland Community College**
**CompTIA Network+ (N10-009) Aligned**

---

## Hub vs Switch vs Router — Comparison Table

| Feature             | Hub                          | Switch                          | Router                          |
|---------------------|------------------------------|---------------------------------|---------------------------------|
| **OSI Layer**       | Layer 1 (Physical)           | Layer 2 (Data Link)             | Layer 3 (Network)               |
| **Addressing**      | None — repeats to all ports  | MAC addresses                   | IP addresses                    |
| **Collision Domain**| Single (all ports share)     | One per port (micro-segmented)  | One per interface               |
| **Broadcast Domain**| Single                       | Single (per VLAN)               | Separates broadcast domains     |
| **Intelligence**    | None                         | MAC address table (CAM table)   | Routing table                   |
| **Duplex**          | Half-duplex                  | Full-duplex                     | Full-duplex                     |
| **Speed**           | Shared bandwidth             | Dedicated bandwidth per port    | WAN/LAN interface speeds        |
| **Use Case**        | Legacy/obsolete              | LAN connectivity                | Inter-network routing           |
| **Security**        | None — all traffic visible   | Port security, VLANs            | ACLs, NAT, firewalling          |

### Key Takeaways

- **Hubs** are obsolete — replaced by switches in modern networks.
- **Switches** forward frames based on MAC address tables; reduce collisions.
- **Routers** forward packets based on IP routing tables; connect different networks.
- A **Layer 3 switch** combines switching and routing in a single device.

---

## Layer 2 vs Layer 3 Switching

| Feature                | Layer 2 Switch                    | Layer 3 Switch                     |
|------------------------|-----------------------------------|------------------------------------|
| **Forwarding Basis**   | MAC addresses                     | MAC addresses + IP addresses       |
| **Routing**            | No                                | Yes (inter-VLAN routing)           |
| **VLANs**              | Creates VLANs, no routing between | Creates VLANs + routes between them|
| **Protocols**          | STP, LLDP, CDP                    | STP, OSPF, EIGRP, static routes   |
| **Performance**        | Wire-speed L2 forwarding          | Wire-speed L2 + hardware L3       |
| **Cost**               | Lower                             | Higher                             |
| **Typical Placement**  | Access layer                      | Distribution / Core layer          |

### Inter-VLAN Routing Methods

1. **Router-on-a-Stick** — Single router interface with 802.1Q sub-interfaces.
2. **Layer 3 Switch** — SVIs (Switched Virtual Interfaces) for each VLAN.
3. **Dedicated Router Interfaces** — One physical interface per VLAN (least scalable).

---

## Wireless Access Points — IEEE 802.11 Standards

| Standard   | Frequency       | Max Speed     | Year | Notes                             |
|------------|-----------------|---------------|------|-----------------------------------|
| 802.11a    | 5 GHz           | 54 Mbps       | 1999 | OFDM, shorter range               |
| 802.11b    | 2.4 GHz         | 11 Mbps       | 1999 | DSSS, longer range, more interference|
| 802.11g    | 2.4 GHz         | 54 Mbps       | 2003 | Backward compatible with 802.11b  |
| 802.11n    | 2.4 / 5 GHz    | 600 Mbps      | 2009 | MIMO, channel bonding (Wi-Fi 4)   |
| 802.11ac   | 5 GHz           | 6.93 Gbps     | 2013 | MU-MIMO, 80/160 MHz channels (Wi-Fi 5)|
| 802.11ax   | 2.4 / 5 / 6 GHz| 9.6 Gbps      | 2021 | OFDMA, BSS Coloring, TWT (Wi-Fi 6/6E)|

### Wireless Security Protocols

| Protocol | Encryption     | Status                                    |
|----------|----------------|-------------------------------------------|
| WEP      | RC4 (64/128)   | Deprecated — easily cracked               |
| WPA      | TKIP (RC4)     | Legacy — improved over WEP                |
| WPA2     | AES-CCMP       | Current standard — recommended minimum    |
| WPA3     | SAE / AES-GCMP | Latest — forward secrecy, stronger auth   |

### Wireless Concepts

- **SSID** — Service Set Identifier: the network name broadcast by the AP.
- **BSS** — Basic Service Set: a single AP and its associated clients.
- **ESS** — Extended Service Set: multiple APs sharing the same SSID for roaming.
- **Channel Overlap (2.4 GHz)** — Only channels 1, 6, and 11 are non-overlapping.
- **Site Survey** — Determines optimal AP placement, channel assignment, and power levels.

---

## Firewalls

### Stateful vs Stateless

| Feature              | Stateless Firewall             | Stateful Firewall                 |
|----------------------|--------------------------------|-----------------------------------|
| **Inspection**       | Individual packets only        | Tracks full connection state      |
| **Context**          | No awareness of session        | Knows if packet belongs to session|
| **ACL Based**        | Yes — src/dst IP, port, proto  | Yes + connection tracking         |
| **Performance**      | Faster (less overhead)         | Slightly slower (state table)     |
| **Security**         | Basic filtering                | Better — blocks out-of-state pkts |
| **Example**          | Simple packet filter / ACL     | Cisco ASA, iptables (conntrack)   |

### Next-Generation Firewall (NGFW)

- Deep Packet Inspection (DPI) — examines application-layer data.
- Application awareness — identifies and controls apps regardless of port.
- Intrusion Prevention System (IPS) — detects and blocks threats inline.
- SSL/TLS inspection — decrypts and inspects encrypted traffic.
- User identity integration — policies based on user/group, not just IP.
- URL filtering and threat intelligence feeds.

---

## Load Balancers

| Feature           | Description                                              |
|-------------------|----------------------------------------------------------|
| **Purpose**       | Distribute traffic across multiple servers for HA/scale  |
| **Layer 4**       | Balances based on IP/port (TCP/UDP)                      |
| **Layer 7**       | Balances based on application data (HTTP headers, URLs)  |
| **Algorithms**    | Round Robin, Least Connections, Weighted, IP Hash         |
| **Health Checks** | Monitors backend server availability                      |
| **Examples**      | F5 BIG-IP, HAProxy, AWS ALB/NLB, NGINX                   |

---

## Proxy Servers

| Type              | Description                                              |
|-------------------|----------------------------------------------------------|
| **Forward Proxy** | Sits between clients and the internet; filters outbound  |
| **Reverse Proxy** | Sits in front of servers; handles inbound requests       |
| **Transparent**   | Intercepts traffic without client configuration          |
| **Caching Proxy** | Stores frequently accessed content to reduce latency     |
| **Use Cases**     | Content filtering, anonymity, caching, SSL termination   |

---

## Enterprise Network Layout — ASCII Diagram

```
                            ┌─────────────┐
                            │  INTERNET   │
                            └──────┬──────┘
                                   │
                          ┌────────┴────────┐
                          │  Edge Router /  │
                          │  NGFW Firewall  │
                          └────────┬────────┘
                                   │
                          ┌────────┴────────┐
                          │   DMZ Switch    │
                          │  (Web, Mail,    │
                          │   DNS servers)  │
                          └────────┬────────┘
                                   │
                  ┌────────────────┼────────────────┐
                  │                │                 │
          ┌───────┴──────┐ ┌──────┴───────┐ ┌──────┴───────┐
          │ Core Switch  │ │ Core Switch  │ │   WLC        │
          │ (Layer 3)    │ │ (Layer 3)    │ │ (Wireless    │
          │              │ │              │ │  Controller) │
          └───────┬──────┘ └──────┬───────┘ └──────┬───────┘
                  │               │                 │
          ┌───────┴──────┐ ┌─────┴────────┐ ┌──────┴───────┐
          │ Distribution │ │ Distribution │ │  Access      │
          │ Switch       │ │ Switch       │ │  Points      │
          └───────┬──────┘ └──────┬───────┘ │  (802.11ax)  │
                  │               │          └──────────────┘
        ┌─────┬──┴──┬─────┐    ┌─┴───┐
        │     │     │     │    │     │
      [PC]  [PC]  [PC] [Printer] [Server] [Server]

  Legend:
    NGFW    = Next-Generation Firewall
    DMZ     = Demilitarized Zone (public-facing services)
    WLC     = Wireless LAN Controller
    Core    = High-speed backbone (Layer 3 routing)
    Dist    = Distribution layer (policy, VLAN routing)
    Access  = End-user connectivity (Layer 2 switching)
```

### Three-Tier Architecture (Cisco Model)

| Tier             | Function                                    | Typical Device        |
|------------------|---------------------------------------------|-----------------------|
| **Core**         | High-speed backbone, fast forwarding         | L3 switches, routers  |
| **Distribution** | Policy enforcement, VLAN routing, aggregation| L3 switches           |
| **Access**       | End-user port connectivity                   | L2 switches, APs      |

---

## CompTIA Network+ (N10-009) — Device Objectives Reference

| Objective | Topic                                             |
|-----------|---------------------------------------------------|
| 2.1       | Networking devices — routers, switches, APs, etc. |
| 2.2       | Routing technologies and concepts                 |
| 2.3       | Ethernet switching features (VLANs, STP, PoE)     |
| 2.4       | Wireless standards and configuration               |
| 4.1       | Security devices — firewalls, IDS/IPS, proxies     |
| 4.3       | Network hardening and access control               |

---

*FLLC Enterprise IT — Portland Community College — Spring 2026*
