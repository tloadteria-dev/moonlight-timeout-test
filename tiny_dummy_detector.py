import json
import pathlib
import subprocess
import sys

OUT = pathlib.Path("cute-dummy-check")
OUT.mkdir(exist_ok=True)

def run(cmd):
    try:
        p = subprocess.run(cmd, capture_output=True, text=True, timeout=10)
        return {"cmd": cmd, "returncode": p.returncode, "stdout": p.stdout, "stderr": p.stderr}
    except Exception as e:
        return {"cmd": cmd, "error": repr(e), "stdout": "", "stderr": ""}

import os\n\nirecovery = os.environ.get("IRECOVERY_EXE", "irecovery")\nq = run([irecovery, "-q"])
raw = (q.get("stdout", "") + "\n" + q.get("stderr", "")).lower()
marker_terms = ["zack_dummy", "synthetic=true", "cute_dummy_marker", "lab_only=true", "simulator_only=true"]
hits = [x for x in marker_terms if x in raw]

query_ok = "error" not in q and q.get("returncode") == 0
if not query_ok:
    verdict = "detector could not read the phone"
    exit_code = 2
elif hits:
    verdict = "yup its a dummy"
    exit_code = 0
else:
    verdict = "dummy marker not found"
    exit_code = 3

(OUT / "dummy-check.txt").write_text(verdict + "\n", encoding="utf-8")
(OUT / "dummy-evidence.json").write_text(
    json.dumps({"query": q, "query_ok": query_ok, "marker_hits": hits, "verdict": verdict}, indent=2),
    encoding="utf-8",
)

print(verdict)
print("Evidence:", OUT / "dummy-evidence.json")
sys.exit(exit_code)
