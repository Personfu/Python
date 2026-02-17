# Hardware & Software Fundamentals
## CIS 120 — Intro to Computing | Preston Furulie

---

## 1. Computer Architecture Overview

Modern computers follow the **Von Neumann architecture** (1945), where both programs and data share the same memory space. This model consists of five core subsystems:

### Central Processing Unit (CPU)

The CPU is the "brain" of the computer, containing:

- **ALU (Arithmetic Logic Unit)** — performs mathematical operations (addition, subtraction, multiplication) and logical comparisons (AND, OR, NOT, XOR)
- **Control Unit (CU)** — fetches instructions from memory, decodes them, and coordinates execution across all components
- **Registers** — ultra-fast, small storage locations inside the CPU (e.g., program counter, instruction register, accumulator)
- **Cache (L1/L2/L3)** — high-speed memory built into or near the CPU to reduce main memory access latency

**Instruction Cycle (Fetch-Decode-Execute):**
1. **Fetch** — CU retrieves the next instruction from RAM using the program counter
2. **Decode** — CU interprets the instruction's opcode and operands
3. **Execute** — ALU performs the operation or data is moved between registers/memory
4. **Store** — results written back to a register or memory address

### Memory Hierarchy

| Level    | Type          | Speed       | Size      | Volatility |
|----------|---------------|-------------|-----------|------------|
| L1 Cache | SRAM          | ~1 ns       | 32-64 KB  | Volatile   |
| L2 Cache | SRAM          | ~4 ns       | 256 KB-1 MB | Volatile |
| L3 Cache | SRAM          | ~10 ns      | 4-64 MB   | Volatile   |
| RAM      | DRAM (DDR5)   | ~50-100 ns  | 8-128 GB  | Volatile   |
| SSD      | NAND Flash    | ~0.1 ms     | 256 GB-8 TB | Non-volatile |
| HDD      | Magnetic Disk | ~5-10 ms    | 1-20 TB   | Non-volatile |
| Tape     | Magnetic Tape | Seconds     | Petabytes | Non-volatile |

### Bus Architecture

- **Data Bus** — carries data between CPU, memory, and I/O devices (width determines throughput: 32-bit, 64-bit)
- **Address Bus** — carries memory addresses (width determines addressable memory: 32-bit = 4 GB, 64-bit = 16 EB)
- **Control Bus** — carries control signals (read/write, interrupt, clock)

---

## 2. Software Layers

Software is organized in layers from low-level (closest to hardware) to high-level (closest to the user):

### Layer 1: Firmware / BIOS / UEFI
- Stored in ROM/flash memory on the motherboard
- POST (Power-On Self-Test) — verifies hardware is functional
- Initializes hardware and hands control to the bootloader
- UEFI is the modern replacement for legacy BIOS (supports GPT, Secure Boot, GUI)

### Layer 2: Operating System
- **Kernel** — core of the OS, manages CPU scheduling, memory allocation, device drivers, and system calls
- **Process Management** — handles multitasking, threading, inter-process communication
- **Memory Management** — virtual memory, paging, segmentation (each process gets its own address space)
- **File System** — organizes data on storage (NTFS, ext4, APFS, FAT32)
- **I/O Management** — abstracts hardware access through device drivers
- Examples: Windows 11, Ubuntu Linux, macOS Sonoma

### Layer 3: System Utilities
- Command-line tools (CMD, PowerShell, Bash)
- Disk management, task managers, network configuration
- Package managers (apt, pip, npm, choco)

### Layer 4: Application Software
- User-facing programs: browsers, IDEs, office suites, games
- Built on top of OS APIs and libraries
- May be native (compiled for specific OS) or cross-platform (Java, Electron, web apps)

---

## 3. Data Representation

### Bit, Byte, Word
- **Bit** — smallest unit: 0 or 1
- **Nibble** — 4 bits (one hexadecimal digit, values 0-15)
- **Byte** — 8 bits (values 0-255, represents one ASCII character)
- **Word** — CPU-native size (32-bit or 64-bit on modern systems)

### Number Systems
- **Binary (base-2)** — 0, 1 — used internally by all digital hardware
- **Octal (base-8)** — 0-7 — historic use in Unix file permissions (e.g., chmod 755)
- **Decimal (base-10)** — 0-9 — human-readable default
- **Hexadecimal (base-16)** — 0-F — compact binary representation (1 hex digit = 4 bits)

### Character Encoding
- **ASCII** — 7-bit encoding for 128 characters (English letters, digits, punctuation)
- **Extended ASCII** — 8-bit, adds 128 more characters (accents, symbols)
- **Unicode (UTF-8)** — variable-length encoding supporting 150,000+ characters from all writing systems; backward-compatible with ASCII

---

## 4. Logic Gates and Boolean Algebra

| Gate | Symbol | Truth Table (A=1, B=1) | Expression |
|------|--------|------------------------|------------|
| AND  | A · B  | 1                      | A AND B    |
| OR   | A + B  | 1                      | A OR B     |
| NOT  | ¬A     | 0                      | NOT A      |
| NAND | ¬(A·B) | 0                      | NOT (A AND B) |
| XOR  | A ⊕ B  | 0                      | A OR B but NOT both |

**De Morgan's Laws:**
- NOT (A AND B) = (NOT A) OR (NOT B)
- NOT (A OR B) = (NOT A) AND (NOT B)

These gates are physically implemented using transistors on silicon chips and form the foundation of all digital computation.

---

## 5. Key Performance Metrics

| Metric | Definition | Typical Values |
|--------|-----------|----------------|
| Clock Speed | CPU cycles per second | 3.0-5.8 GHz |
| IPC | Instructions per clock cycle | 4-8 (modern CPUs) |
| Core Count | Independent processing units | 4-24 (consumer), 64-128 (server) |
| RAM Bandwidth | Data transfer rate | DDR5: 38-51 GB/s |
| Storage IOPS | I/O operations per second | SSD: 100K-1M, HDD: 75-200 |
| Network | Data transfer rate | Gigabit (1 Gbps), Wi-Fi 6 (9.6 Gbps theoretical) |

---

## 6. Emerging Technologies

- **Quantum Computing** — uses qubits (superposition of 0 and 1) for exponential parallelism on specific problems (cryptography, optimization)
- **Neuromorphic Chips** — mimic biological neural networks for AI workloads (Intel Loihi, IBM TrueNorth)
- **ARM Architecture** — energy-efficient RISC processors now powering laptops (Apple M-series) and cloud servers (AWS Graviton)
- **Persistent Memory (PMEM)** — Intel Optane bridges gap between DRAM speed and SSD persistence
