#!/usr/bin/env python3
import argparse, hashlib, json, os, platform, re, shutil, subprocess, sys
from datetime import datetime, timezone
from pathlib import Path

TARGET = {
    "product_type": "iPhone14,7",
    "board": "d27ap",
    "cpid": "0x8110",
    "bdid": "0x18",
    "ios": "26.6.1",
    "build": "23G83",
    "iboot": "mBoot-18000.162.10",
}
SAFE_COMMANDS = [["irecovery", "-q"]]

def now():
    return datetime.now(timezone.utc).isoformat()

def sha256(data: bytes):
    return hashlib.sha256(data).hexdigest()

def find_irecovery():
    candidates = ["irecovery.exe", "irecovery"] if os.name == "nt" else ["irecovery"]
    for name in candidates:
        p = shutil.which(name)
        if p:
            return p
    return None

def run_query(binary):
    cmd = [binary, "-q"]
    started = now()
    proc = subprocess.run(cmd, capture_output=True, text=True, timeout=15, shell=False)
    stdout = proc.stdout or ""
    stderr = proc.stderr or ""
    return {
        "command": [Path(binary).name, "-q"],
        "started_utc": started,
        "finished_utc": now(),
        "returncode": proc.returncode,
        "stdout": stdout,
        "stderr": stderr,
        "stdout_sha256": sha256(stdout.encode("utf-8", "replace")),
        "stderr_sha256": sha256(stderr.encode("utf-8", "replace")),
    }

def parse_query(text):
    out = {}
    for line in text.splitlines():
        m = re.match(r"^\s*([^:]+):\s*(.*?)\s*$", line)
        if m:
            out[m.group(1).strip()] = m.group(2).strip()
    return out

def compare(parsed):
    aliases = {
        "product_type": ["PRODUCT", "ProductType", "MODEL"],
        "board": ["MODEL", "BoardConfig", "BOARD"],
        "cpid": ["CPID"],
        "bdid": ["BDID"],
        "iboot": ["IBOOT", "iBoot"],
    }
    report = {}
    for key, names in aliases.items():
        seen = next((parsed[n] for n in names if n in parsed), None)
        expected = TARGET[key]
        report[key] = {"expected": expected, "observed": seen,
                       "status": "unknown" if seen is None else ("match" if expected.lower() in seen.lower() else "different")}
    return report

def main():
    ap = argparse.ArgumentParser(description="Read-only Apple Recovery Mode evidence collector")
    ap.add_argument("--output", default="recovery-inspector-output")
    args = ap.parse_args()
    outdir = Path(args.output)
    outdir.mkdir(parents=True, exist_ok=True)

    binary = find_irecovery()
    report = {
        "tool": "Recovery Inspector v1",
        "mode": "READ_ONLY",
        "created_utc": now(),
        "host": {"os": platform.platform(), "python": sys.version.split()[0]},
        "target_baseline": TARGET,
        "safety": {
            "allowed": ["irecovery -q"],
            "blocked": ["restore", "erase", "update", "reboot", "shell", "arbitrary iBoot commands", "USB writes", "exploit delivery", "Bluetooth pairing/session forcing"],
        },
    }

    if not binary:
        report["status"] = "irecovery_not_found"
        report["next_action"] = "Install/build official libimobiledevice/libirecovery, then rerun. This program will only invoke irecovery -q."
    else:
        q = run_query(binary)
        parsed = parse_query(q["stdout"])
        report["status"] = "query_complete"
        report["irecovery_path"] = binary
        report["query"] = q
        report["parsed"] = parsed
        report["baseline_comparison"] = compare(parsed)

    raw = json.dumps(report, indent=2, sort_keys=True).encode()
    report["report_sha256_before_self_hash"] = sha256(raw)
    final = json.dumps(report, indent=2, sort_keys=True) + "\n"
    path = outdir / "recovery_report.json"
    path.write_text(final, encoding="utf-8")
    digest = sha256(path.read_bytes())
    (outdir / "SHA256SUMS.txt").write_text(f"{digest}  recovery_report.json\n", encoding="utf-8")
    print(path)
    print("READ_ONLY: only 'irecovery -q' is permitted by this build.")

if __name__ == "__main__":
    main()
