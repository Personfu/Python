# Encryption & Hashing Demo
# CIS 350 — Network & Cybersecurity | Preston Furulie

import hashlib
import secrets

# SHA-256 Hashing
password = "MySecurePass123!"
hash_obj = hashlib.sha256(password.encode())
print("SHA-256:", hash_obj.hexdigest())

# Salted hashing (proper password storage)
salt = secrets.token_hex(16)
salted = salt + password
salted_hash = hashlib.sha256(salted.encode()).hexdigest()
print("Salt:", salt)
print("Salted SHA-256:", salted_hash)
print()

# Verify password
def verify(password, salt, expected_hash):
    check = hashlib.sha256((salt + password).encode()).hexdigest()
    return check == expected_hash

print("Verify correct:", verify("MySecurePass123!", salt, salted_hash))
print("Verify wrong:", verify("WrongPassword", salt, salted_hash))
print()

# Compare hash algorithms
for algo in ["md5", "sha1", "sha256", "sha512"]:
    h = hashlib.new(algo, password.encode()).hexdigest()
    print(f"{algo:<8} ({len(h)*4:>3}-bit): {h[:40]}...")
