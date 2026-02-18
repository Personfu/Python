# ============================================================
# Assignment — Security Fundamentals
# CIS 156 — Computer Science Concepts | FLLC Enterprise
# Author: Preston Furulie
# ============================================================
# CompTIA ITF+ Alignment: Security domain — understanding core
# security principles, threat categories, encryption basics,
# and best practices for protecting systems and data.
# ============================================================

"""
Security Fundamentals
=====================
Information security protects data from unauthorized access,
modification, or destruction. This module covers the CIA triad,
authentication, common threats, password hygiene, basic
cryptography, and firewall concepts.
"""

import hashlib
import string
import re


# ────────────────────────────────────────────────────────────
# 1. CIA TRIAD
# ────────────────────────────────────────────────────────────
# The three pillars of information security. Every security
# control maps back to at least one of these principles.

def cia_triad_demo():
    """Explain and illustrate the CIA triad."""
    print(f"\n{'='*60}")
    print("1. THE CIA TRIAD")
    print(f"{'='*60}")

    pillars = {
        "Confidentiality": {
            "definition": "Only authorized parties can access the data.",
            "controls": [
                "Encryption (AES, TLS)",
                "Access control lists (ACLs)",
                "Multi-factor authentication (MFA)",
                "Data classification labels",
            ],
            "example": "FLLC encrypts employee records at rest and in transit.",
        },
        "Integrity": {
            "definition": "Data has not been altered by unauthorized means.",
            "controls": [
                "Hashing (SHA-256 checksums)",
                "Digital signatures",
                "Version control systems",
                "Input validation",
            ],
            "example": "FLLC verifies file checksums after every backup.",
        },
        "Availability": {
            "definition": "Systems and data are accessible when needed.",
            "controls": [
                "Redundant servers and failover",
                "Regular backups and disaster recovery",
                "DDoS mitigation",
                "UPS and generator power",
            ],
            "example": "FLLC maintains 99.9% uptime with load-balanced servers.",
        },
    }

    for pillar, info in pillars.items():
        print(f"\n  {pillar}")
        print(f"    Definition : {info['definition']}")
        print(f"    Controls   :")
        for ctrl in info["controls"]:
            print(f"      - {ctrl}")
        print(f"    FLLC Example: {info['example']}")


# ────────────────────────────────────────────────────────────
# 2. AUTHENTICATION vs AUTHORIZATION
# ────────────────────────────────────────────────────────────

def auth_demo():
    """Clarify the difference between authentication and authorization."""
    print(f"\n{'='*60}")
    print("2. AUTHENTICATION vs AUTHORIZATION")
    print(f"{'='*60}")

    print(f"""
  Authentication ("Who are you?")
    - Verifies the IDENTITY of a user or system
    - Methods: password, biometrics, token, certificate, MFA
    - Example: Logging in with username + password + OTP

  Authorization ("What can you do?")
    - Determines the PERMISSIONS of an authenticated entity
    - Methods: role-based (RBAC), attribute-based (ABAC), ACLs
    - Example: An intern can read reports but cannot delete them

  Comparison:
  {'Feature':<20} {'Authentication':<26} {'Authorization'}
  {'-'*20} {'-'*26} {'-'*20}
  {"Question":<20} {"Who are you?":<26} {"What are you allowed?"}
  {"Happens":<20} {"First":<26} {"After authentication"}
  {"Visible to user":<20} {"Yes (login screen)":<26} {"Often invisible"}
  {"Controlled by":<20} {"Identity provider":<26} {"Resource owner / policy"}
    """)

    users = {
        "admin":  {"password": "S3cur3!Pass", "role": "administrator"},
        "pfurulie": {"password": "Fllc2026#", "role": "developer"},
        "intern":  {"password": "Summer26!", "role": "read-only"},
    }

    permissions = {
        "administrator": ["read", "write", "delete", "admin"],
        "developer":     ["read", "write"],
        "read-only":     ["read"],
    }

    print("  FLLC User Directory:")
    print(f"  {'Username':<12} {'Role':<16} {'Permissions'}")
    print(f"  {'-'*12} {'-'*16} {'-'*30}")
    for user, info in users.items():
        role = info["role"]
        perms = ", ".join(permissions[role])
        print(f"  {user:<12} {role:<16} {perms}")


# ────────────────────────────────────────────────────────────
# 3. COMMON THREATS
# ────────────────────────────────────────────────────────────
# CompTIA ITF+ expects awareness of major threat categories.

def common_threats_demo():
    """Catalog common cybersecurity threats."""
    print(f"\n{'='*60}")
    print("3. COMMON CYBERSECURITY THREATS")
    print(f"{'='*60}")

    threats = [
        ("Phishing",
         "Fraudulent email/site tricks user into revealing credentials",
         "Verify sender, hover over links, use email filtering"),
        ("Ransomware",
         "Malware encrypts victim's files; demands payment for key",
         "Regular backups, endpoint protection, user training"),
        ("Virus",
         "Self-replicating code that attaches to legitimate programs",
         "Antivirus software, avoid untrusted downloads"),
        ("Trojan",
         "Malicious software disguised as legitimate application",
         "Download only from trusted sources, code signing"),
        ("Worm",
         "Self-propagating malware that spreads without user action",
         "Patch management, network segmentation"),
        ("Social Engineering",
         "Manipulating people to divulge confidential information",
         "Security awareness training, verification procedures"),
        ("Man-in-the-Middle",
         "Attacker intercepts communication between two parties",
         "Use HTTPS/TLS, VPN, certificate pinning"),
        ("DDoS",
         "Overwhelms a service with traffic to cause unavailability",
         "Rate limiting, CDN, traffic scrubbing services"),
    ]

    for name, desc, mitigation in threats:
        print(f"\n  {name}")
        print(f"    Description : {desc}")
        print(f"    Mitigation  : {mitigation}")


# ────────────────────────────────────────────────────────────
# 4. PASSWORD STRENGTH CHECKER
# ────────────────────────────────────────────────────────────
# Strong passwords are a first line of defense. NIST 800-63B
# recommends length over complexity, but ITF+ still tests on
# traditional complexity rules.

def check_password_strength(password):
    """Evaluate a password against common strength criteria."""
    checks = {
        "Length >= 12 characters": len(password) >= 12,
        "Contains uppercase":     bool(re.search(r"[A-Z]", password)),
        "Contains lowercase":     bool(re.search(r"[a-z]", password)),
        "Contains digit":         bool(re.search(r"\d", password)),
        "Contains special char":  bool(re.search(r"[!@#$%^&*(),.?\":{}|<>]", password)),
        "No common patterns":     password.lower() not in (
            "password", "123456", "qwerty", "letmein", "admin"
        ),
    }
    score = sum(checks.values())
    if score >= 6:
        strength = "STRONG"
    elif score >= 4:
        strength = "MODERATE"
    else:
        strength = "WEAK"
    return checks, score, strength


def password_demo():
    """Demonstrate password strength evaluation."""
    print(f"\n{'='*60}")
    print("4. PASSWORD STRENGTH CHECKER")
    print(f"{'='*60}")

    test_passwords = [
        "password",
        "Fllc2026",
        "S3cur3!Passw0rd#2026",
        "correct horse battery staple",
    ]

    for pw in test_passwords:
        checks, score, strength = check_password_strength(pw)
        masked = pw[:3] + "*" * (len(pw) - 3)
        print(f"\n  Password: {masked}  ({len(pw)} chars)")
        for rule, passed in checks.items():
            status = "PASS" if passed else "FAIL"
            print(f"    [{status}] {rule}")
        print(f"  Score: {score}/6 — {strength}")

    print("\n  Best Practices:")
    practices = [
        "Use a unique password for every account",
        "Prefer passphrases (4+ random words) for memorability",
        "Enable multi-factor authentication (MFA) everywhere",
        "Use a password manager to generate and store credentials",
        "Never share passwords via email or chat",
    ]
    for i, p in enumerate(practices, 1):
        print(f"    {i}. {p}")


# ────────────────────────────────────────────────────────────
# 5. BASIC ENCRYPTION CONCEPTS
# ────────────────────────────────────────────────────────────

def caesar_cipher(text, shift):
    """Classic substitution cipher — shifts each letter by 'shift' positions."""
    result = []
    for ch in text:
        if ch.isalpha():
            base = ord("A") if ch.isupper() else ord("a")
            result.append(chr((ord(ch) - base + shift) % 26 + base))
        else:
            result.append(ch)
    return "".join(result)


def encryption_demo():
    """Demonstrate Caesar cipher and hashing fundamentals."""
    print(f"\n{'='*60}")
    print("5. BASIC ENCRYPTION CONCEPTS")
    print(f"{'='*60}")

    print("\n  --- Caesar Cipher (symmetric substitution) ---")
    plaintext = "FLLC Enterprise Security"
    shift = 3
    encrypted = caesar_cipher(plaintext, shift)
    decrypted = caesar_cipher(encrypted, -shift)
    print(f"  Plaintext  : {plaintext}")
    print(f"  Shift      : {shift}")
    print(f"  Encrypted  : {encrypted}")
    print(f"  Decrypted  : {decrypted}")

    print("\n  --- Hashing (one-way, not encryption) ---")
    print("  Hashing produces a fixed-size digest; it cannot be reversed.")
    samples = ["password123", "FLLC2026", "S3cur3!Passw0rd#2026"]
    print(f"\n  {'Input':<28} {'SHA-256 Hash (first 32 chars)'}")
    print(f"  {'-'*28} {'-'*40}")
    for sample in samples:
        digest = hashlib.sha256(sample.encode()).hexdigest()
        print(f"  {sample:<28} {digest[:32]}...")

    print("\n  Encryption vs Hashing:")
    print(f"  {'Attribute':<18} {'Encryption':<26} {'Hashing'}")
    print(f"  {'-'*18} {'-'*26} {'-'*22}")
    print(f"  {'Reversible':<18} {'Yes (with key)':<26} {'No'}")
    print(f"  {'Purpose':<18} {'Protect data in transit':<26} {'Verify integrity'}")
    print(f"  {'Output size':<18} {'Variable':<26} {'Fixed (e.g., 256 bits)'}")


# ────────────────────────────────────────────────────────────
# 6. FIREWALL CONCEPTS
# ────────────────────────────────────────────────────────────

def firewall_demo():
    """Explain firewall types and demonstrate a simple rule set."""
    print(f"\n{'='*60}")
    print("6. FIREWALL CONCEPTS")
    print(f"{'='*60}")

    print("""
  A firewall monitors and controls network traffic based on
  predetermined security rules. It establishes a barrier between
  trusted internal networks and untrusted external networks.

  Types of Firewalls:
    - Packet Filter    : Inspects headers (IP, port, protocol)
    - Stateful         : Tracks connection state (new, established)
    - Application-layer: Inspects payload content (deep inspection)
    - Next-Gen (NGFW)  : Combines stateful + app awareness + IPS
    """)

    rules = [
        {"id": 1, "action": "ALLOW", "proto": "TCP", "src": "ANY",
         "dst": "192.168.1.10", "port": 443, "desc": "HTTPS to web server"},
        {"id": 2, "action": "ALLOW", "proto": "TCP", "src": "ANY",
         "dst": "192.168.1.10", "port": 80,  "desc": "HTTP to web server"},
        {"id": 3, "action": "ALLOW", "proto": "TCP", "src": "10.0.0.0/8",
         "dst": "192.168.1.30", "port": 5432, "desc": "PostgreSQL (internal)"},
        {"id": 4, "action": "DENY",  "proto": "TCP", "src": "ANY",
         "dst": "192.168.1.30", "port": 5432, "desc": "Block ext DB access"},
        {"id": 5, "action": "ALLOW", "proto": "ICMP", "src": "10.0.0.0/8",
         "dst": "ANY",          "port": "-",  "desc": "Internal ping"},
        {"id": 6, "action": "DENY",  "proto": "ANY", "src": "ANY",
         "dst": "ANY",          "port": "-",  "desc": "Default deny all"},
    ]

    print("  FLLC Enterprise Firewall Rules:")
    header = (f"  {'#':<4} {'Action':<8} {'Proto':<6} "
              f"{'Source':<16} {'Destination':<16} {'Port':<6} {'Description'}")
    print(header)
    print(f"  {'-'*80}")
    for r in rules:
        print(f"  {r['id']:<4} {r['action']:<8} {r['proto']:<6} "
              f"{r['src']:<16} {r['dst']:<16} {str(r['port']):<6} {r['desc']}")

    print("\n  Rule evaluation is top-down; first match wins.")
    print("  The final 'DENY ALL' is the implicit default policy.")


# ────────────────────────────────────────────────────────────
# 7. CompTIA ITF+ SECURITY DOMAIN SUMMARY
# ────────────────────────────────────────────────────────────

def itf_security_summary():
    """Map module topics to CompTIA ITF+ security exam objectives."""
    print(f"\n{'='*60}")
    print("7. CompTIA ITF+ — SECURITY DOMAIN OBJECTIVES")
    print(f"{'='*60}")

    objectives = [
        ("6.1", "Summarize confidentiality, integrity, and availability"),
        ("6.2", "Explain methods used to secure devices and networks"),
        ("6.3", "Compare and contrast authentication methods"),
        ("6.4", "Explain password best practices"),
        ("6.5", "Explain common social-engineering threats"),
        ("6.6", "Explain the differences between encryption and hashing"),
        ("6.7", "Explain business continuity concepts"),
    ]

    print(f"\n  {'Objective':<10} {'Description'}")
    print(f"  {'-'*10} {'-'*50}")
    for obj_id, desc in objectives:
        print(f"  {obj_id:<10} {desc}")

    print("\n  All topics in this module map directly to the ITF+")
    print("  Security domain (approximately 20% of the exam).")


# ────────────────────────────────────────────────────────────
# MAIN — Run all demonstrations
# ────────────────────────────────────────────────────────────

def main():
    print("=" * 60)
    print("  CIS 156 — Security Fundamentals")
    print("  FLLC Enterprise | Preston Furulie | Spring 2026")
    print("=" * 60)

    cia_triad_demo()
    auth_demo()
    common_threats_demo()
    password_demo()
    encryption_demo()
    firewall_demo()
    itf_security_summary()

    print(f"\n{'='*60}")
    print("  End of Security Fundamentals Module")
    print(f"{'='*60}")


if __name__ == "__main__":
    main()
