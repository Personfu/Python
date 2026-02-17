# ============================================================
# Encryption & Hashing — Complete Implementation
# CIS 350 — Network & Cybersecurity | Preston Furulie
# ============================================================
# Covers: hash functions (MD5, SHA family), salted hashing,
# HMAC, PBKDF2 key derivation, password strength analysis,
# file integrity checking, Caesar cipher, XOR encryption,
# and timing attack demonstration.
# ============================================================

import hashlib
import hmac
import secrets
import string
import os
import time

print("=" * 60)
print("  ENCRYPTION & HASHING — CIS 350 | Preston Furulie")
print("=" * 60)


# ── Section 1: Hash Function Comparison ─────────────────────

print("\n--- Section 1: Hash Algorithms ---")
message = "The quick brown fox jumps over the lazy dog"

algorithms = {
    "MD5":     hashlib.md5,
    "SHA-1":   hashlib.sha1,
    "SHA-256": hashlib.sha256,
    "SHA-384": hashlib.sha384,
    "SHA-512": hashlib.sha512,
}

print(f"  Message: \"{message}\"\n")
print(f"  {'Algorithm':<10} {'Bits':>5}  {'Hash'}")
print(f"  {'─' * 70}")
for name, func in algorithms.items():
    digest = func(message.encode()).hexdigest()
    bits = len(digest) * 4
    print(f"  {name:<10} {bits:>5}  {digest}")

# Avalanche effect: tiny change → completely different hash
print(f"\n  Avalanche Effect (change one character):")
msg1 = "Hello World"
msg2 = "Hello World!"
h1 = hashlib.sha256(msg1.encode()).hexdigest()
h2 = hashlib.sha256(msg2.encode()).hexdigest()
print(f"  \"{msg1}\"  → {h1[:32]}...")
print(f"  \"{msg2}\" → {h2[:32]}...")
diff_bits = sum(c1 != c2 for c1, c2 in zip(h1, h2))
print(f"  Different hex digits: {diff_bits}/{len(h1)} ({diff_bits/len(h1)*100:.0f}%)")


# ── Section 2: Salted Password Hashing ──────────────────────

print("\n--- Section 2: Salted Password Hashing ---")

def hash_password(password, salt=None):
    """Hash a password with a random salt.
    Salt prevents rainbow table attacks by making each hash unique
    even for identical passwords."""
    if salt is None:
        salt = secrets.token_hex(16)  # 32-char hex = 128-bit salt
    salted = salt + password
    hashed = hashlib.sha256(salted.encode()).hexdigest()
    return salt, hashed

def verify_password(password, salt, expected_hash):
    """Verify a password against its stored salt and hash."""
    _, computed_hash = hash_password(password, salt)
    return hmac.compare_digest(computed_hash, expected_hash)

# Demonstrate: same password, different salts → different hashes
password = "SecureP@ss2026!"
salt1, hash1 = hash_password(password)
salt2, hash2 = hash_password(password)
print(f"  Password: {password}")
print(f"  Salt 1: {salt1}")
print(f"  Hash 1: {hash1}")
print(f"  Salt 2: {salt2}")
print(f"  Hash 2: {hash2}")
print(f"  Same hash? {hash1 == hash2}  (different salts = different hashes)")
print(f"\n  Verify correct password: {verify_password(password, salt1, hash1)}")
print(f"  Verify wrong password:   {verify_password('WrongPass', salt1, hash1)}")


# ── Section 3: PBKDF2 (Key Derivation) ─────────────────────

print("\n--- Section 3: PBKDF2 Key Derivation ---")

def pbkdf2_hash(password, salt=None, iterations=600_000):
    """PBKDF2: Password-Based Key Derivation Function 2.
    Applies the hash function many times (iterations) to make
    brute-force attacks computationally expensive.
    NIST recommends >= 600,000 iterations for SHA-256."""
    if salt is None:
        salt = os.urandom(16)  # 128-bit random salt
    key = hashlib.pbkdf2_hmac(
        "sha256",
        password.encode(),
        salt,
        iterations,
        dklen=32   # 256-bit derived key
    )
    return salt, key.hex(), iterations

salt, key, iters = pbkdf2_hash("MyPassword123")
print(f"  Iterations: {iters:,}")
print(f"  Salt:       {salt.hex()}")
print(f"  Key:        {key}")


# ── Section 4: HMAC (Hash-based Message Authentication) ─────

print("\n--- Section 4: HMAC ---")

def create_hmac(message, secret_key):
    """Create an HMAC to verify message integrity AND authenticity.
    Unlike a plain hash, HMAC requires a shared secret key."""
    return hmac.new(
        secret_key.encode(),
        message.encode(),
        hashlib.sha256
    ).hexdigest()

def verify_hmac(message, secret_key, received_mac):
    """Verify HMAC using constant-time comparison (prevents timing attacks)."""
    computed = create_hmac(message, secret_key)
    return hmac.compare_digest(computed, received_mac)

secret = "my_secret_api_key_2026"
msg = "Transfer $500 to account 12345"
mac = create_hmac(msg, secret)

print(f"  Message: {msg}")
print(f"  HMAC:    {mac}")
print(f"  Valid:   {verify_hmac(msg, secret, mac)}")
# Tampered message
tampered = "Transfer $50000 to account 12345"
print(f"\n  Tampered: {tampered}")
print(f"  Valid:    {verify_hmac(tampered, secret, mac)}")


# ── Section 5: Password Strength Analyzer ───────────────────

print("\n--- Section 5: Password Strength Analyzer ---")

def analyze_password(password):
    """Analyze password strength and estimate crack time."""
    score = 0
    feedback = []
    length = len(password)

    # Length scoring
    if length >= 16:
        score += 3
    elif length >= 12:
        score += 2
    elif length >= 8:
        score += 1
    else:
        feedback.append("Too short (minimum 8 characters)")

    # Character diversity
    has_lower = any(c in string.ascii_lowercase for c in password)
    has_upper = any(c in string.ascii_uppercase for c in password)
    has_digit = any(c in string.digits for c in password)
    has_special = any(c in string.punctuation for c in password)

    char_types = sum([has_lower, has_upper, has_digit, has_special])
    score += char_types

    if not has_upper:
        feedback.append("Add uppercase letters")
    if not has_digit:
        feedback.append("Add numbers")
    if not has_special:
        feedback.append("Add special characters (!@#$%)")

    # Common patterns
    common = ["password", "123456", "qwerty", "admin", "letmein"]
    if password.lower() in common:
        score = 0
        feedback.append("Extremely common password")

    # Estimate entropy
    pool_size = 0
    if has_lower: pool_size += 26
    if has_upper: pool_size += 26
    if has_digit: pool_size += 10
    if has_special: pool_size += 32
    entropy = length * (pool_size.bit_length() if pool_size > 0 else 0)

    # Strength label
    if score >= 6:
        strength = "STRONG"
    elif score >= 4:
        strength = "MODERATE"
    elif score >= 2:
        strength = "WEAK"
    else:
        strength = "VERY WEAK"

    return {
        "password": password,
        "length": length,
        "score": score,
        "strength": strength,
        "entropy_bits": entropy,
        "char_types": char_types,
        "feedback": feedback
    }

test_passwords = [
    "password",
    "Hello123",
    "MyP@ssw0rd!",
    "c0rr3ct-H0rse-B@ttery-St@ple!",
]

for pw in test_passwords:
    result = analyze_password(pw)
    print(f"\n  Password: {result['password']}")
    print(f"    Strength:    {result['strength']} (score: {result['score']}/7)")
    print(f"    Length:      {result['length']}")
    print(f"    Char types:  {result['char_types']}/4")
    print(f"    Entropy:     ~{result['entropy_bits']} bits")
    if result['feedback']:
        print(f"    Feedback:    {', '.join(result['feedback'])}")


# ── Section 6: Caesar Cipher (Classical Encryption) ─────────

print("\n--- Section 6: Caesar Cipher ---")

def caesar_encrypt(plaintext, shift):
    """Caesar cipher: shift each letter by N positions.
    Historical: used by Julius Caesar with shift=3."""
    result = []
    for char in plaintext:
        if char.isalpha():
            base = ord('A') if char.isupper() else ord('a')
            shifted = (ord(char) - base + shift) % 26 + base
            result.append(chr(shifted))
        else:
            result.append(char)
    return "".join(result)

def caesar_decrypt(ciphertext, shift):
    """Decrypt by shifting in the opposite direction."""
    return caesar_encrypt(ciphertext, -shift)

def caesar_brute_force(ciphertext):
    """Try all 26 possible shifts to break a Caesar cipher."""
    results = []
    for shift in range(26):
        decrypted = caesar_decrypt(ciphertext, shift)
        results.append((shift, decrypted))
    return results

plaintext = "ATTACK AT DAWN"
shift = 13
encrypted = caesar_encrypt(plaintext, shift)
decrypted = caesar_decrypt(encrypted, shift)
print(f"  Plaintext:  {plaintext}")
print(f"  Shift:      {shift}")
print(f"  Encrypted:  {encrypted}")
print(f"  Decrypted:  {decrypted}")

print(f"\n  Brute force (first 5 shifts):")
for s, text in caesar_brute_force(encrypted)[:5]:
    print(f"    Shift {s:>2}: {text}")


# ── Section 7: XOR Encryption ──────────────────────────────

print("\n--- Section 7: XOR Encryption ---")

def xor_encrypt(plaintext, key):
    """XOR each byte of plaintext with repeating key bytes.
    XOR property: A ^ B ^ B = A (encrypt and decrypt are the same operation)."""
    encrypted = []
    for i, char in enumerate(plaintext):
        key_char = key[i % len(key)]
        encrypted.append(chr(ord(char) ^ ord(key_char)))
    return encrypted

def xor_to_hex(encrypted_chars):
    """Convert XOR result to hex string for display."""
    return " ".join(f"{ord(c):02x}" for c in encrypted_chars)

plaintext = "CONFIDENTIAL DATA"
key = "SECRET"
encrypted = xor_encrypt(plaintext, key)
decrypted = "".join(xor_encrypt(encrypted, key))
print(f"  Plaintext:  {plaintext}")
print(f"  Key:        {key}")
print(f"  Encrypted:  {xor_to_hex(encrypted)}")
print(f"  Decrypted:  {decrypted}")


# ── Section 8: File Integrity Checking ──────────────────────

print("\n--- Section 8: File Integrity ---")

def file_checksum(filepath, algorithm="sha256"):
    """Calculate the hash of a file for integrity verification.
    Used to detect tampering or corruption during transfer."""
    h = hashlib.new(algorithm)
    try:
        with open(filepath, "rb") as f:
            while chunk := f.read(8192):
                h.update(chunk)
        return h.hexdigest()
    except FileNotFoundError:
        return None

# Create a test file and verify its integrity
test_content = "This is a test file for integrity checking.\nLine 2.\nLine 3.\n"
with open("test_integrity.txt", "w") as f:
    f.write(test_content)

original_hash = file_checksum("test_integrity.txt")
print(f"  Original SHA-256: {original_hash}")

# Verify unchanged file
verify_hash = file_checksum("test_integrity.txt")
print(f"  Verify SHA-256:   {verify_hash}")
print(f"  Integrity OK:     {original_hash == verify_hash}")

# Tamper with the file
with open("test_integrity.txt", "a") as f:
    f.write("tampered!")

tampered_hash = file_checksum("test_integrity.txt")
print(f"  Tampered SHA-256: {tampered_hash}")
print(f"  Integrity OK:     {original_hash == tampered_hash}")

# Clean up
os.remove("test_integrity.txt")


# ── Section 9: Secure Random Generation ─────────────────────

print("\n--- Section 9: Secure Random Generation ---")

print(f"  Random token (hex):      {secrets.token_hex(16)}")
print(f"  Random token (urlsafe):  {secrets.token_urlsafe(16)}")
print(f"  Random integer (0-999):  {secrets.randbelow(1000)}")

def generate_password(length=16):
    """Generate a cryptographically secure random password."""
    chars = string.ascii_letters + string.digits + string.punctuation
    while True:
        pw = "".join(secrets.choice(chars) for _ in range(length))
        # Ensure it has at least one of each type
        if (any(c in string.ascii_lowercase for c in pw) and
            any(c in string.ascii_uppercase for c in pw) and
            any(c in string.digits for c in pw) and
            any(c in string.punctuation for c in pw)):
            return pw

print(f"\n  Generated passwords:")
for i in range(3):
    pw = generate_password(20)
    result = analyze_password(pw)
    print(f"    {pw}  [{result['strength']}]")
