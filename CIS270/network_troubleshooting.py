"""
============================================================
FLLC Enterprise IT -- Phase 11: Computer Networking
CIS 270 -- Computer Networking | Preston Furulie
Spring 2026 | Portland Community College
CompTIA Network+ (N10-009) Aligned
============================================================
Module: Network Troubleshooting
Topics: CompTIA 7-step methodology, common issues,
        CLI tools, connectivity checks, cable types,
        performance metrics
============================================================
"""

import subprocess
import platform
import socket


# ---------------------------------------------------------------------------
# CompTIA Troubleshooting Methodology -- 7 Steps
# ---------------------------------------------------------------------------

TROUBLESHOOTING_STEPS = [
    {
        "step": 1,
        "name": "Identify the Problem",
        "actions": [
            "Gather information from the user/documentation.",
            "Identify symptoms -- what is working and what is not.",
            "Question users: when did it start? What changed?",
            "Determine scope: single user, department, or entire network.",
            "Duplicate the problem if possible.",
            "Check system logs, event viewers, and monitoring tools.",
        ],
    },
    {
        "step": 2,
        "name": "Establish a Theory of Probable Cause",
        "actions": [
            "Consider the most likely cause first (Occam's Razor).",
            "Use the OSI model: start from Layer 1 (Physical) upward.",
            "Check for recent changes (new software, config changes).",
            "Consider external factors (ISP outage, power issues).",
            "Question the obvious -- is it plugged in? Is the link light on?",
        ],
    },
    {
        "step": 3,
        "name": "Test the Theory to Determine Cause",
        "actions": [
            "Test the most likely theory first.",
            "If confirmed, proceed to resolution.",
            "If not confirmed, establish a new theory and test again.",
            "Use diagnostic tools: ping, traceroute, nslookup, etc.",
        ],
    },
    {
        "step": 4,
        "name": "Establish a Plan of Action",
        "actions": [
            "Plan the fix and identify potential side effects.",
            "Consider change management procedures.",
            "Notify affected users/stakeholders.",
            "Schedule maintenance window if needed.",
            "Prepare a rollback plan in case the fix fails.",
        ],
    },
    {
        "step": 5,
        "name": "Implement the Solution or Escalate",
        "actions": [
            "Apply the fix according to the plan.",
            "If beyond your expertise, escalate to senior staff or vendor.",
            "Follow change management and documentation procedures.",
        ],
    },
    {
        "step": 6,
        "name": "Verify Full System Functionality",
        "actions": [
            "Test the specific fix -- does the original problem recur?",
            "Test related systems -- did the fix break anything else?",
            "Have the end user confirm the issue is resolved.",
            "Implement preventive measures if applicable.",
        ],
    },
    {
        "step": 7,
        "name": "Document Findings, Actions, and Outcomes",
        "actions": [
            "Record the problem, cause, and resolution.",
            "Update knowledge base / ticketing system.",
            "Document any configuration changes made.",
            "Share lessons learned with the team.",
        ],
    },
]


# ---------------------------------------------------------------------------
# Common Network Issues & Symptoms
# ---------------------------------------------------------------------------

COMMON_ISSUES = {
    "No Connectivity": {
        "symptoms": ["Cannot ping gateway", "No link light", "APIPA address (169.254.x.x)"],
        "possible_causes": [
            "Cable unplugged or damaged",
            "NIC disabled or failed",
            "Switch port disabled or misconfigured",
            "DHCP server unreachable",
            "Wrong VLAN assignment",
        ],
    },
    "Slow Network Performance": {
        "symptoms": ["High latency", "Packet loss", "Timeouts", "Buffering"],
        "possible_causes": [
            "Network congestion / bandwidth saturation",
            "Duplex mismatch (half vs full)",
            "Failing hardware (cable, NIC, switch port)",
            "Broadcast storms",
            "DNS resolution delays",
            "Malware / unauthorized traffic",
        ],
    },
    "Intermittent Connectivity": {
        "symptoms": ["Drops periodically", "Ping replies with sporadic timeouts"],
        "possible_causes": [
            "Loose cable connection",
            "Wireless interference (2.4 GHz microwave, Bluetooth)",
            "Spanning Tree reconvergence",
            "IP address conflict",
            "Overloaded DHCP scope / short lease times",
        ],
    },
    "Cannot Resolve Hostnames": {
        "symptoms": ["Ping by IP works but not by name", "Browser errors"],
        "possible_causes": [
            "DNS server down or misconfigured",
            "Incorrect DNS settings on client",
            "DNS cache poisoned or stale (flush with ipconfig /flushdns)",
            "Firewall blocking port 53",
        ],
    },
}


# ---------------------------------------------------------------------------
# Command-Line Network Tools
# ---------------------------------------------------------------------------

CLI_TOOLS = {
    "ping": {
        "purpose": "Test reachability and round-trip time to a host using ICMP Echo.",
        "syntax_win": "ping <hostname_or_ip> [-t] [-n count]",
        "syntax_linux": "ping <hostname_or_ip> [-c count]",
        "example": "ping 8.8.8.8 -n 4",
        "notes": "Uses ICMP. Blocked by some firewalls. -t for continuous (Windows).",
    },
    "tracert / traceroute": {
        "purpose": "Trace the path (hops) packets take to reach a destination.",
        "syntax_win": "tracert <hostname_or_ip>",
        "syntax_linux": "traceroute <hostname_or_ip>",
        "example": "tracert www.google.com",
        "notes": "Uses ICMP (Win) or UDP (Linux). Shows each router hop and RTT.",
    },
    "nslookup": {
        "purpose": "Query DNS servers for name resolution records.",
        "syntax_win": "nslookup <domain> [dns_server]",
        "syntax_linux": "nslookup <domain> [dns_server]",
        "example": "nslookup www.example.com 8.8.8.8",
        "notes": "Can query specific record types: nslookup -type=MX example.com",
    },
    "ipconfig / ifconfig / ip": {
        "purpose": "Display or manage IP configuration on the local machine.",
        "syntax_win": "ipconfig [/all] [/release] [/renew] [/flushdns]",
        "syntax_linux": "ip addr show  |  ifconfig",
        "example": "ipconfig /all",
        "notes": "/release + /renew to get a new DHCP lease. /flushdns clears DNS cache.",
    },
    "netstat": {
        "purpose": "Display active connections, listening ports, and routing tables.",
        "syntax_win": "netstat [-a] [-n] [-o] [-b]",
        "syntax_linux": "netstat -tulnp  |  ss -tulnp",
        "example": "netstat -an",
        "notes": "-a all connections, -n numeric, -o PID (Win), -b process name (Win).",
    },
    "arp": {
        "purpose": "Display or modify the ARP cache (IP -> MAC mapping).",
        "syntax_win": "arp -a  |  arp -d *",
        "syntax_linux": "arp -a  |  ip neigh",
        "example": "arp -a",
        "notes": "-a shows cache, -d clears entry. Useful for ARP conflict diagnosis.",
    },
    "pathping (Windows)": {
        "purpose": "Combines ping and tracert -- shows packet loss per hop.",
        "syntax_win": "pathping <hostname_or_ip>",
        "syntax_linux": "mtr <hostname_or_ip> (equivalent)",
        "example": "pathping www.example.com",
        "notes": "Takes time to complete as it collects statistics over multiple rounds.",
    },
}


# ---------------------------------------------------------------------------
# Python Connectivity Checks
# ---------------------------------------------------------------------------

def check_ping(host: str, count: int = 4) -> str:
    """Ping a host and return the result summary."""
    param = "-n" if platform.system().lower() == "windows" else "-c"
    try:
        result = subprocess.run(
            ["ping", param, str(count), host],
            capture_output=True, text=True, timeout=30,
        )
        return result.stdout if result.returncode == 0 else f"Ping failed:\n{result.stderr}"
    except FileNotFoundError:
        return "Error: ping command not found."
    except subprocess.TimeoutExpired:
        return "Error: ping timed out."


def check_port(host: str, port: int, timeout: float = 3.0) -> str:
    """Check if a TCP port is open on a remote host."""
    try:
        with socket.create_connection((host, port), timeout=timeout):
            return f"Port {port} on {host} is OPEN."
    except (socket.timeout, ConnectionRefusedError, OSError) as exc:
        return f"Port {port} on {host} is CLOSED or unreachable ({exc})."


def check_dns(domain: str) -> str:
    """Resolve a domain name to IP addresses."""
    try:
        results = socket.getaddrinfo(domain, None)
        ips = sorted({r[4][0] for r in results})
        return f"{domain} resolves to: {', '.join(ips)}"
    except socket.gaierror as exc:
        return f"DNS resolution failed for {domain}: {exc}"


# ---------------------------------------------------------------------------
# Cable Types -- Physical Layer Reference
# ---------------------------------------------------------------------------

CABLE_TYPES = {
    "Cat5e": {
        "speed": "1 Gbps",
        "max_distance": "100 m (328 ft)",
        "frequency": "100 MHz",
        "connector": "RJ-45",
        "use_case": "Standard LAN -- adequate for most office environments",
    },
    "Cat6": {
        "speed": "10 Gbps (up to 55 m) / 1 Gbps (100 m)",
        "max_distance": "100 m (55 m for 10G)",
        "frequency": "250 MHz",
        "connector": "RJ-45",
        "use_case": "Higher performance LAN, short 10G runs",
    },
    "Cat6a": {
        "speed": "10 Gbps",
        "max_distance": "100 m (328 ft)",
        "frequency": "500 MHz",
        "connector": "RJ-45",
        "use_case": "Full-distance 10G, PoE++, data centers",
    },
    "Single-Mode Fiber (SMF)": {
        "speed": "Up to 100+ Gbps",
        "max_distance": "Up to 80+ km",
        "frequency": "N/A (light wavelength: 1310/1550 nm)",
        "connector": "LC, SC",
        "use_case": "Long-haul, WAN, campus backbone, ISP links",
    },
    "Multi-Mode Fiber (MMF)": {
        "speed": "Up to 100 Gbps (short distance)",
        "max_distance": "Up to 550 m (OM3/OM4 at 10G)",
        "frequency": "N/A (light wavelength: 850 nm)",
        "connector": "LC, SC, ST",
        "use_case": "Data centers, building backbone, short runs",
    },
    "Coaxial (RG-6)": {
        "speed": "Varies (cable broadband: ~1 Gbps DOCSIS 3.1)",
        "max_distance": "500+ m (depends on type)",
        "frequency": "Varies",
        "connector": "F-type, BNC",
        "use_case": "Cable internet, TV distribution",
    },
}


# ---------------------------------------------------------------------------
# Network Performance Metrics
# ---------------------------------------------------------------------------

PERFORMANCE_METRICS = {
    "Latency": {
        "definition": "Time for a packet to travel from source to destination (measured in ms).",
        "acceptable": "< 100 ms for most applications; < 30 ms for VoIP/gaming.",
        "tool": "ping (RTT), traceroute (per-hop latency)",
    },
    "Jitter": {
        "definition": "Variation in packet arrival times (inconsistent latency).",
        "acceptable": "< 30 ms for VoIP. High jitter causes choppy audio/video.",
        "tool": "iperf, network monitoring tools, QoS policies",
    },
    "Bandwidth": {
        "definition": "Maximum theoretical data transfer capacity of a link (e.g., 1 Gbps).",
        "acceptable": "Depends on requirements. Ensure sufficient headroom.",
        "tool": "Interface statistics, link speed negotiation",
    },
    "Throughput": {
        "definition": "Actual data transfer rate achieved (always <= bandwidth).",
        "acceptable": "Should be close to bandwidth under normal conditions.",
        "tool": "iperf, file transfer tests, SNMP monitoring",
    },
    "Packet Loss": {
        "definition": "Percentage of packets that fail to reach their destination.",
        "acceptable": "< 1% for most applications; 0% ideal for VoIP.",
        "tool": "ping (% loss), pathping/mtr (per-hop loss)",
    },
}


# ---------------------------------------------------------------------------
# Display Functions
# ---------------------------------------------------------------------------

def display_troubleshooting_methodology() -> None:
    print("\n" + "=" * 62)
    print("  COMPTIA TROUBLESHOOTING METHODOLOGY -- 7 Steps")
    print("  (N10-009 Objective 5.1)")
    print("=" * 62)
    for step_info in TROUBLESHOOTING_STEPS:
        print(f"\n  Step {step_info['step']}: {step_info['name']}")
        print(f"  {'-' * 56}")
        for action in step_info["actions"]:
            print(f"    * {action}")
    print()


def display_common_issues() -> None:
    print("\n" + "=" * 62)
    print("  COMMON NETWORK ISSUES & SYMPTOMS")
    print("=" * 62)
    for issue, info in COMMON_ISSUES.items():
        print(f"\n  {issue}")
        print(f"  {'-' * 56}")
        print("  Symptoms:")
        for s in info["symptoms"]:
            print(f"    -> {s}")
        print("  Possible Causes:")
        for c in info["possible_causes"]:
            print(f"    * {c}")
    print()


def display_cli_tools() -> None:
    print("\n" + "=" * 62)
    print("  COMMAND-LINE NETWORK TOOLS")
    print("=" * 62)
    for tool_name, info in CLI_TOOLS.items():
        print(f"\n  {tool_name}")
        print(f"  {'-' * 56}")
        print(f"  Purpose   : {info['purpose']}")
        print(f"  Windows   : {info['syntax_win']}")
        print(f"  Linux     : {info['syntax_linux']}")
        print(f"  Example   : {info['example']}")
        print(f"  Notes     : {info['notes']}")
    print()


def display_cable_types() -> None:
    print("\n" + "=" * 62)
    print("  CABLE TYPES -- Physical Layer Reference")
    print("=" * 62)
    for cable, info in CABLE_TYPES.items():
        print(f"\n  {cable}")
        print(f"  {'-' * 56}")
        for key, val in info.items():
            print(f"    {key:<14}: {val}")
    print()


def display_performance_metrics() -> None:
    print("\n" + "=" * 62)
    print("  NETWORK PERFORMANCE METRICS")
    print("=" * 62)
    for metric, info in PERFORMANCE_METRICS.items():
        print(f"\n  {metric}")
        print(f"  {'-' * 56}")
        print(f"    Definition : {info['definition']}")
        print(f"    Acceptable : {info['acceptable']}")
        print(f"    Measured By: {info['tool']}")
    print()


def display_connectivity_demo() -> None:
    print("\n" + "=" * 62)
    print("  PYTHON CONNECTIVITY CHECKS -- Live Demo")
    print("=" * 62)

    print("\n  [1] DNS Resolution Check:")
    print(f"      {check_dns('www.google.com')}")

    print("\n  [2] TCP Port Check (google.com:443):")
    print(f"      {check_port('www.google.com', 443)}")

    print("\n  [3] TCP Port Check (localhost:9999):")
    print(f"      {check_port('127.0.0.1', 9999, timeout=2.0)}")

    print()


# ---------------------------------------------------------------------------
# Main -- Standalone Execution
# ---------------------------------------------------------------------------

def main() -> None:
    print("=" * 62)
    print("  FLLC Enterprise IT -- Phase 11: Computer Networking")
    print("  CIS 270 | Network Troubleshooting | Preston Furulie")
    print("  Spring 2026 | CompTIA Network+ (N10-009)")
    print("=" * 62)

    display_troubleshooting_methodology()
    display_common_issues()
    display_cli_tools()
    display_cable_types()
    display_performance_metrics()
    display_connectivity_demo()

    print("\n" + "=" * 62)
    print("  End of Module -- Network Troubleshooting")
    print("=" * 62)


if __name__ == "__main__":
    main()
