# ============================================================
# Assignment — Networking Fundamentals
# CIS 156 — Computer Science Concepts | FLLC Enterprise
# Author: Preston Furulie
# ============================================================
# CompTIA ITF+ Alignment: Infrastructure domain — understanding
# how devices communicate over networks using layered protocols,
# addressing schemes, and standard services.
# ============================================================

"""
Networking Fundamentals
=======================
Networks enable computers to share data and resources. This module
covers the layered model of networking, addressing, transport
protocols, and common services that FLLC Enterprise depends on
every day.
"""

import socket
import struct
import threading
import time


# ────────────────────────────────────────────────────────────
# 1. OSI 7-LAYER MODEL
# ────────────────────────────────────────────────────────────
# The Open Systems Interconnection model provides a universal
# framework for understanding how data moves from application
# to physical medium and back.

OSI_LAYERS = [
    {
        "number": 7,
        "name": "Application",
        "description": "End-user services and interfaces",
        "protocols": ["HTTP", "HTTPS", "FTP", "SMTP", "DNS", "SSH"],
        "pdu": "Data",
    },
    {
        "number": 6,
        "name": "Presentation",
        "description": "Data formatting, encryption, compression",
        "protocols": ["SSL/TLS", "JPEG", "ASCII", "MPEG"],
        "pdu": "Data",
    },
    {
        "number": 5,
        "name": "Session",
        "description": "Establish, manage, and terminate sessions",
        "protocols": ["NetBIOS", "RPC", "PPTP"],
        "pdu": "Data",
    },
    {
        "number": 4,
        "name": "Transport",
        "description": "Reliable/unreliable delivery, flow control",
        "protocols": ["TCP", "UDP"],
        "pdu": "Segment",
    },
    {
        "number": 3,
        "name": "Network",
        "description": "Logical addressing, routing between networks",
        "protocols": ["IP", "ICMP", "ARP", "OSPF"],
        "pdu": "Packet",
    },
    {
        "number": 2,
        "name": "Data Link",
        "description": "MAC addressing, error detection, frame delivery",
        "protocols": ["Ethernet", "Wi-Fi (802.11)", "PPP"],
        "pdu": "Frame",
    },
    {
        "number": 1,
        "name": "Physical",
        "description": "Electrical signals, cables, connectors",
        "protocols": ["USB", "Bluetooth", "DSL", "Fiber"],
        "pdu": "Bits",
    },
]


def osi_model_demo():
    """Display the complete OSI model with details."""
    print(f"\n{'='*60}")
    print("1. OSI 7-LAYER MODEL")
    print(f"{'='*60}")

    for layer in OSI_LAYERS:
        print(f"\n  Layer {layer['number']}: {layer['name']}")
        print(f"    Description : {layer['description']}")
        print(f"    PDU         : {layer['pdu']}")
        print(f"    Protocols   : {', '.join(layer['protocols'])}")

    print("\n  Mnemonic (top-down): All People Seem To Need Data Processing")
    print("  Mnemonic (bottom-up): Please Do Not Throw Sausage Pizza Away")


# ────────────────────────────────────────────────────────────
# 2. TCP vs UDP COMPARISON
# ────────────────────────────────────────────────────────────

def tcp_vs_udp():
    """Compare the two primary transport-layer protocols."""
    print(f"\n{'='*60}")
    print("2. TCP vs UDP COMPARISON")
    print(f"{'='*60}")

    comparisons = [
        ("Full name",        "Transmission Control Protocol", "User Datagram Protocol"),
        ("Connection",       "Connection-oriented",           "Connectionless"),
        ("Reliability",      "Guaranteed delivery",           "Best-effort delivery"),
        ("Ordering",         "In-order delivery",             "No ordering guarantee"),
        ("Speed",            "Slower (overhead)",             "Faster (minimal overhead)"),
        ("Header size",      "20-60 bytes",                   "8 bytes"),
        ("Flow control",     "Yes (windowing)",               "No"),
        ("Use cases",        "Web, email, file transfer",     "Streaming, DNS, gaming"),
        ("Error checking",   "Checksum + retransmission",     "Checksum only"),
    ]

    print(f"\n  {'Feature':<20} {'TCP':<32} {'UDP'}")
    print(f"  {'-'*20} {'-'*32} {'-'*30}")
    for feature, tcp, udp in comparisons:
        print(f"  {feature:<20} {tcp:<32} {udp}")


# ────────────────────────────────────────────────────────────
# 3. IP ADDRESSING — IPv4, SUBNETS, CIDR
# ────────────────────────────────────────────────────────────

def ip_to_binary(ip_str):
    """Convert dotted-decimal IPv4 address to binary string."""
    octets = ip_str.split(".")
    return ".".join(f"{int(o):08b}" for o in octets)


def cidr_info(cidr):
    """Parse a CIDR notation address and compute network details."""
    ip_str, prefix_len = cidr.split("/")
    prefix_len = int(prefix_len)
    ip_int = struct.unpack("!I", socket.inet_aton(ip_str))[0]

    mask_int = (0xFFFFFFFF << (32 - prefix_len)) & 0xFFFFFFFF
    network_int = ip_int & mask_int
    broadcast_int = network_int | (~mask_int & 0xFFFFFFFF)
    num_hosts = (1 << (32 - prefix_len)) - 2

    to_ip = lambda n: socket.inet_ntoa(struct.pack("!I", n))
    return {
        "address": ip_str,
        "prefix": prefix_len,
        "subnet_mask": to_ip(mask_int),
        "network": to_ip(network_int),
        "broadcast": to_ip(broadcast_int),
        "usable_hosts": max(num_hosts, 0),
        "binary": ip_to_binary(ip_str),
    }


def ip_addressing_demo():
    """Demonstrate IPv4 addressing and subnetting."""
    print(f"\n{'='*60}")
    print("3. IP ADDRESSING — IPv4, Subnets, CIDR")
    print(f"{'='*60}")

    print("\n  IPv4 Address Classes:")
    classes = [
        ("A", "1.0.0.0",   "126.255.255.255", "/8",  "Large networks"),
        ("B", "128.0.0.0",  "191.255.255.255", "/16", "Medium networks"),
        ("C", "192.0.0.0",  "223.255.255.255", "/24", "Small networks"),
        ("D", "224.0.0.0",  "239.255.255.255", "N/A", "Multicast"),
        ("E", "240.0.0.0",  "255.255.255.255", "N/A", "Experimental"),
    ]
    print(f"  {'Class':<8} {'Start':<18} {'End':<18} {'CIDR':<6} {'Use'}")
    print(f"  {'-'*8} {'-'*18} {'-'*18} {'-'*6} {'-'*16}")
    for cls, start, end, cidr, use in classes:
        print(f"  {cls:<8} {start:<18} {end:<18} {cidr:<6} {use}")

    examples = ["192.168.1.0/24", "10.0.0.0/8", "172.16.0.0/16"]
    for cidr in examples:
        info = cidr_info(cidr)
        print(f"\n  CIDR: {cidr}")
        print(f"    Binary       : {info['binary']}")
        print(f"    Subnet mask  : {info['subnet_mask']}")
        print(f"    Network addr : {info['network']}")
        print(f"    Broadcast    : {info['broadcast']}")
        print(f"    Usable hosts : {info['usable_hosts']:,}")


# ────────────────────────────────────────────────────────────
# 4. SOCKET PROGRAMMING BASICS
# ────────────────────────────────────────────────────────────
# Sockets are endpoints for communication. A server listens
# on a port; a client connects to it.

def socket_demo():
    """Demonstrate a simple TCP client-server exchange."""
    print(f"\n{'='*60}")
    print("4. SOCKET PROGRAMMING — Client / Server Demo")
    print(f"{'='*60}")

    host = "127.0.0.1"
    port = 0  # OS assigns an available port

    server_ready = threading.Event()
    actual_port = {"value": 0}

    def server():
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind((host, port))
            actual_port["value"] = s.getsockname()[1]
            s.listen(1)
            server_ready.set()
            conn, addr = s.accept()
            with conn:
                data = conn.recv(1024)
                response = f"Echo: {data.decode()}"
                conn.sendall(response.encode())

    def client():
        server_ready.wait()
        time.sleep(0.05)
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((host, actual_port["value"]))
            message = "Hello from FLLC client!"
            s.sendall(message.encode())
            response = s.recv(1024).decode()
            print(f"\n  Client sent    : {message}")
            print(f"  Server replied : {response}")

    t_server = threading.Thread(target=server)
    t_client = threading.Thread(target=client)
    t_server.start()
    t_client.start()
    t_server.join(timeout=5)
    t_client.join(timeout=5)

    print(f"  Port used      : {actual_port['value']}")
    print("  Protocol       : TCP (connection-oriented)")


# ────────────────────────────────────────────────────────────
# 5. DNS RESOLUTION SIMULATION
# ────────────────────────────────────────────────────────────
# DNS translates human-readable domain names into IP addresses.

def dns_simulation():
    """Simulate DNS resolution with a local lookup table."""
    print(f"\n{'='*60}")
    print("5. DNS RESOLUTION SIMULATION")
    print(f"{'='*60}")

    dns_table = {
        "www.fllc-enterprise.com":  "192.168.1.10",
        "mail.fllc-enterprise.com": "192.168.1.20",
        "db.fllc-enterprise.com":   "192.168.1.30",
        "api.fllc-enterprise.com":  "192.168.1.40",
        "www.example.com":          "93.184.216.34",
    }
    cache = {}

    def resolve(domain):
        if domain in cache:
            return cache[domain], "CACHE HIT"
        if domain in dns_table:
            cache[domain] = dns_table[domain]
            return dns_table[domain], "RESOLVED"
        return None, "NXDOMAIN"

    queries = [
        "www.fllc-enterprise.com",
        "mail.fllc-enterprise.com",
        "www.fllc-enterprise.com",  # should hit cache
        "unknown.invalid",
        "api.fllc-enterprise.com",
    ]

    print(f"\n  {'Query':<35} {'IP Address':<18} {'Status'}")
    print(f"  {'-'*35} {'-'*18} {'-'*12}")
    for domain in queries:
        ip, status = resolve(domain)
        ip_display = ip if ip else "—"
        print(f"  {domain:<35} {ip_display:<18} {status}")


# ────────────────────────────────────────────────────────────
# 6. HTTP REQUEST / RESPONSE CYCLE
# ────────────────────────────────────────────────────────────

def http_cycle_demo():
    """Explain the HTTP request/response lifecycle."""
    print(f"\n{'='*60}")
    print("6. HTTP REQUEST / RESPONSE CYCLE")
    print(f"{'='*60}")

    print("""
  1. Client (browser) opens TCP connection to server on port 80/443
  2. Client sends HTTP request:

     GET /index.html HTTP/1.1
     Host: www.fllc-enterprise.com
     User-Agent: Mozilla/5.0
     Accept: text/html

  3. Server processes the request (routes, auth, DB query, etc.)
  4. Server sends HTTP response:

     HTTP/1.1 200 OK
     Content-Type: text/html; charset=UTF-8
     Content-Length: 3421

     <html>...</html>

  5. Client renders the response (HTML, CSS, JS)
  6. Connection closed (or kept alive for reuse)
    """)

    status_codes = [
        (200, "OK",                    "Request succeeded"),
        (301, "Moved Permanently",     "Resource relocated (redirect)"),
        (403, "Forbidden",             "Server refuses the request"),
        (404, "Not Found",             "Resource does not exist"),
        (500, "Internal Server Error", "Server-side failure"),
    ]
    print(f"  Common HTTP Status Codes:")
    print(f"  {'Code':<6} {'Reason':<24} {'Meaning'}")
    print(f"  {'-'*6} {'-'*24} {'-'*32}")
    for code, reason, meaning in status_codes:
        print(f"  {code:<6} {reason:<24} {meaning}")


# ────────────────────────────────────────────────────────────
# 7. NETWORK TROUBLESHOOTING CONCEPTS
# ────────────────────────────────────────────────────────────

def troubleshooting_demo():
    """Describe common network diagnostic tools and techniques."""
    print(f"\n{'='*60}")
    print("7. NETWORK TROUBLESHOOTING TOOLS")
    print(f"{'='*60}")

    tools = [
        ("ping",       "Tests reachability via ICMP echo",
         "ping 192.168.1.1"),
        ("traceroute", "Shows the path packets take to a destination",
         "tracert www.fllc-enterprise.com"),
        ("nslookup",   "Queries DNS for domain-to-IP mapping",
         "nslookup www.fllc-enterprise.com"),
        ("ipconfig",   "Displays local network adapter configuration",
         "ipconfig /all"),
        ("netstat",    "Shows active connections and listening ports",
         "netstat -an"),
        ("nmap",       "Network scanner for open ports and services",
         "nmap -sV 192.168.1.0/24"),
    ]

    for tool, desc, example in tools:
        print(f"\n  {tool}")
        print(f"    Purpose : {desc}")
        print(f"    Example : {example}")

    print("\n  Troubleshooting methodology (top-down):")
    steps = [
        "Identify the problem (symptoms, scope, recent changes)",
        "Check physical layer (cables, lights, power)",
        "Verify IP configuration (ipconfig / ifconfig)",
        "Test local connectivity (ping gateway)",
        "Test remote connectivity (ping external host)",
        "Check DNS resolution (nslookup)",
        "Check application-layer service (curl, browser)",
        "Document findings and resolution",
    ]
    for i, step in enumerate(steps, 1):
        print(f"    {i}. {step}")


# ────────────────────────────────────────────────────────────
# MAIN — Run all demonstrations
# ────────────────────────────────────────────────────────────

def main():
    print("=" * 60)
    print("  CIS 156 — Networking Fundamentals")
    print("  FLLC Enterprise | Preston Furulie | Spring 2026")
    print("=" * 60)

    osi_model_demo()
    tcp_vs_udp()
    ip_addressing_demo()
    socket_demo()
    dns_simulation()
    http_cycle_demo()
    troubleshooting_demo()

    print(f"\n{'='*60}")
    print("  End of Networking Fundamentals Module")
    print(f"{'='*60}")


if __name__ == "__main__":
    main()
