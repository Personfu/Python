# ============================================================
# Assignment — Operating System Concepts
# CIS 156 — Computer Science Concepts | FLLC Enterprise
# Author: Preston Furulie
# ============================================================
# CompTIA ITF+ Alignment: Infrastructure domain — understanding
# how operating systems manage hardware resources, processes,
# memory, and file systems.
# ============================================================

"""
Operating System Concepts
=========================
An operating system (OS) is system software that manages hardware
and provides services for application software. Core responsibilities:

  - Process Management   — creating, scheduling, terminating processes
  - Memory Management    — allocating and freeing RAM for programs
  - File System          — organizing data on persistent storage
  - I/O Management       — coordinating device communication
  - Security & Access    — enforcing permissions and user isolation
"""

import os
import time
import threading
from pathlib import Path
from collections import deque


# ────────────────────────────────────────────────────────────
# 1. PROCESS MANAGEMENT SIMULATION
# ────────────────────────────────────────────────────────────
# A process is a running instance of a program. Each process
# has a PID, a state, and resource requirements.

class Process:
    """Simulates a lightweight process with state transitions."""

    STATES = ("NEW", "READY", "RUNNING", "WAITING", "TERMINATED")

    def __init__(self, pid, name, burst_time):
        self.pid = pid
        self.name = name
        self.burst_time = burst_time      # CPU time needed
        self.remaining_time = burst_time
        self.state = "NEW"

    def transition(self, new_state):
        old = self.state
        self.state = new_state
        return f"  PID {self.pid:>3} ({self.name:<12}) : {old} -> {new_state}"

    def __repr__(self):
        return (f"Process(pid={self.pid}, name='{self.name}', "
                f"burst={self.burst_time}, state='{self.state}')")


def process_lifecycle_demo():
    """Show the standard process lifecycle."""
    print(f"\n{'='*60}")
    print("1. PROCESS MANAGEMENT — Lifecycle Simulation")
    print(f"{'='*60}")

    processes = [
        Process(1001, "web_server",  8),
        Process(1002, "db_query",    4),
        Process(1003, "log_writer",  2),
        Process(1004, "backup_job", 10),
    ]

    print("\nProcess Table:")
    print(f"  {'PID':<6} {'Name':<14} {'Burst':<8} {'State'}")
    print(f"  {'-'*6} {'-'*14} {'-'*8} {'-'*12}")
    for p in processes:
        print(f"  {p.pid:<6} {p.name:<14} {p.burst_time:<8} {p.state}")

    print("\nState Transitions:")
    for p in processes:
        print(p.transition("READY"))
    print(processes[0].transition("RUNNING"))
    print(processes[0].transition("WAITING"))
    print(processes[0].transition("READY"))
    print(processes[0].transition("RUNNING"))
    print(processes[0].transition("TERMINATED"))


# ────────────────────────────────────────────────────────────
# 2. CPU SCHEDULING ALGORITHMS
# ────────────────────────────────────────────────────────────
# The scheduler decides which ready process gets the CPU next.

def fcfs_scheduling(processes):
    """First-Come, First-Served — simplest scheduling algorithm."""
    print(f"\n{'='*60}")
    print("2a. SCHEDULING — First-Come, First-Served (FCFS)")
    print(f"{'='*60}")

    current_time = 0
    print(f"\n  {'Process':<14} {'Burst':<8} {'Start':<8} {'Finish':<8} {'Wait'}")
    print(f"  {'-'*14} {'-'*8} {'-'*8} {'-'*8} {'-'*8}")
    total_wait = 0
    for p in processes:
        wait = current_time
        finish = current_time + p.burst_time
        print(f"  {p.name:<14} {p.burst_time:<8} {current_time:<8} {finish:<8} {wait}")
        total_wait += wait
        current_time = finish
    avg_wait = total_wait / len(processes)
    print(f"\n  Average wait time: {avg_wait:.2f} units")


def sjf_scheduling(processes):
    """Shortest Job First — minimizes average wait time."""
    print(f"\n{'='*60}")
    print("2b. SCHEDULING — Shortest Job First (SJF)")
    print(f"{'='*60}")

    sorted_procs = sorted(processes, key=lambda p: p.burst_time)
    current_time = 0
    print(f"\n  {'Process':<14} {'Burst':<8} {'Start':<8} {'Finish':<8} {'Wait'}")
    print(f"  {'-'*14} {'-'*8} {'-'*8} {'-'*8} {'-'*8}")
    total_wait = 0
    for p in sorted_procs:
        wait = current_time
        finish = current_time + p.burst_time
        print(f"  {p.name:<14} {p.burst_time:<8} {current_time:<8} {finish:<8} {wait}")
        total_wait += wait
        current_time = finish
    avg_wait = total_wait / len(sorted_procs)
    print(f"\n  Average wait time: {avg_wait:.2f} units")


def round_robin_scheduling(processes, quantum=3):
    """Round Robin — each process gets a fixed time slice (quantum)."""
    print(f"\n{'='*60}")
    print(f"2c. SCHEDULING — Round Robin (quantum = {quantum})")
    print(f"{'='*60}")

    queue = deque()
    for p in processes:
        p.remaining_time = p.burst_time
        queue.append(p)

    current_time = 0
    execution_log = []

    while queue:
        proc = queue.popleft()
        run_time = min(quantum, proc.remaining_time)
        execution_log.append((proc.name, current_time, current_time + run_time))
        proc.remaining_time -= run_time
        current_time += run_time
        if proc.remaining_time > 0:
            queue.append(proc)

    print(f"\n  {'Process':<14} {'Start':<8} {'End':<8} {'Slice'}")
    print(f"  {'-'*14} {'-'*8} {'-'*8} {'-'*8}")
    for name, start, end in execution_log:
        print(f"  {name:<14} {start:<8} {end:<8} {end - start}")
    print(f"\n  Total time: {current_time} units")


# ────────────────────────────────────────────────────────────
# 3. MEMORY MANAGEMENT SIMULATION
# ────────────────────────────────────────────────────────────
# The OS must allocate RAM to processes and reclaim it when
# they finish. Two common strategies: first-fit and best-fit.

def memory_allocation_demo():
    """Simulate first-fit and best-fit memory allocation."""
    print(f"\n{'='*60}")
    print("3. MEMORY MANAGEMENT — Allocation Strategies")
    print(f"{'='*60}")

    # Memory partitions (size in MB)
    partitions = [100, 500, 200, 300, 600]
    requests = [212, 417, 112, 426]

    def first_fit(parts, reqs):
        alloc = {}
        available = list(parts)
        for req in reqs:
            placed = False
            for i, block in enumerate(available):
                if block >= req:
                    alloc[req] = (i, block)
                    available[i] -= req
                    placed = True
                    break
            if not placed:
                alloc[req] = (None, None)
        return alloc

    def best_fit(parts, reqs):
        alloc = {}
        available = list(parts)
        for req in reqs:
            best_idx = None
            best_size = float("inf")
            for i, block in enumerate(available):
                if block >= req and block < best_size:
                    best_idx = i
                    best_size = block
            if best_idx is not None:
                alloc[req] = (best_idx, best_size)
                available[best_idx] -= req
            else:
                alloc[req] = (None, None)
        return alloc

    print(f"\n  Partitions (MB): {partitions}")
    print(f"  Requests   (MB): {requests}")

    print("\n  --- First-Fit Allocation ---")
    ff = first_fit(partitions, requests)
    for req, (idx, size) in ff.items():
        if idx is not None:
            print(f"    {req} MB -> Partition {idx} ({size} MB)")
        else:
            print(f"    {req} MB -> NOT ALLOCATED")

    print("\n  --- Best-Fit Allocation ---")
    bf = best_fit(partitions, requests)
    for req, (idx, size) in bf.items():
        if idx is not None:
            print(f"    {req} MB -> Partition {idx} ({size} MB)")
        else:
            print(f"    {req} MB -> NOT ALLOCATED")


# ────────────────────────────────────────────────────────────
# 4. FILE SYSTEM OPERATIONS
# ────────────────────────────────────────────────────────────
# The file system organizes data hierarchically. Python's os
# and pathlib modules provide cross-platform file operations.

def file_system_demo():
    """Demonstrate file system information using os and pathlib."""
    print(f"\n{'='*60}")
    print("4. FILE SYSTEM OPERATIONS")
    print(f"{'='*60}")

    cwd = Path.cwd()
    print(f"\n  Current directory : {cwd}")
    print(f"  OS name           : {os.name}")
    print(f"  Path separator    : {os.sep}")

    print("\n  Directory listing (first 10 entries):")
    entries = list(cwd.iterdir())[:10]
    for entry in entries:
        kind = "DIR " if entry.is_dir() else "FILE"
        size = entry.stat().st_size if entry.is_file() else 0
        print(f"    [{kind}] {entry.name:<30} {size:>10,} bytes")

    print("\n  Key pathlib features:")
    sample = Path("/home/fllc/projects/app/main.py")
    print(f"    Path         : {sample}")
    print(f"    Parent       : {sample.parent}")
    print(f"    Stem         : {sample.stem}")
    print(f"    Suffix       : {sample.suffix}")
    print(f"    Parts        : {sample.parts}")


# ────────────────────────────────────────────────────────────
# 5. THREADS vs PROCESSES
# ────────────────────────────────────────────────────────────
# Processes have separate memory spaces; threads share memory
# within a process. Threads are lighter but need synchronization.

def thread_demo():
    """Show basic threading with shared state."""
    print(f"\n{'='*60}")
    print("5. THREADS vs PROCESSES")
    print(f"{'='*60}")

    print("\n  Concept Comparison:")
    print(f"  {'Attribute':<22} {'Process':<22} {'Thread'}")
    print(f"  {'-'*22} {'-'*22} {'-'*22}")
    comparisons = [
        ("Memory space",   "Separate",            "Shared"),
        ("Creation cost",  "High",                "Low"),
        ("Communication",  "IPC (pipes, sockets)","Direct (shared vars)"),
        ("Crash isolation", "Isolated",            "Can crash parent"),
        ("Use case",       "CPU-heavy parallelism","I/O-bound concurrency"),
    ]
    for attr, proc, thrd in comparisons:
        print(f"  {attr:<22} {proc:<22} {thrd}")

    counter = {"value": 0}
    lock = threading.Lock()

    def increment(n, label):
        for _ in range(n):
            with lock:
                counter["value"] += 1
        print(f"    Thread '{label}' finished — counter = {counter['value']}")

    print("\n  Thread demo — 3 threads incrementing a shared counter:")
    threads = []
    for i in range(3):
        t = threading.Thread(target=increment, args=(1000, f"worker-{i}"))
        threads.append(t)
        t.start()
    for t in threads:
        t.join()
    print(f"    Final counter value: {counter['value']} (expected 3000)")


# ────────────────────────────────────────────────────────────
# MAIN — Run all demonstrations
# ────────────────────────────────────────────────────────────

def main():
    print("=" * 60)
    print("  CIS 156 — Operating System Concepts")
    print("  FLLC Enterprise | Preston Furulie | Spring 2026")
    print("=" * 60)

    process_lifecycle_demo()

    procs = [
        Process(1, "web_server",  8),
        Process(2, "db_query",    4),
        Process(3, "log_writer",  2),
        Process(4, "backup_job", 10),
    ]
    fcfs_scheduling(procs)
    sjf_scheduling(procs)
    round_robin_scheduling(procs, quantum=3)

    memory_allocation_demo()
    file_system_demo()
    thread_demo()

    print(f"\n{'='*60}")
    print("  End of Operating System Concepts Module")
    print(f"{'='*60}")


if __name__ == "__main__":
    main()
