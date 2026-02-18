"""
============================================================
FLLC Enterprise IT -- Phase 11: Computer Networking
CIS 270 -- Computer Networking | Preston Furulie
Spring 2026 | Portland Community College
CompTIA Network+ (N10-009) Aligned
============================================================
Module: IP Addressing & Subnetting
Topics: IPv4 classes, binary conversion, subnet masks,
        CIDR, network/broadcast calc, usable hosts,
        subnetting practice, VLSM, IPv6 overview
============================================================
"""


# ---------------------------------------------------------------------------
# IPv4 Address Classes
# ---------------------------------------------------------------------------

IPV4_CLASSES = {
    "A": {
        "range": "1.0.0.0 -- 126.255.255.255",
        "default_mask": "255.0.0.0 (/8)",
        "leading_bits": "0xxxxxxx",
        "network_bits": 8,
        "host_bits": 24,
        "max_networks": "126 (2^7 - 2)",
        "max_hosts": "16,777,214 (2^24 - 2)",
        "purpose": "Large organizations / ISPs",
        "private_range": "10.0.0.0 -- 10.255.255.255",
    },
    "B": {
        "range": "128.0.0.0 -- 191.255.255.255",
        "default_mask": "255.255.0.0 (/16)",
        "leading_bits": "10xxxxxx",
        "network_bits": 16,
        "host_bits": 16,
        "max_networks": "16,384 (2^14)",
        "max_hosts": "65,534 (2^16 - 2)",
        "purpose": "Medium-sized organizations",
        "private_range": "172.16.0.0 -- 172.31.255.255",
    },
    "C": {
        "range": "192.0.0.0 -- 223.255.255.255",
        "default_mask": "255.255.255.0 (/24)",
        "leading_bits": "110xxxxx",
        "network_bits": 24,
        "host_bits": 8,
        "max_networks": "2,097,152 (2^21)",
        "max_hosts": "254 (2^8 - 2)",
        "purpose": "Small organizations / home networks",
        "private_range": "192.168.0.0 -- 192.168.255.255",
    },
    "D": {
        "range": "224.0.0.0 -- 239.255.255.255",
        "default_mask": "N/A",
        "leading_bits": "1110xxxx",
        "network_bits": "N/A",
        "host_bits": "N/A",
        "max_networks": "N/A",
        "max_hosts": "N/A",
        "purpose": "Multicast",
        "private_range": "N/A",
    },
    "E": {
        "range": "240.0.0.0 -- 255.255.255.255",
        "default_mask": "N/A",
        "leading_bits": "1111xxxx",
        "network_bits": "N/A",
        "host_bits": "N/A",
        "max_networks": "N/A",
        "max_hosts": "N/A",
        "purpose": "Experimental / Reserved",
        "private_range": "N/A",
    },
}

SPECIAL_ADDRESSES = {
    "127.0.0.0/8": "Loopback (localhost)",
    "169.254.0.0/16": "APIPA (link-local, auto-assigned when DHCP fails)",
    "0.0.0.0": "Default route / unspecified address",
    "255.255.255.255": "Limited broadcast",
}


# ---------------------------------------------------------------------------
# Binary <-> Decimal Conversion
# ---------------------------------------------------------------------------

def ip_to_binary(ip: str) -> str:
    """Convert a dotted-decimal IPv4 address to binary notation."""
    octets = ip.strip().split(".")
    binary_octets = [format(int(o), "08b") for o in octets]
    return ".".join(binary_octets)


def binary_to_ip(binary_str: str) -> str:
    """Convert a binary IPv4 string (with dots) back to dotted-decimal."""
    octets = binary_str.strip().split(".")
    return ".".join(str(int(o, 2)) for o in octets)


def ip_to_int(ip: str) -> int:
    """Convert dotted-decimal IP to a 32-bit integer."""
    parts = ip.strip().split(".")
    return (int(parts[0]) << 24) + (int(parts[1]) << 16) + \
           (int(parts[2]) << 8) + int(parts[3])


def int_to_ip(num: int) -> str:
    """Convert a 32-bit integer to dotted-decimal IP."""
    return f"{(num >> 24) & 0xFF}.{(num >> 16) & 0xFF}.{(num >> 8) & 0xFF}.{num & 0xFF}"


# ---------------------------------------------------------------------------
# Subnet Mask & CIDR Utilities
# ---------------------------------------------------------------------------

def cidr_to_mask(prefix_len: int) -> str:
    """Convert CIDR prefix length to dotted-decimal subnet mask."""
    mask_int = (0xFFFFFFFF << (32 - prefix_len)) & 0xFFFFFFFF
    return int_to_ip(mask_int)


def mask_to_cidr(mask: str) -> int:
    """Convert dotted-decimal subnet mask to CIDR prefix length."""
    return bin(ip_to_int(mask)).count("1")


COMMON_MASKS = {
    "/24": {"mask": "255.255.255.0",   "hosts": 254,  "subnets_from_c": 1},
    "/25": {"mask": "255.255.255.128", "hosts": 126,  "subnets_from_c": 2},
    "/26": {"mask": "255.255.255.192", "hosts": 62,   "subnets_from_c": 4},
    "/27": {"mask": "255.255.255.224", "hosts": 30,   "subnets_from_c": 8},
    "/28": {"mask": "255.255.255.240", "hosts": 14,   "subnets_from_c": 16},
    "/29": {"mask": "255.255.255.248", "hosts": 6,    "subnets_from_c": 32},
    "/30": {"mask": "255.255.255.252", "hosts": 2,    "subnets_from_c": 64},
    "/31": {"mask": "255.255.255.254", "hosts": 0,    "subnets_from_c": 128},
    "/32": {"mask": "255.255.255.255", "hosts": 0,    "subnets_from_c": 256},
}


# ---------------------------------------------------------------------------
# Network / Broadcast / Usable Host Calculations
# ---------------------------------------------------------------------------

def calculate_subnet_info(ip: str, prefix_len: int) -> dict:
    """Given an IP and CIDR prefix, compute full subnet details."""
    ip_int = ip_to_int(ip)
    mask_int = (0xFFFFFFFF << (32 - prefix_len)) & 0xFFFFFFFF
    wildcard_int = mask_int ^ 0xFFFFFFFF

    network_int = ip_int & mask_int
    broadcast_int = network_int | wildcard_int

    host_bits = 32 - prefix_len
    total_addresses = 2 ** host_bits
    usable_hosts = max(total_addresses - 2, 0)

    first_host = network_int + 1 if usable_hosts > 0 else network_int
    last_host = broadcast_int - 1 if usable_hosts > 0 else broadcast_int

    return {
        "ip_address": ip,
        "prefix_length": prefix_len,
        "subnet_mask": int_to_ip(mask_int),
        "wildcard_mask": int_to_ip(wildcard_int),
        "network_address": int_to_ip(network_int),
        "broadcast_address": int_to_ip(broadcast_int),
        "first_usable_host": int_to_ip(first_host),
        "last_usable_host": int_to_ip(last_host),
        "total_addresses": total_addresses,
        "usable_hosts": usable_hosts,
        "binary_mask": ip_to_binary(int_to_ip(mask_int)),
        "binary_ip": ip_to_binary(ip),
    }


# ---------------------------------------------------------------------------
# VLSM -- Variable Length Subnet Masking
# ---------------------------------------------------------------------------

VLSM_EXPLANATION = """
VARIABLE LENGTH SUBNET MASKING (VLSM)
--------------------------------------
VLSM allows different subnets within the same network to use different
subnet mask lengths. This maximizes address efficiency by allocating
only the needed number of addresses to each subnet.

Steps for VLSM Design:
  1. List all subnets and required host counts (largest first).
  2. Assign the largest subnet first from the available address space.
  3. Calculate the prefix length: find smallest n where (2^n - 2) >= hosts needed.
  4. Record the network address and move to the next available block.
  5. Repeat for the next-largest subnet requirement.

Example -- Network 192.168.10.0/24 split via VLSM:
  Dept A: 100 hosts -> /25 (126 usable) -> 192.168.10.0/25
  Dept B:  50 hosts -> /26 (62 usable)  -> 192.168.10.128/26
  Dept C:  25 hosts -> /27 (30 usable)  -> 192.168.10.192/27
  WAN link:  2 hosts -> /30 (2 usable)  -> 192.168.10.224/30
"""


# ---------------------------------------------------------------------------
# Subnetting Practice Problems
# ---------------------------------------------------------------------------

PRACTICE_PROBLEMS = [
    {
        "question": "Subnet 192.168.1.0/24 into 4 equal subnets. What is the new mask?",
        "answer": "/26 (255.255.255.192) -- 4 subnets with 62 usable hosts each.",
        "subnets": [
            "192.168.1.0/26   (hosts: .1 -- .62,   broadcast: .63)",
            "192.168.1.64/26  (hosts: .65 -- .126,  broadcast: .127)",
            "192.168.1.128/26 (hosts: .129 -- .190, broadcast: .191)",
            "192.168.1.192/26 (hosts: .193 -- .254, broadcast: .255)",
        ],
    },
    {
        "question": "What is the network address for host 172.16.45.130/20?",
        "answer": "172.16.32.0 -- The /20 mask is 255.255.240.0.",
    },
    {
        "question": "How many usable hosts in a /27 network?",
        "answer": "30 usable hosts (2^5 - 2 = 30).",
    },
    {
        "question": "Given 10.0.0.0/8, what prefix creates subnets with 1022 hosts each?",
        "answer": "/22 (255.255.252.0) -- 2^10 - 2 = 1022 usable hosts per subnet.",
    },
    {
        "question": "What is the broadcast address for 192.168.50.0/28?",
        "answer": "192.168.50.15 -- The block size is 16; broadcast = network + 15.",
    },
]


# ---------------------------------------------------------------------------
# IPv6 Overview
# ---------------------------------------------------------------------------

IPV6_INFO = {
    "format": "128-bit address written as 8 groups of 4 hex digits (e.g., 2001:0db8:85a3:0000:0000:8a2e:0370:7334)",
    "shortening_rules": [
        "Leading zeros in each group can be omitted: 0db8 -> db8",
        "One consecutive group of all-zero blocks can be replaced with :: (once per address)",
        "Example: 2001:0db8:0000:0000:0000:0000:0000:0001 -> 2001:db8::1",
    ],
    "address_types": {
        "Unicast": "Identifies a single interface (Global, Link-Local, Unique Local)",
        "Multicast": "One-to-many delivery (replaces broadcast in IPv4) -- ff00::/8",
        "Anycast": "Assigned to multiple interfaces; routed to the nearest one",
    },
    "special_addresses": {
        "::1": "Loopback (equivalent to 127.0.0.1)",
        "::": "Unspecified address (equivalent to 0.0.0.0)",
        "fe80::/10": "Link-local addresses (auto-configured, not routable)",
        "2000::/3": "Global unicast (routable on the internet)",
        "fc00::/7": "Unique local addresses (similar to RFC 1918 private)",
        "ff00::/8": "Multicast addresses",
    },
    "prefix_length": "/64 is the standard subnet size (2^64 host addresses per subnet)",
    "differences_from_ipv4": [
        "128-bit vs 32-bit address space",
        "No broadcast -- uses multicast instead",
        "No NAT needed -- every device gets a global address",
        "Built-in IPsec support",
        "Simplified header (no checksum, no fragmentation by routers)",
        "SLAAC (Stateless Address Auto-Configuration) for automatic addressing",
    ],
}


# ---------------------------------------------------------------------------
# Display Functions
# ---------------------------------------------------------------------------

def display_ipv4_classes() -> None:
    print("\n" + "=" * 62)
    print("  IPv4 ADDRESS CLASSES")
    print("=" * 62)
    for cls_name, info in IPV4_CLASSES.items():
        print(f"\n  Class {cls_name}")
        print(f"  {'-' * 56}")
        for key, val in info.items():
            print(f"    {key:<16}: {val}")

    print(f"\n  Special Addresses:")
    print(f"  {'-' * 56}")
    for addr, desc in SPECIAL_ADDRESSES.items():
        print(f"    {addr:<22} {desc}")
    print()


def display_binary_demo() -> None:
    print("\n" + "=" * 62)
    print("  BINARY <-> DECIMAL CONVERSION DEMO")
    print("=" * 62)
    examples = ["192.168.1.1", "10.0.0.1", "172.16.254.100", "255.255.255.0"]
    for ip in examples:
        binary = ip_to_binary(ip)
        back = binary_to_ip(binary)
        print(f"  {ip:<20} -> {binary:<35} -> {back}")
    print()


def display_common_masks() -> None:
    print("\n" + "=" * 62)
    print("  COMMON SUBNET MASKS -- CIDR REFERENCE")
    print("=" * 62)
    print(f"  {'CIDR':<8} {'Subnet Mask':<20} {'Usable Hosts':<14} {'Subnets(/24)'}")
    print(f"  {'-' * 56}")
    for cidr, info in COMMON_MASKS.items():
        print(f"  {cidr:<8} {info['mask']:<20} {info['hosts']:<14} {info['subnets_from_c']}")
    print()


def display_subnet_calculation(ip: str, prefix: int) -> None:
    info = calculate_subnet_info(ip, prefix)
    print(f"\n  Subnet Calculation for {ip}/{prefix}")
    print(f"  {'-' * 56}")
    print(f"    Subnet Mask      : {info['subnet_mask']}")
    print(f"    Wildcard Mask    : {info['wildcard_mask']}")
    print(f"    Network Address  : {info['network_address']}")
    print(f"    Broadcast Address: {info['broadcast_address']}")
    print(f"    First Usable Host: {info['first_usable_host']}")
    print(f"    Last Usable Host : {info['last_usable_host']}")
    print(f"    Total Addresses  : {info['total_addresses']}")
    print(f"    Usable Hosts     : {info['usable_hosts']}")
    print(f"    Binary IP        : {info['binary_ip']}")
    print(f"    Binary Mask      : {info['binary_mask']}")


def display_practice_problems() -> None:
    print("\n" + "=" * 62)
    print("  SUBNETTING PRACTICE PROBLEMS")
    print("=" * 62)
    for i, prob in enumerate(PRACTICE_PROBLEMS, 1):
        print(f"\n  Problem {i}: {prob['question']}")
        print(f"  Answer  : {prob['answer']}")
        if "subnets" in prob:
            for s in prob["subnets"]:
                print(f"            {s}")
    print()


def display_vlsm() -> None:
    print("\n" + "=" * 62)
    print(VLSM_EXPLANATION)
    print("=" * 62)


def display_ipv6_overview() -> None:
    print("\n" + "=" * 62)
    print("  IPv6 OVERVIEW")
    print("=" * 62)
    print(f"  Format: {IPV6_INFO['format']}")
    print(f"  Standard Prefix: {IPV6_INFO['prefix_length']}")

    print(f"\n  Shortening Rules:")
    for rule in IPV6_INFO["shortening_rules"]:
        print(f"    * {rule}")

    print(f"\n  Address Types:")
    for atype, desc in IPV6_INFO["address_types"].items():
        print(f"    {atype:<12}: {desc}")

    print(f"\n  Special Addresses:")
    for addr, desc in IPV6_INFO["special_addresses"].items():
        print(f"    {addr:<14} {desc}")

    print(f"\n  Key Differences from IPv4:")
    for diff in IPV6_INFO["differences_from_ipv4"]:
        print(f"    * {diff}")
    print()


# ---------------------------------------------------------------------------
# Main -- Standalone Execution
# ---------------------------------------------------------------------------

def main() -> None:
    print("=" * 62)
    print("  FLLC Enterprise IT -- Phase 11: Computer Networking")
    print("  CIS 270 | IP Addressing & Subnetting | Preston Furulie")
    print("  Spring 2026 | CompTIA Network+ (N10-009)")
    print("=" * 62)

    display_ipv4_classes()
    display_binary_demo()
    display_common_masks()

    print("\n" + "=" * 62)
    print("  SUBNET CALCULATIONS -- Examples")
    print("=" * 62)
    display_subnet_calculation("192.168.1.100", 24)
    display_subnet_calculation("10.0.50.200", 22)
    display_subnet_calculation("172.16.0.1", 28)

    display_practice_problems()
    display_vlsm()
    display_ipv6_overview()

    print("\n" + "=" * 62)
    print("  End of Module -- IP Addressing & Subnetting")
    print("=" * 62)


if __name__ == "__main__":
    main()
