"""
============================================================
FLLC Enterprise IT -- Phase 11: Computer Networking
CIS 270 -- Computer Networking | Preston Furulie
Spring 2026 | Portland Community College
CompTIA Network+ (N10-009) Aligned
============================================================
Module: OSI 7-Layer Model & TCP/IP 4-Layer Model
Topics: Layer descriptions, protocol mapping, PDU names,
        encapsulation/decapsulation simulation
============================================================
"""


# ---------------------------------------------------------------------------
# OSI 7-Layer Model -- Full Reference
# ---------------------------------------------------------------------------

OSI_LAYERS = {
    7: {
        "name": "Application",
        "pdu": "Data",
        "description": (
            "Provides network services directly to end-user applications. "
            "This layer identifies communication partners, determines resource "
            "availability, and synchronizes communication. It is the closest "
            "layer to the end user and interacts with software applications."
        ),
        "protocols": ["HTTP", "HTTPS", "FTP", "FTPS", "SFTP", "SMTP",
                       "POP3", "IMAP", "DNS", "DHCP", "SNMP", "Telnet",
                       "SSH", "TFTP", "NTP", "LDAP", "RDP"],
        "devices": ["Hosts", "Firewalls (Layer 7)", "Load Balancers"],
        "network_plus": "N10-009 Objective 1.1, 1.5",
    },
    6: {
        "name": "Presentation",
        "pdu": "Data",
        "description": (
            "Translates data between the application layer and the network "
            "format. Handles encryption/decryption (TLS/SSL), data compression, "
            "and character encoding translation (ASCII, EBCDIC, Unicode). "
            "Ensures data from one system can be read by another."
        ),
        "protocols": ["TLS/SSL", "JPEG", "GIF", "PNG", "MPEG", "ASCII",
                       "EBCDIC", "Unicode"],
        "devices": ["Encryption appliances"],
        "network_plus": "N10-009 Objective 1.1",
    },
    5: {
        "name": "Session",
        "pdu": "Data",
        "description": (
            "Establishes, manages, and terminates sessions between two "
            "communicating hosts. Controls dialogues (simplex, half-duplex, "
            "full-duplex) and provides synchronization with checkpoints so "
            "sessions can resume after interruption."
        ),
        "protocols": ["NetBIOS", "PPTP", "RPC", "SCP", "NFS", "SQL",
                       "SMB"],
        "devices": ["Session-aware gateways"],
        "network_plus": "N10-009 Objective 1.1",
    },
    4: {
        "name": "Transport",
        "pdu": "Segment (TCP) / Datagram (UDP)",
        "description": (
            "Provides reliable or unreliable end-to-end data delivery. "
            "TCP offers connection-oriented, ordered, error-checked delivery "
            "with flow control (windowing) and three-way handshake. UDP offers "
            "connectionless, fast delivery without guaranteed ordering. "
            "Port numbers identify source and destination applications."
        ),
        "protocols": ["TCP", "UDP"],
        "devices": ["Firewalls (Layer 4)", "Load Balancers"],
        "network_plus": "N10-009 Objective 1.1, 1.5",
    },
    3: {
        "name": "Network",
        "pdu": "Packet",
        "description": (
            "Handles logical addressing (IP addresses) and routing of data "
            "between networks. Determines the best path for data to travel "
            "from source to destination across multiple networks. Supports "
            "both IPv4 and IPv6 addressing schemes."
        ),
        "protocols": ["IPv4", "IPv6", "ICMP", "ICMPv6", "IGMP", "IPsec",
                       "OSPF", "EIGRP", "BGP", "RIP"],
        "devices": ["Routers", "Layer 3 Switches", "Firewalls"],
        "network_plus": "N10-009 Objective 1.1, 1.4, 2.2",
    },
    2: {
        "name": "Data Link",
        "pdu": "Frame",
        "description": (
            "Provides node-to-node data transfer and handles error detection "
            "via Frame Check Sequence (FCS/CRC). Divided into two sublayers: "
            "LLC (Logical Link Control -- flow control, error notification) and "
            "MAC (Media Access Control -- physical addressing via MAC addresses, "
            "media access methods like CSMA/CD and CSMA/CA)."
        ),
        "protocols": ["Ethernet (802.3)", "Wi-Fi (802.11)", "PPP", "HDLC",
                       "Frame Relay", "ARP", "STP", "LLDP", "CDP"],
        "devices": ["Switches (Layer 2)", "Bridges", "NICs",
                     "Wireless Access Points"],
        "network_plus": "N10-009 Objective 1.1, 2.1, 2.3",
    },
    1: {
        "name": "Physical",
        "pdu": "Bits",
        "description": (
            "Transmits raw bitstreams over the physical medium. Defines "
            "electrical, optical, and radio signal specifications, cable types "
            "(Cat5e, Cat6, fiber), connectors (RJ-45, LC, SC), signaling "
            "methods, and physical topologies (star, mesh, bus, ring). "
            "Concerned with voltage levels, timing, and data rates."
        ),
        "protocols": ["Ethernet physical (100BASE-TX, 1000BASE-T)",
                       "DSL", "ISDN", "SONET", "802.11 radio"],
        "devices": ["Hubs", "Repeaters", "Media Converters", "Modems",
                     "Cables", "Patch Panels"],
        "network_plus": "N10-009 Objective 1.1, 1.3",
    },
}


# ---------------------------------------------------------------------------
# TCP/IP 4-Layer Model -- Mapped to OSI
# ---------------------------------------------------------------------------

TCPIP_MODEL = {
    4: {
        "name": "Application",
        "osi_equivalent": "Layers 5, 6, 7 (Session, Presentation, Application)",
        "description": (
            "Combines the functionality of OSI Layers 5-7. Contains all "
            "higher-level protocols that interact with user applications, "
            "handle data formatting, and manage sessions."
        ),
        "protocols": ["HTTP", "HTTPS", "FTP", "DNS", "DHCP", "SSH",
                       "SMTP", "POP3", "IMAP", "SNMP", "Telnet",
                       "TFTP", "NTP", "RDP", "TLS/SSL"],
    },
    3: {
        "name": "Transport",
        "osi_equivalent": "Layer 4 (Transport)",
        "description": (
            "Provides end-to-end communication services. TCP ensures "
            "reliable, ordered delivery; UDP provides lightweight, "
            "connectionless communication."
        ),
        "protocols": ["TCP", "UDP"],
    },
    2: {
        "name": "Internet",
        "osi_equivalent": "Layer 3 (Network)",
        "description": (
            "Handles logical addressing and routing across internetworks. "
            "IP (v4 and v6) is the primary protocol. ICMP provides error "
            "messaging and diagnostics (ping, traceroute)."
        ),
        "protocols": ["IPv4", "IPv6", "ICMP", "ICMPv6", "ARP", "IGMP",
                       "IPsec"],
    },
    1: {
        "name": "Network Access (Link)",
        "osi_equivalent": "Layers 1, 2 (Physical, Data Link)",
        "description": (
            "Combines physical and data link functions. Handles hardware "
            "addressing (MAC), media access control, physical signal "
            "transmission, and frame formatting for the local network."
        ),
        "protocols": ["Ethernet (802.3)", "Wi-Fi (802.11)", "PPP", "ARP",
                       "Frame Relay"],
    },
}


# ---------------------------------------------------------------------------
# PDU Names per OSI Layer
# ---------------------------------------------------------------------------

PDU_REFERENCE = {
    7: "Data",
    6: "Data",
    5: "Data",
    4: "Segment (TCP) / Datagram (UDP)",
    3: "Packet",
    2: "Frame",
    1: "Bits",
}


# ---------------------------------------------------------------------------
# Encapsulation / Decapsulation Simulation
# ---------------------------------------------------------------------------

def simulate_encapsulation(message: str) -> None:
    """Walk through packet encapsulation from Layer 7 down to Layer 1."""
    print("\n" + "=" * 62)
    print("  ENCAPSULATION SIMULATION -- Sender Side")
    print("=" * 62)

    steps = [
        (7, "Application",  f"[DATA: '{message}']"),
        (6, "Presentation", f"[ENCODED/ENCRYPTED + DATA: '{message}']"),
        (5, "Session",      f"[SESSION_ID + DATA: '{message}']"),
        (4, "Transport",    f"[TCP_HDR(SrcPort:49152,DstPort:80) + DATA]"),
        (3, "Network",      f"[IP_HDR(Src:192.168.1.10,Dst:93.184.216.34) + SEGMENT]"),
        (2, "Data Link",    f"[ETH_HDR(SrcMAC:AA:BB:CC:DD:EE:01,DstMAC:AA:BB:CC:DD:EE:02) + PACKET + FCS]"),
        (1, "Physical",     "[BITSTREAM: 01101001 01001000 01010100 ...]"),
    ]

    for layer_num, layer_name, representation in steps:
        pdu = PDU_REFERENCE[layer_num]
        print(f"\n  Layer {layer_num} -- {layer_name}  (PDU: {pdu})")
        print(f"    {representation}")

    print("\n" + "-" * 62)
    print("  Data is now on the wire/medium as raw bits.")
    print("=" * 62)


def simulate_decapsulation() -> None:
    """Walk through packet decapsulation from Layer 1 up to Layer 7."""
    print("\n" + "=" * 62)
    print("  DECAPSULATION SIMULATION -- Receiver Side")
    print("=" * 62)

    steps = [
        (1, "Physical",     "Receive bitstream from physical medium"),
        (2, "Data Link",    "Strip Ethernet header/trailer -> extract Packet; verify FCS"),
        (3, "Network",      "Strip IP header -> extract Segment; check destination IP"),
        (4, "Transport",    "Strip TCP header -> extract Data; reassemble segments"),
        (5, "Session",      "Manage session context; pass Data up"),
        (6, "Presentation", "Decrypt / decode Data into application format"),
        (7, "Application",  "Deliver data to the destination application (browser, etc.)"),
    ]

    for layer_num, layer_name, action in steps:
        pdu = PDU_REFERENCE[layer_num]
        print(f"\n  Layer {layer_num} -- {layer_name}  (PDU: {pdu})")
        print(f"    Action: {action}")

    print("\n" + "-" * 62)
    print("  Original application data has been fully reconstructed.")
    print("=" * 62)


# ---------------------------------------------------------------------------
# Display Helpers
# ---------------------------------------------------------------------------

def display_osi_model() -> None:
    """Print the complete OSI 7-layer model reference."""
    print("\n" + "=" * 62)
    print("  OSI 7-LAYER MODEL -- Complete Reference")
    print("  CompTIA Network+ (N10-009)")
    print("=" * 62)

    for layer_num in range(7, 0, -1):
        layer = OSI_LAYERS[layer_num]
        print(f"\n{'-' * 62}")
        print(f"  Layer {layer_num}: {layer['name']}  |  PDU: {layer['pdu']}")
        print(f"{'-' * 62}")
        print(f"  {layer['description']}")
        print(f"  Protocols : {', '.join(layer['protocols'])}")
        print(f"  Devices   : {', '.join(layer['devices'])}")
        print(f"  Exam Ref  : {layer['network_plus']}")

    print()


def display_tcpip_model() -> None:
    """Print the TCP/IP 4-layer model with OSI mapping."""
    print("\n" + "=" * 62)
    print("  TCP/IP 4-LAYER MODEL -- Mapped to OSI")
    print("=" * 62)

    for layer_num in range(4, 0, -1):
        layer = TCPIP_MODEL[layer_num]
        print(f"\n{'-' * 62}")
        print(f"  Layer {layer_num}: {layer['name']}")
        print(f"  OSI Equiv : {layer['osi_equivalent']}")
        print(f"{'-' * 62}")
        print(f"  {layer['description']}")
        print(f"  Protocols : {', '.join(layer['protocols'])}")

    print()


def display_pdu_summary() -> None:
    """Print a quick PDU-per-layer reference table."""
    print("\n" + "=" * 62)
    print("  PDU NAMES PER OSI LAYER")
    print("=" * 62)
    print(f"  {'Layer':<10} {'Name':<16} {'PDU'}")
    print(f"  {'-' * 50}")
    for layer_num in range(7, 0, -1):
        name = OSI_LAYERS[layer_num]["name"]
        pdu = PDU_REFERENCE[layer_num]
        print(f"  {layer_num:<10} {name:<16} {pdu}")
    print()


def display_layer_comparison() -> None:
    """Side-by-side OSI vs TCP/IP comparison."""
    print("\n" + "=" * 62)
    print("  OSI vs TCP/IP -- Side-by-Side Comparison")
    print("=" * 62)
    print(f"  {'OSI Layer':<28} {'TCP/IP Layer'}")
    print(f"  {'-' * 50}")

    mapping = [
        ("7 -- Application",    "4 -- Application"),
        ("6 -- Presentation",   "      ^"),
        ("5 -- Session",        "      ^"),
        ("4 -- Transport",      "3 -- Transport"),
        ("3 -- Network",        "2 -- Internet"),
        ("2 -- Data Link",      "1 -- Network Access"),
        ("1 -- Physical",       "      ^"),
    ]

    for osi, tcpip in mapping:
        print(f"  {osi:<28} {tcpip}")
    print()


# ---------------------------------------------------------------------------
# TCP Three-Way Handshake
# ---------------------------------------------------------------------------

def display_tcp_handshake() -> None:
    """Illustrate the TCP three-way handshake."""
    print("\n" + "=" * 62)
    print("  TCP THREE-WAY HANDSHAKE")
    print("=" * 62)
    print("""
    Client                          Server
      |                               |
      |  ---- SYN (seq=100) ---->     |   Step 1: Client initiates
      |                               |
      |  <-- SYN-ACK (seq=300,       |   Step 2: Server acknowledges
      |       ack=101) ------         |           and synchronizes
      |                               |
      |  ---- ACK (ack=301) ---->     |   Step 3: Client confirms
      |                               |
      |  === Connection Established ==|
    """)
    print("  After handshake: data transfer begins.")
    print("  Connection teardown uses a 4-step FIN/ACK process.")
    print()


# ---------------------------------------------------------------------------
# Main -- Standalone Execution
# ---------------------------------------------------------------------------

def main() -> None:
    print("=" * 62)
    print("  FLLC Enterprise IT -- Phase 11: Computer Networking")
    print("  CIS 270 | OSI & TCP/IP Models | Preston Furulie")
    print("  Spring 2026 | CompTIA Network+ (N10-009)")
    print("=" * 62)

    display_osi_model()
    display_tcpip_model()
    display_pdu_summary()
    display_layer_comparison()
    display_tcp_handshake()
    simulate_encapsulation("GET /index.html HTTP/1.1")
    simulate_decapsulation()

    print("\n" + "=" * 62)
    print("  End of Module -- OSI & TCP/IP Models")
    print("=" * 62)


if __name__ == "__main__":
    main()
