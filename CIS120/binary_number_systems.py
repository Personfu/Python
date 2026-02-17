# ============================================================
# Binary & Number Systems — Complete Implementation
# CIS 120 — Intro to Computing | Preston Furulie
# ============================================================
# Covers: decimal, binary, octal, hexadecimal conversions,
# bitwise operations, two's complement, ASCII encoding,
# manual base-conversion algorithms, and IEEE 754 basics.
# ============================================================

# ── Section 1: Built-in Base Conversions ────────────────────

def convert_all_bases(decimal_num):
    """Convert a decimal integer to binary, octal, and hexadecimal
    using Python built-ins. Returns formatted strings."""
    return {
        "decimal":     str(decimal_num),
        "binary":      bin(decimal_num),        # prefix 0b
        "octal":       oct(decimal_num),         # prefix 0o
        "hexadecimal": hex(decimal_num),         # prefix 0x
        "binary_clean":  bin(decimal_num)[2:],   # no prefix
        "octal_clean":   oct(decimal_num)[2:],
        "hex_clean":     hex(decimal_num)[2:].upper(),
    }


# ── Section 2: Manual Decimal-to-Binary (Division Method) ──

def decimal_to_binary_manual(n):
    """Convert decimal to binary using repeated division by 2.
    This is the algorithm taught in CIS 120 lectures."""
    if n == 0:
        return "0"
    negative = n < 0
    n = abs(n)
    bits = []
    while n > 0:
        remainder = n % 2        # the current bit (0 or 1)
        bits.append(str(remainder))
        n = n // 2               # integer division, shift right
    bits.reverse()               # LSB was collected first
    result = "".join(bits)
    return ("-" + result) if negative else result


def binary_to_decimal_manual(binary_str):
    """Convert a binary string to decimal using positional notation.
    Each bit's value = bit * 2^position (right to left)."""
    binary_str = binary_str.lstrip("-")
    total = 0
    for i, bit in enumerate(reversed(binary_str)):
        if bit == "1":
            total += 2 ** i      # add 2^position for each '1' bit
    return total


# ── Section 3: Arbitrary Base Conversion ────────────────────

def decimal_to_base(n, base):
    """Convert decimal to any base (2-16) using division-remainder.
    Uses 0-9 and A-F for digits above 9."""
    if base < 2 or base > 16:
        raise ValueError("Base must be between 2 and 16")
    if n == 0:
        return "0"
    digits = "0123456789ABCDEF"
    negative = n < 0
    n = abs(n)
    result = []
    while n > 0:
        result.append(digits[n % base])
        n //= base
    result.reverse()
    return ("-" if negative else "") + "".join(result)


def base_to_decimal(value_str, base):
    """Convert a string in any base (2-16) back to decimal.
    Uses positional multiplication: digit * base^position."""
    digits = "0123456789ABCDEF"
    value_str = value_str.upper().lstrip("-")
    total = 0
    for i, char in enumerate(reversed(value_str)):
        total += digits.index(char) * (base ** i)
    return total


# ── Section 4: Bitwise Operations ───────────────────────────

def demonstrate_bitwise(a, b):
    """Show all six bitwise operations on two integers.
    These operate on the binary representation directly."""
    print(f"\n  Bitwise Operations on {a} ({bin(a)}) and {b} ({bin(b)}):")
    print(f"  {'AND (&)':<12}  {a} & {b}  = {a & b:<6}  ({bin(a & b)})")
    print(f"  {'OR  (|)':<12}  {a} | {b}  = {a | b:<6}  ({bin(a | b)})")
    print(f"  {'XOR (^)':<12}  {a} ^ {b}  = {a ^ b:<6}  ({bin(a ^ b)})")
    print(f"  {'NOT (~)':<12}  ~{a}      = {~a:<6}  ({bin(~a)})")
    print(f"  {'L-Shift':<12}  {a} << 1  = {a << 1:<6}  ({bin(a << 1)})")
    print(f"  {'R-Shift':<12}  {a} >> 1  = {a >> 1:<6}  ({bin(a >> 1)})")


# ── Section 5: Two's Complement (Signed Integers) ──────────

def twos_complement(n, bits=8):
    """Compute the two's complement representation of a signed integer.
    Used in hardware to represent negative numbers.
    Steps: invert all bits, then add 1."""
    if n >= 0:
        binary = bin(n)[2:].zfill(bits)
        return binary
    else:
        positive = bin(abs(n))[2:].zfill(bits)
        # Invert each bit
        inverted = "".join("1" if b == "0" else "0" for b in positive)
        # Add 1 to the inverted value
        result = bin(int(inverted, 2) + 1)[2:].zfill(bits)
        return result


# ── Section 6: ASCII / Character Encoding ───────────────────

def ascii_table(start=32, end=126):
    """Print an ASCII reference table showing decimal, hex, binary,
    and the character for each code point."""
    print(f"\n  {'Dec':<6}{'Hex':<6}{'Binary':<11}{'Char'}")
    print("  " + "-" * 30)
    for code in range(start, end + 1):
        char = chr(code)
        print(f"  {code:<6}{hex(code):<6}{bin(code)[2:].zfill(8):<11}{char}")


def string_to_binary(text):
    """Convert each character of a string to its 8-bit binary
    ASCII representation."""
    return " ".join(format(ord(c), "08b") for c in text)


def binary_to_string(binary_text):
    """Convert space-separated 8-bit binary back to a string."""
    bytes_list = binary_text.split(" ")
    return "".join(chr(int(b, 2)) for b in bytes_list)


# ── Section 7: Data Size Calculations ───────────────────────

def storage_units(bytes_count):
    """Convert a byte count into KB, MB, GB, TB for perspective."""
    units = [
        ("Bytes", 1),
        ("KB",    1024),
        ("MB",    1024 ** 2),
        ("GB",    1024 ** 3),
        ("TB",    1024 ** 4),
    ]
    results = {}
    for name, divisor in units:
        results[name] = bytes_count / divisor
    return results


# ── Main Program: Interactive Demonstrations ────────────────

if __name__ == "__main__":
    print("=" * 60)
    print("  BINARY & NUMBER SYSTEMS — CIS 120")
    print("  Preston Furulie")
    print("=" * 60)

    # --- Demo 1: Full base conversion ---
    number = int(input("\n  Enter a decimal number: "))
    results = convert_all_bases(number)
    print(f"\n  Decimal:     {results['decimal']}")
    print(f"  Binary:      {results['binary_clean']}")
    print(f"  Octal:       {results['octal_clean']}")
    print(f"  Hexadecimal: {results['hex_clean']}")

    # --- Demo 2: Manual conversion verification ---
    manual_bin = decimal_to_binary_manual(number)
    print(f"\n  Manual binary conversion: {manual_bin}")
    print(f"  Back to decimal:          {binary_to_decimal_manual(manual_bin)}")

    # --- Demo 3: Arbitrary base conversion ---
    print(f"\n  {number} in base 3:  {decimal_to_base(number, 3)}")
    print(f"  {number} in base 5:  {decimal_to_base(number, 5)}")
    print(f"  {number} in base 7:  {decimal_to_base(number, 7)}")
    print(f"  {number} in base 12: {decimal_to_base(number, 12)}")

    # --- Demo 4: Bitwise operations ---
    demonstrate_bitwise(12, 10)

    # --- Demo 5: Two's complement ---
    print(f"\n  Two's Complement (8-bit):")
    for val in [42, -42, 1, -1, 127, -128]:
        print(f"    {val:>5} → {twos_complement(val, 8)}")

    # --- Demo 6: ASCII encoding ---
    text = input("\n  Enter text to encode as binary: ")
    encoded = string_to_binary(text)
    print(f"  Binary:  {encoded}")
    print(f"  Decoded: {binary_to_string(encoded)}")

    # --- Demo 7: Storage calculation ---
    file_size = 1_073_741_824  # 1 GB in bytes
    sizes = storage_units(file_size)
    print(f"\n  {file_size:,} bytes =")
    for unit, value in sizes.items():
        print(f"    {value:>15,.2f} {unit}")

    # --- Demo 8: Partial ASCII table (printable range) ---
    show_ascii = input("\n  Show ASCII table? (y/n): ").lower()
    if show_ascii == "y":
        ascii_table(65, 90)  # A-Z
