#!/usr/bin/env python3
import argparse, hashlib, json, os, platform, re, shutil, subprocess, sys
from datetime import datetime, timezone
from pathlib import Path
TARGET={"product_type":"iPhone14,7","board":"d27ap","cpid":"0x8110","bdid":"0x18","ios":"26.6.1","build":"23G83","iboot":"mBoot-18000.162.10"}
def now(): return datetime.now(timezone.utc).isoformat()
def sha256(x): return hashlib.sha256(x).hexdigest()
def find_irecovery():
    for n in (["irecovery.exe","irecovery"] if os.name=="nt" else ["irecovery"]):
        p=shutil.which(n)
        if p:return p
def parse(text):
    out={}
    for line in text.splitlines():
        m=re.match(r"^\s*([^:]+):\s*(.*?)\s*$",line)
        if m: out[m.group(1).strip()]=m.group(2).strip()
    return out
def main():
    ap=argparse.ArgumentParser(); ap.add_argument("--output",default="one-click-results"); a=ap.parse_args()
    out=Path(a.output); out.mkdir(parents=True,exist_ok=True)
    r={"tool":"fun testing phone thing / one-click recovery validation","mode":"READ_ONLY_DEVICE_PLUS_SYNTHETIC","created_utc":now(),"host":{"os":platform.platform(),"python":sys.version.split()[0]},"target_baseline":TARGET}
    b=find_irecovery()
    if not b:
        r["device_status"]="irecovery_not_found"
    else:
        p=subprocess.run([b,"-q"],capture_output=True,text=True,timeout=15,shell=False)
        r["device_status"]="query_complete" if p.returncode == 0 else "query_failed"; r["irecovery_path"]=b; r["returncode"]=p.returncode
        r["stdout"]=p.stdout or ""; r["stderr"]=p.stderr or ""; r["parsed"]=parse(r["stdout"])
        observed=r["parsed"]
        checks={}
        aliases={"product_type":["PRODUCT","ProductType"],"board":["MODEL","BoardConfig","BOARD"],"cpid":["CPID"],"bdid":["BDID"]}
        for key,names in aliases.items():
            value=next((observed[n] for n in names if n in observed),None)
            checks[key]={"expected":TARGET[key],"observed":value,"match":None if value is None else TARGET[key].lower() in value.lower()}
        r["identity_checks"]=checks
        r["identity_mismatch"]=any(v["match"] is False for v in checks.values())
    path=out/"device_report.json"; path.write_text(json.dumps(r,indent=2,sort_keys=True)+"\n",encoding="utf-8")
    (out/"SHA256SUMS.txt").write_text(f"{sha256(path.read_bytes())}  device_report.json\n",encoding="utf-8")
    print(path)
    print("READ_ONLY DEVICE STAGE COMPLETE. No device mutation commands exist in this build.")
    if r.get("device_status") != "query_complete" or r.get("identity_mismatch"):
        raise SystemExit(2)
if __name__=="__main__": main()
