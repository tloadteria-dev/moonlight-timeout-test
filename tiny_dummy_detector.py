import json, pathlib, subprocess, sys
OUT=pathlib.Path("cute-dummy-check")
OUT.mkdir(exist_ok=True)
def run(cmd):
    try:
        p=subprocess.run(cmd,capture_output=True,text=True,timeout=10)
        return {"cmd":cmd,"returncode":p.returncode,"stdout":p.stdout,"stderr":p.stderr}
    except Exception as e:
        return {"cmd":cmd,"error":repr(e),"stdout":"","stderr":""}
# Read-only device query only.
q=run(["irecovery","-q"])
raw=(q.get("stdout","")+"\n"+q.get("stderr","")).lower()
# Fail closed: ordinary Apple identity fields are NOT dummy proof.
marker_terms=["zack_dummy","synthetic=true","cute_dummy_marker","lab_only=true","simulator_only=true"]
hits=[x for x in marker_terms if x in raw]
verdict="yup its a dummy" if hits else "not a dummy"
(OUT/"dummy-check.txt").write_text(verdict+"\n",encoding="utf-8")
(OUT/"dummy-evidence.json").write_text(json.dumps({"query":q,"marker_hits":hits,"verdict":verdict},indent=2),encoding="utf-8")
print(verdict)
print("Evidence:",OUT/"dummy-evidence.json")
