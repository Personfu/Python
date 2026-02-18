"""
===============================================================================
FLLC Enterprise — Platform Engineering Division
===============================================================================
Program:        automation_scripting.py
Author:         Preston Furulie
Organization:   FLLC Enterprise
Course:         CIS 411 — Advanced Systems Administration
Institution:    Portland Community College
Term:           Spring 2026
Alignment:      CompTIA Server+ / Cloud+
Description:    Systems administration automation toolkit demonstrating
                practical Python scripting for server management tasks
                including monitoring, backups, log parsing, and reporting.
===============================================================================
"""

import os
import sys
import platform
import socket
import shutil
import datetime
import csv
import json
import hashlib
import time
import logging
from pathlib import Path
from collections import Counter

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------

FLLC_ORG = "FLLC Enterprise"
FLLC_DEPT = "Platform Engineering"
AUTHOR = "Preston Furulie"

LOG_FORMAT = "%(asctime)s [%(levelname)s] %(message)s"
logging.basicConfig(level=logging.INFO, format=LOG_FORMAT)
logger = logging.getLogger("fllc_automation")

REPORT_DIR = Path("reports")
BACKUP_DIR = Path("backups")


# ===========================================================================
# 1. System Information Gathering
# ===========================================================================

def gather_system_info() -> dict:
    """Collect comprehensive system information using platform, os, and socket modules."""
    info = {
        "hostname": socket.gethostname(),
        "fqdn": socket.getfqdn(),
        "ip_address": _get_primary_ip(),
        "os_system": platform.system(),
        "os_release": platform.release(),
        "os_version": platform.version(),
        "architecture": platform.machine(),
        "processor": platform.processor(),
        "python_version": platform.python_version(),
        "cpu_count_logical": os.cpu_count(),
        "current_user": os.getlogin() if hasattr(os, "getlogin") else "unknown",
        "collection_time": datetime.datetime.now().isoformat(),
        "organization": FLLC_ORG,
    }
    return info


def _get_primary_ip() -> str:
    """Determine the primary IP address by connecting to an external target."""
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
            s.connect(("8.8.8.8", 80))
            return s.getsockname()[0]
    except OSError:
        return "127.0.0.1"


def display_system_info():
    """Pretty-print system information to the console."""
    info = gather_system_info()
    width = 60
    print("=" * width)
    print(f"{'FLLC Enterprise — System Information Report':^{width}}")
    print("=" * width)
    for key, value in info.items():
        label = key.replace("_", " ").title()
        print(f"  {label:<28} {value}")
    print("=" * width)
    return info


# ===========================================================================
# 2. Disk Usage Monitoring
# ===========================================================================

def check_disk_usage(warning_pct: float = 80.0, critical_pct: float = 90.0) -> list[dict]:
    """Monitor disk usage across all mounted partitions.

    Args:
        warning_pct: Percentage threshold for warning alerts.
        critical_pct: Percentage threshold for critical alerts.

    Returns:
        List of partition info dictionaries with alert status.
    """
    results = []

    if platform.system() == "Windows":
        drives = _get_windows_drives()
    else:
        drives = ["/"]

    for drive in drives:
        try:
            usage = shutil.disk_usage(drive)
            total_gb = usage.total / (1024 ** 3)
            used_gb = usage.used / (1024 ** 3)
            free_gb = usage.free / (1024 ** 3)
            pct_used = (usage.used / usage.total) * 100

            if pct_used >= critical_pct:
                status = "CRITICAL"
            elif pct_used >= warning_pct:
                status = "WARNING"
            else:
                status = "OK"

            entry = {
                "drive": drive,
                "total_gb": round(total_gb, 2),
                "used_gb": round(used_gb, 2),
                "free_gb": round(free_gb, 2),
                "percent_used": round(pct_used, 2),
                "status": status,
            }
            results.append(entry)

            log_fn = logger.critical if status == "CRITICAL" else (
                logger.warning if status == "WARNING" else logger.info
            )
            log_fn(f"Disk {drive}: {pct_used:.1f}% used ({free_gb:.1f} GB free) [{status}]")

        except PermissionError:
            logger.warning(f"Permission denied accessing {drive}")

    return results


def _get_windows_drives() -> list[str]:
    """Enumerate available Windows drive letters."""
    drives = []
    for letter in "ABCDEFGHIJKLMNOPQRSTUVWXYZ":
        drive = f"{letter}:\\"
        if os.path.exists(drive):
            drives.append(drive)
    return drives


# ===========================================================================
# 3. Log File Parsing and Alerting
# ===========================================================================

ALERT_KEYWORDS = ["ERROR", "CRITICAL", "FATAL", "FAILURE", "EXCEPTION"]
WARNING_KEYWORDS = ["WARNING", "WARN", "TIMEOUT", "RETRY"]


def parse_log_file(log_path: str, max_lines: int = 10000) -> dict:
    """Parse a log file and extract alert-worthy entries.

    Args:
        log_path: Path to the log file to analyze.
        max_lines: Maximum number of lines to process.

    Returns:
        Dictionary with parsed results and statistics.
    """
    path = Path(log_path)
    if not path.exists():
        logger.error(f"Log file not found: {log_path}")
        return {"error": f"File not found: {log_path}"}

    alerts = []
    warnings = []
    line_count = 0
    keyword_counts = Counter()

    with open(path, "r", encoding="utf-8", errors="replace") as f:
        for line_num, line in enumerate(f, start=1):
            if line_num > max_lines:
                break
            line_count += 1
            upper_line = line.upper()

            for kw in ALERT_KEYWORDS:
                if kw in upper_line:
                    alerts.append({"line": line_num, "keyword": kw, "text": line.strip()})
                    keyword_counts[kw] += 1
                    break

            for kw in WARNING_KEYWORDS:
                if kw in upper_line:
                    warnings.append({"line": line_num, "keyword": kw, "text": line.strip()})
                    keyword_counts[kw] += 1
                    break

    result = {
        "file": str(path),
        "lines_processed": line_count,
        "total_alerts": len(alerts),
        "total_warnings": len(warnings),
        "keyword_counts": dict(keyword_counts),
        "alerts": alerts[:50],
        "warnings": warnings[:50],
    }

    logger.info(
        f"Log analysis complete: {log_path} — "
        f"{len(alerts)} alerts, {len(warnings)} warnings in {line_count} lines"
    )
    return result


def generate_log_alert_summary(parse_result: dict) -> str:
    """Format log parse results into a human-readable alert summary."""
    lines = [
        f"{'=' * 60}",
        f"{'FLLC Enterprise — Log Alert Summary':^60}",
        f"{'=' * 60}",
        f"  File:              {parse_result.get('file', 'N/A')}",
        f"  Lines Processed:   {parse_result.get('lines_processed', 0)}",
        f"  Total Alerts:      {parse_result.get('total_alerts', 0)}",
        f"  Total Warnings:    {parse_result.get('total_warnings', 0)}",
        "",
        "  Keyword Breakdown:",
    ]
    for kw, count in parse_result.get("keyword_counts", {}).items():
        lines.append(f"    {kw:<20} {count}")

    if parse_result.get("alerts"):
        lines.append("")
        lines.append("  Recent Alerts (up to 10):")
        for alert in parse_result["alerts"][:10]:
            lines.append(f"    Line {alert['line']}: {alert['text'][:80]}")

    lines.append("=" * 60)
    return "\n".join(lines)


# ===========================================================================
# 4. Automated Backup Script Simulation
# ===========================================================================

def simulate_backup(source_dir: str, backup_name: str = None) -> dict:
    """Simulate a backup operation for a source directory.

    This function demonstrates backup automation concepts without performing
    actual file copies (to keep the demo safe and fast). In production,
    replace the simulation logic with real copy/archive operations.

    Args:
        source_dir: Directory to back up.
        backup_name: Optional custom name for the backup.

    Returns:
        Backup metadata dictionary.
    """
    source = Path(source_dir)
    if not source.exists():
        logger.error(f"Source directory not found: {source_dir}")
        return {"error": f"Source not found: {source_dir}"}

    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    if backup_name is None:
        backup_name = f"backup_{source.name}_{timestamp}"

    file_count = 0
    total_size = 0
    file_manifest = []

    for item in source.rglob("*"):
        if item.is_file():
            file_count += 1
            size = item.stat().st_size
            total_size += size
            file_manifest.append({
                "path": str(item.relative_to(source)),
                "size_bytes": size,
                "modified": datetime.datetime.fromtimestamp(
                    item.stat().st_mtime
                ).isoformat(),
            })

    checksum = hashlib.sha256(
        json.dumps(file_manifest, sort_keys=True).encode()
    ).hexdigest()[:16]

    backup_meta = {
        "backup_name": backup_name,
        "source_directory": str(source),
        "timestamp": timestamp,
        "file_count": file_count,
        "total_size_bytes": total_size,
        "total_size_mb": round(total_size / (1024 ** 2), 2),
        "manifest_checksum": checksum,
        "status": "SIMULATED_SUCCESS",
        "backup_type": "full",
        "organization": FLLC_ORG,
    }

    REPORT_DIR.mkdir(exist_ok=True)
    manifest_path = REPORT_DIR / f"{backup_name}_manifest.json"
    with open(manifest_path, "w", encoding="utf-8") as f:
        json.dump(backup_meta, f, indent=2)

    logger.info(
        f"Backup simulated: {file_count} files, "
        f"{backup_meta['total_size_mb']} MB — manifest saved to {manifest_path}"
    )
    return backup_meta


# ===========================================================================
# 5. Service Health Checking (HTTP Endpoint Monitoring)
# ===========================================================================

def check_service_health(endpoints: list[dict]) -> list[dict]:
    """Check health of HTTP/HTTPS endpoints.

    Each endpoint dict should have: {"name": str, "url": str, "timeout": int}

    Args:
        endpoints: List of endpoint configurations to check.

    Returns:
        List of health check results.
    """
    try:
        from urllib.request import urlopen, Request
        from urllib.error import URLError, HTTPError
    except ImportError:
        logger.error("urllib not available")
        return []

    results = []
    for ep in endpoints:
        name = ep.get("name", "Unknown")
        url = ep.get("url", "")
        timeout = ep.get("timeout", 10)

        start = time.time()
        try:
            req = Request(url, method="GET")
            req.add_header("User-Agent", f"FLLC-HealthCheck/1.0 ({FLLC_ORG})")
            with urlopen(req, timeout=timeout) as resp:
                status_code = resp.getcode()
                elapsed_ms = round((time.time() - start) * 1000, 2)
                health = "HEALTHY" if 200 <= status_code < 400 else "DEGRADED"

        except HTTPError as e:
            status_code = e.code
            elapsed_ms = round((time.time() - start) * 1000, 2)
            health = "UNHEALTHY"

        except (URLError, OSError) as e:
            status_code = 0
            elapsed_ms = round((time.time() - start) * 1000, 2)
            health = "DOWN"

        result = {
            "name": name,
            "url": url,
            "status_code": status_code,
            "response_time_ms": elapsed_ms,
            "health": health,
            "checked_at": datetime.datetime.now().isoformat(),
        }
        results.append(result)

        log_fn = logger.info if health == "HEALTHY" else logger.warning
        log_fn(f"Health check [{name}]: {health} (HTTP {status_code}, {elapsed_ms}ms)")

    return results


# ===========================================================================
# 6. CSV Report Generation
# ===========================================================================

def generate_csv_report(data: list[dict], report_name: str, fields: list[str] = None) -> str:
    """Generate a CSV report from a list of dictionaries.

    Args:
        data: List of dictionaries containing report data.
        report_name: Name for the report file (without extension).
        fields: Optional list of field names to include. If None, uses all keys.

    Returns:
        Path to the generated CSV file.
    """
    if not data:
        logger.warning("No data provided for report generation")
        return ""

    REPORT_DIR.mkdir(exist_ok=True)
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{report_name}_{timestamp}.csv"
    filepath = REPORT_DIR / filename

    if fields is None:
        fields = list(data[0].keys())

    with open(filepath, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fields, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(data)

    logger.info(f"CSV report generated: {filepath} ({len(data)} rows)")
    return str(filepath)


def generate_system_report() -> str:
    """Generate a comprehensive system health report combining all checks."""
    report_lines = [
        "=" * 70,
        f"{'FLLC Enterprise — Comprehensive System Health Report':^70}",
        "=" * 70,
        f"  Generated:      {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
        f"  Author:         {AUTHOR}",
        f"  Organization:   {FLLC_ORG}",
        f"  Department:     {FLLC_DEPT}",
        "",
        "-" * 70,
        "  SECTION 1: System Information",
        "-" * 70,
    ]

    sys_info = gather_system_info()
    for key, value in sys_info.items():
        label = key.replace("_", " ").title()
        report_lines.append(f"    {label:<30} {value}")

    report_lines.extend([
        "",
        "-" * 70,
        "  SECTION 2: Disk Usage",
        "-" * 70,
    ])

    disk_results = check_disk_usage()
    for d in disk_results:
        report_lines.append(
            f"    {d['drive']:<10} {d['percent_used']:>6.1f}% used "
            f"({d['free_gb']:.1f} GB free) [{d['status']}]"
        )

    report_lines.extend([
        "",
        "-" * 70,
        "  SECTION 3: Service Health Checks",
        "-" * 70,
    ])

    default_endpoints = [
        {"name": "Google DNS", "url": "https://dns.google", "timeout": 5},
        {"name": "GitHub", "url": "https://github.com", "timeout": 5},
        {"name": "PCC Website", "url": "https://www.pcc.edu", "timeout": 5},
    ]

    health_results = check_service_health(default_endpoints)
    for h in health_results:
        report_lines.append(
            f"    {h['name']:<20} {h['health']:<12} "
            f"HTTP {h['status_code']}  {h['response_time_ms']}ms"
        )

    report_lines.extend([
        "",
        "=" * 70,
        f"{'End of Report':^70}",
        "=" * 70,
    ])

    report_text = "\n".join(report_lines)

    REPORT_DIR.mkdir(exist_ok=True)
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    report_path = REPORT_DIR / f"system_health_{timestamp}.txt"
    with open(report_path, "w", encoding="utf-8") as f:
        f.write(report_text)

    if disk_results:
        generate_csv_report(disk_results, "disk_usage", [
            "drive", "total_gb", "used_gb", "free_gb", "percent_used", "status"
        ])

    if health_results:
        generate_csv_report(health_results, "service_health", [
            "name", "url", "status_code", "response_time_ms", "health", "checked_at"
        ])

    logger.info(f"Full system report saved to {report_path}")
    return report_text


# ===========================================================================
# 7. Scheduled Task Concepts
# ===========================================================================

TASK_SCHEDULE = [
    {"task": "System Health Check", "frequency": "Every 5 minutes", "module": "generate_system_report"},
    {"task": "Disk Usage Alert", "frequency": "Every 15 minutes", "module": "check_disk_usage"},
    {"task": "Log File Analysis", "frequency": "Every hour", "module": "parse_log_file"},
    {"task": "Backup Verification", "frequency": "Daily at 02:00", "module": "simulate_backup"},
    {"task": "CSV Report Generation", "frequency": "Daily at 06:00", "module": "generate_csv_report"},
    {"task": "Service Health Check", "frequency": "Every 5 minutes", "module": "check_service_health"},
]


def display_task_schedule():
    """Display the recommended task schedule for FLLC Enterprise monitoring."""
    print("=" * 70)
    print(f"{'FLLC Enterprise — Recommended Task Schedule':^70}")
    print("=" * 70)
    print(f"  {'Task':<30} {'Frequency':<25} {'Module':<25}")
    print(f"  {'-'*30} {'-'*25} {'-'*25}")
    for task in TASK_SCHEDULE:
        print(f"  {task['task']:<30} {task['frequency']:<25} {task['module']:<25}")
    print("=" * 70)
    print()
    print("  Implementation Options:")
    print("    - Windows: Task Scheduler (schtasks.exe or GUI)")
    print("    - Linux:   cron (crontab -e)")
    print("    - Python:  schedule library or APScheduler")
    print("    - Cloud:   AWS EventBridge, Azure Logic Apps, GCP Cloud Scheduler")
    print()


# ===========================================================================
# Main Entry Point
# ===========================================================================

def main():
    """Run all automation demonstrations."""
    print()
    print("=" * 70)
    print(f"{'FLLC Enterprise — Systems Administration Automation Toolkit':^70}")
    print(f"{'CIS 411 | Portland Community College | Spring 2026':^70}")
    print(f"{'Author: Preston Furulie':^70}")
    print("=" * 70)
    print()

    print("[1/4] Gathering system information...")
    display_system_info()
    print()

    print("[2/4] Checking disk usage...")
    disk_data = check_disk_usage()
    print()

    print("[3/4] Displaying recommended task schedule...")
    display_task_schedule()

    print("[4/4] Generating comprehensive system report...")
    report = generate_system_report()
    print(report)
    print()

    print("All automation tasks completed successfully.")
    print(f"Reports saved to: {REPORT_DIR.resolve()}")


if __name__ == "__main__":
    main()
