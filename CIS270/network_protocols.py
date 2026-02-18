"""
============================================================
FLLC Enterprise IT -- Phase 11: Computer Networking
CIS 270 -- Computer Networking | Preston Furulie
Spring 2026 | Portland Community College
CompTIA Network+ (N10-009) Aligned
============================================================
Module: Network Protocols
Topics: DHCP (DORA), DNS resolution, ARP simulation,
        HTTP/HTTPS, FTP, SSH, SMTP, POP3, IMAP,
        well-known port numbers reference
============================================================
"""


# ---------------------------------------------------------------------------
# Well-Known Port Numbers Reference
# ---------------------------------------------------------------------------

PORT_REFERENCE = {
    20:   {"protocol": "FTP Data",      "transport": "TCP",     "description": "File Transfer Protocol -- data channel"},
    21:   {"protocol": "FTP Control",   "transport": "TCP",     "description": "File Transfer Protocol -- command/control channel"},
    22:   {"protocol": "SSH/SCP/SFTP",  "transport": "TCP",     "description": "Secure Shell -- encrypted remote access and file transfer"},
    23:   {"protocol": "Telnet",        "transport": "TCP",     "description": "Unencrypted remote terminal access (insecure)"},
    25:   {"protocol": "SMTP",          "transport": "TCP",     "description": "Simple Mail Transfer Protocol -- sending email"},
    53:   {"protocol": "DNS",           "transport": "TCP/UDP", "description": "Domain Name System -- name resolution"},
    67:   {"protocol": "DHCP Server",   "transport": "UDP",     "description": "Dynamic Host Configuration Protocol -- server listens"},
    68:   {"protocol": "DHCP Client",   "transport": "UDP",     "description": "Dynamic Host Configuration Protocol -- client listens"},
    69:   {"protocol": "TFTP",          "transport": "UDP",     "description": "Trivial File Transfer Protocol -- simple file transfer"},
    80:   {"protocol": "HTTP",          "transport": "TCP",     "description": "Hypertext Transfer Protocol -- unencrypted web traffic"},
    110:  {"protocol": "POP3",          "transport": "TCP",     "description": "Post Office Protocol v3 -- retrieving email"},
    123:  {"protocol": "NTP",           "transport": "UDP",     "description": "Network Time Protocol -- clock synchronization"},
    143:  {"protocol": "IMAP",          "transport": "TCP",     "description": "Internet Message Access Protocol -- email management"},
    161:  {"protocol": "SNMP",          "transport": "UDP",     "description": "Simple Network Management Protocol -- monitoring"},
    162:  {"protocol": "SNMP Trap",     "transport": "UDP",     "description": "SNMP Trap -- unsolicited alerts from agents"},
    389:  {"protocol": "LDAP",          "transport": "TCP",     "description": "Lightweight Directory Access Protocol"},
    443:  {"protocol": "HTTPS",         "transport": "TCP",     "description": "HTTP over TLS/SSL -- encrypted web traffic"},
    445:  {"protocol": "SMB/CIFS",      "transport": "TCP",     "description": "Server Message Block -- Windows file/printer sharing"},
    465:  {"protocol": "SMTPS",         "transport": "TCP",     "description": "SMTP over SSL -- secure email sending"},
    514:  {"protocol": "Syslog",        "transport": "UDP",     "description": "System logging protocol"},
    587:  {"protocol": "SMTP (sub)",    "transport": "TCP",     "description": "SMTP submission -- authenticated email sending"},
    636:  {"protocol": "LDAPS",         "transport": "TCP",     "description": "LDAP over SSL/TLS"},
    993:  {"protocol": "IMAPS",         "transport": "TCP",     "description": "IMAP over SSL/TLS -- secure email retrieval"},
    995:  {"protocol": "POP3S",         "transport": "TCP",     "description": "POP3 over SSL/TLS -- secure email retrieval"},
    1433: {"protocol": "MS SQL",        "transport": "TCP",     "description": "Microsoft SQL Server database"},
    3306: {"protocol": "MySQL",         "transport": "TCP",     "description": "MySQL database server"},
    3389: {"protocol": "RDP",           "transport": "TCP/UDP", "description": "Remote Desktop Protocol -- Windows remote access"},
    5060: {"protocol": "SIP",           "transport": "TCP/UDP", "description": "Session Initiation Protocol -- VoIP signaling"},
}

PORT_RANGES = {
    "Well-Known":  "0 -- 1,023      (assigned by IANA to common services)",
    "Registered":  "1,024 -- 49,151 (registered for specific applications)",
    "Dynamic":     "49,152 -- 65,535 (ephemeral ports for client connections)",
}


# ---------------------------------------------------------------------------
# DHCP -- DORA Process
# ---------------------------------------------------------------------------

DHCP_DORA = {
    "overview": (
        "DHCP dynamically assigns IP addresses and network configuration "
        "to clients. Uses UDP ports 67 (server) and 68 (client)."
    ),
    "steps": [
        {
            "step": "1. Discover",
            "source": "Client (0.0.0.0)",
            "destination": "Broadcast (255.255.255.255)",
            "description": (
                "Client broadcasts a DHCPDISCOVER message to find available "
                "DHCP servers on the network."
            ),
        },
        {
            "step": "2. Offer",
            "source": "DHCP Server",
            "destination": "Broadcast (or unicast to client MAC)",
            "description": (
                "Server responds with a DHCPOFFER containing a proposed IP "
                "address, subnet mask, default gateway, DNS servers, and lease time."
            ),
        },
        {
            "step": "3. Request",
            "source": "Client",
            "destination": "Broadcast (255.255.255.255)",
            "description": (
                "Client broadcasts a DHCPREQUEST accepting the offered IP. "
                "Broadcast ensures all DHCP servers know which offer was accepted."
            ),
        },
        {
            "step": "4. Acknowledge",
            "source": "DHCP Server",
            "destination": "Client",
            "description": (
                "Server sends DHCPACK confirming the lease. Client can now use "
                "the assigned IP address for the duration of the lease."
            ),
        },
    ],
    "additional_info": [
        "Lease renewal: client requests renewal at 50% (T1) and 87.5% (T2) of lease.",
        "DHCP Relay Agent: forwards DHCP broadcasts across subnets (ip helper-address).",
        "DHCP Reservation: binds a specific IP to a client's MAC address.",
        "DHCP Scope: the range of IP addresses a server can assign.",
    ],
}


# ---------------------------------------------------------------------------
# DNS -- Domain Name System
# ---------------------------------------------------------------------------

DNS_INFO = {
    "overview": (
        "DNS translates human-readable domain names (e.g., www.example.com) "
        "into IP addresses. Uses UDP port 53 for queries and TCP port 53 "
        "for zone transfers and large responses."
    ),
    "resolution_types": {
        "Recursive": (
            "Client asks its DNS resolver to do all the work. The resolver "
            "queries root, TLD, and authoritative servers on behalf of the "
            "client and returns the final answer."
        ),
        "Iterative": (
            "The DNS server responds with the best answer it has or a referral "
            "to another server. The querying resolver follows the chain itself."
        ),
    },
    "record_types": {
        "A":     "Maps a hostname to an IPv4 address (e.g., example.com -> 93.184.216.34)",
        "AAAA":  "Maps a hostname to an IPv6 address",
        "CNAME": "Canonical Name -- alias for another domain name",
        "MX":    "Mail Exchange -- specifies mail servers for the domain (with priority)",
        "NS":    "Name Server -- authoritative DNS servers for the zone",
        "PTR":   "Pointer -- reverse DNS lookup (IP -> hostname)",
        "SOA":   "Start of Authority -- zone metadata (serial, refresh, retry, expire)",
        "SRV":   "Service locator -- specifies host/port for services",
        "TXT":   "Text record -- arbitrary text (SPF, DKIM, domain verification)",
    },
    "hierarchy": [
        "Root DNS Servers (13 named root server clusters: a.root-servers.net ... m.root-servers.net)",
        "TLD Servers (.com, .org, .net, .edu, country codes: .us, .uk, etc.)",
        "Authoritative Name Servers (hold actual DNS records for a domain)",
        "Recursive Resolver (ISP or public DNS: 8.8.8.8, 1.1.1.1)",
    ],
}


# ---------------------------------------------------------------------------
# ARP -- Address Resolution Protocol
# ---------------------------------------------------------------------------

def simulate_arp_table() -> dict:
    """Simulate a sample ARP table mapping IP addresses to MAC addresses."""
    arp_table = {
        "192.168.1.1":   "AA:BB:CC:DD:EE:01",
        "192.168.1.10":  "AA:BB:CC:DD:EE:0A",
        "192.168.1.20":  "AA:BB:CC:DD:EE:14",
        "192.168.1.50":  "AA:BB:CC:DD:EE:32",
        "192.168.1.100": "AA:BB:CC:DD:EE:64",
    }
    return arp_table


ARP_INFO = {
    "overview": (
        "ARP resolves IPv4 addresses to MAC (hardware) addresses on a local "
        "network segment. Operates at Layer 2/3 boundary."
    ),
    "process": [
        "1. Host A wants to send data to 192.168.1.20 but doesn't know its MAC.",
        "2. Host A checks its local ARP cache -- no entry found.",
        "3. Host A broadcasts an ARP Request: 'Who has 192.168.1.20? Tell 192.168.1.10'",
        "4. All hosts on the segment receive the broadcast.",
        "5. Host with 192.168.1.20 sends an ARP Reply (unicast) with its MAC address.",
        "6. Host A updates its ARP cache and sends the frame to the resolved MAC.",
    ],
    "security": (
        "ARP Spoofing/Poisoning: attacker sends fake ARP replies to redirect "
        "traffic. Mitigated with Dynamic ARP Inspection (DAI) on managed switches."
    ),
}


# ---------------------------------------------------------------------------
# HTTP / HTTPS
# ---------------------------------------------------------------------------

HTTP_INFO = {
    "methods": {
        "GET":     "Retrieve a resource (idempotent, no body)",
        "POST":    "Submit data to create a resource (non-idempotent)",
        "PUT":     "Replace a resource entirely (idempotent)",
        "PATCH":   "Partially update a resource",
        "DELETE":  "Remove a resource (idempotent)",
        "HEAD":    "Like GET but returns headers only (no body)",
        "OPTIONS": "Describe communication options for the target resource",
    },
    "status_codes": {
        "1xx Informational": {"100": "Continue", "101": "Switching Protocols"},
        "2xx Success":       {"200": "OK", "201": "Created", "204": "No Content"},
        "3xx Redirection":   {"301": "Moved Permanently", "302": "Found (Temporary)",
                              "304": "Not Modified"},
        "4xx Client Error":  {"400": "Bad Request", "401": "Unauthorized",
                              "403": "Forbidden", "404": "Not Found",
                              "405": "Method Not Allowed", "408": "Request Timeout"},
        "5xx Server Error":  {"500": "Internal Server Error", "502": "Bad Gateway",
                              "503": "Service Unavailable", "504": "Gateway Timeout"},
    },
    "headers": {
        "Host":           "Target domain name (required in HTTP/1.1)",
        "Content-Type":   "MIME type of the body (e.g., application/json, text/html)",
        "Authorization":  "Credentials for authentication (Bearer token, Basic)",
        "Cache-Control":  "Caching directives (no-cache, max-age=3600)",
        "User-Agent":     "Client software identifier",
        "Accept":         "Acceptable response content types",
        "Set-Cookie":     "Server sets a cookie on the client",
    },
    "https": (
        "HTTPS = HTTP over TLS (Transport Layer Security). Uses port 443. "
        "Provides confidentiality (encryption), integrity (message authentication), "
        "and authentication (server certificates). TLS handshake negotiates "
        "cipher suites and establishes a symmetric session key."
    ),
}


# ---------------------------------------------------------------------------
# Additional Protocol Descriptions
# ---------------------------------------------------------------------------

PROTOCOL_DESCRIPTIONS = {
    "FTP": {
        "ports": "20 (data), 21 (control)",
        "transport": "TCP",
        "description": (
            "File Transfer Protocol -- transfers files between client and server. "
            "Active mode: server initiates data connection. Passive mode: client "
            "initiates both connections (firewall-friendly). Credentials sent in "
            "cleartext -- use SFTP or FTPS for security."
        ),
    },
    "SSH": {
        "ports": "22",
        "transport": "TCP",
        "description": (
            "Secure Shell -- encrypted remote command-line access. Replaces Telnet. "
            "Supports key-based and password authentication. Also tunnels other "
            "protocols (port forwarding). SCP and SFTP run over SSH."
        ),
    },
    "SMTP": {
        "ports": "25 (relay), 587 (submission), 465 (SMTPS)",
        "transport": "TCP",
        "description": (
            "Simple Mail Transfer Protocol -- sends/relays email between mail servers "
            "and from clients to servers. Port 587 with STARTTLS is the modern "
            "standard for authenticated submission."
        ),
    },
    "POP3": {
        "ports": "110 (plain), 995 (POP3S)",
        "transport": "TCP",
        "description": (
            "Post Office Protocol v3 -- downloads email from server to client. "
            "Typically deletes messages from server after download. Simple but "
            "limited -- no server-side folder management."
        ),
    },
    "IMAP": {
        "ports": "143 (plain), 993 (IMAPS)",
        "transport": "TCP",
        "description": (
            "Internet Message Access Protocol -- manages email on the server. "
            "Supports folders, search, flags, and synchronization across multiple "
            "devices. Messages remain on server until explicitly deleted."
        ),
    },
    "SNMP": {
        "ports": "161 (agent), 162 (trap)",
        "transport": "UDP",
        "description": (
            "Simple Network Management Protocol -- monitors and manages network "
            "devices. Uses community strings (v1/v2c) or authentication (v3). "
            "GET retrieves data; SET modifies config; TRAP sends alerts."
        ),
    },
    "NTP": {
        "ports": "123",
        "transport": "UDP",
        "description": (
            "Network Time Protocol -- synchronizes clocks across network devices. "
            "Uses a hierarchy of time sources (stratum levels). Stratum 0 is an "
            "atomic clock; Stratum 1 is directly connected to Stratum 0."
        ),
    },
    "RDP": {
        "ports": "3389",
        "transport": "TCP/UDP",
        "description": (
            "Remote Desktop Protocol -- provides graphical remote access to "
            "Windows systems. Supports encryption, clipboard sharing, drive "
            "redirection, and multi-monitor setups."
        ),
    },
}


# ---------------------------------------------------------------------------
# Display Functions
# ---------------------------------------------------------------------------

def display_port_reference() -> None:
    print("\n" + "=" * 72)
    print("  WELL-KNOWN PORT NUMBERS -- Network+ Reference")
    print("=" * 72)
    print(f"  {'Port':<7} {'Protocol':<16} {'Transport':<10} {'Description'}")
    print(f"  {'-' * 68}")
    for port, info in PORT_REFERENCE.items():
        print(f"  {port:<7} {info['protocol']:<16} {info['transport']:<10} {info['description']}")

    print(f"\n  Port Ranges:")
    for name, desc in PORT_RANGES.items():
        print(f"    {name:<14} {desc}")
    print()


def display_dhcp() -> None:
    print("\n" + "=" * 62)
    print("  DHCP -- DORA PROCESS")
    print("=" * 62)
    print(f"  {DHCP_DORA['overview']}\n")
    for step in DHCP_DORA["steps"]:
        print(f"  {step['step']}")
        print(f"    Source     : {step['source']}")
        print(f"    Destination: {step['destination']}")
        print(f"    {step['description']}")
        print()
    print("  Additional DHCP Concepts:")
    for item in DHCP_DORA["additional_info"]:
        print(f"    * {item}")
    print()


def display_dns() -> None:
    print("\n" + "=" * 62)
    print("  DNS -- DOMAIN NAME SYSTEM")
    print("=" * 62)
    print(f"  {DNS_INFO['overview']}\n")

    print("  Resolution Types:")
    for rtype, desc in DNS_INFO["resolution_types"].items():
        print(f"    {rtype}: {desc}\n")

    print("  DNS Record Types:")
    print(f"  {'-' * 56}")
    for rec, desc in DNS_INFO["record_types"].items():
        print(f"    {rec:<8} {desc}")

    print(f"\n  DNS Hierarchy:")
    for level in DNS_INFO["hierarchy"]:
        print(f"    -> {level}")
    print()


def display_arp() -> None:
    print("\n" + "=" * 62)
    print("  ARP -- ADDRESS RESOLUTION PROTOCOL")
    print("=" * 62)
    print(f"  {ARP_INFO['overview']}\n")

    print("  ARP Process:")
    for step in ARP_INFO["process"]:
        print(f"    {step}")

    print(f"\n  Sample ARP Table:")
    print(f"  {'-' * 44}")
    print(f"  {'IP Address':<20} {'MAC Address'}")
    print(f"  {'-' * 44}")
    arp_table = simulate_arp_table()
    for ip, mac in arp_table.items():
        print(f"  {ip:<20} {mac}")

    print(f"\n  Security: {ARP_INFO['security']}")
    print()


def display_http() -> None:
    print("\n" + "=" * 62)
    print("  HTTP / HTTPS")
    print("=" * 62)
    print(f"  {HTTP_INFO['https']}\n")

    print("  HTTP Methods:")
    for method, desc in HTTP_INFO["methods"].items():
        print(f"    {method:<10} {desc}")

    print(f"\n  HTTP Status Codes:")
    for category, codes in HTTP_INFO["status_codes"].items():
        print(f"\n    {category}:")
        for code, msg in codes.items():
            print(f"      {code} -- {msg}")

    print(f"\n  Common HTTP Headers:")
    for header, desc in HTTP_INFO["headers"].items():
        print(f"    {header:<18} {desc}")
    print()


def display_protocols() -> None:
    print("\n" + "=" * 62)
    print("  ADDITIONAL PROTOCOL DETAILS")
    print("=" * 62)
    for name, info in PROTOCOL_DESCRIPTIONS.items():
        print(f"\n  {name} (Port(s): {info['ports']} | {info['transport']})")
        print(f"  {'-' * 56}")
        print(f"  {info['description']}")
    print()


# ---------------------------------------------------------------------------
# Main -- Standalone Execution
# ---------------------------------------------------------------------------

def main() -> None:
    print("=" * 72)
    print("  FLLC Enterprise IT -- Phase 11: Computer Networking")
    print("  CIS 270 | Network Protocols | Preston Furulie")
    print("  Spring 2026 | CompTIA Network+ (N10-009)")
    print("=" * 72)

    display_port_reference()
    display_dhcp()
    display_dns()
    display_arp()
    display_http()
    display_protocols()

    print("\n" + "=" * 62)
    print("  End of Module -- Network Protocols")
    print("=" * 62)


if __name__ == "__main__":
    main()
