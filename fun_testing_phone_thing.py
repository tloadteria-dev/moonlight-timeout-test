from __future__ import annotations
import argparse, json, hashlib, time
from dataclasses import dataclass, asdict
from enum import Enum

class State(str, Enum):
    BOOTED_BFU="BOOTED_BFU"
    PASSCODE_REQUIRED="PASSCODE_REQUIRED"
    FIRST_UNLOCK="FIRST_UNLOCK"
    FACE_ID_ELIGIBLE="FACE_ID_ELIGIBLE"

@dataclass
class Event:
    ts: float
    before: str
    action: str
    after: str
    mode: str

class Lab:
    def __init__(self, mode: str):
        self.mode=mode
        self.state=State.PASSCODE_REQUIRED
        self.events=[]
    def face_scan_attempt(self):
        before=self.state
        if self.mode=="vulnerable" and self.state==State.PASSCODE_REQUIRED:
            self.state=State.FACE_ID_ELIGIBLE
        self.events.append(Event(time.time(),before.value,"face_scan_attempt",self.state.value,self.mode))
    def report(self):
        payload={"profile":"iPhone14,7 / D27AP / A15 / iOS 26.6.1 / 23G83","synthetic":True,
                 "state":self.state.value,"events":[asdict(e) for e in self.events]}
        raw=json.dumps(payload,sort_keys=True).encode()
        payload["sha256"]=hashlib.sha256(raw).hexdigest()
        return payload

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--mode",choices=["vulnerable","patched"],default="vulnerable")
    ap.add_argument("--out",default="recovery-validation.json")
    a=ap.parse_args()
    lab=Lab(a.mode)
    lab.face_scan_attempt()
    report=lab.report()
    with open(a.out,"w",encoding="utf-8") as f: json.dump(report,f,indent=2)
    print(json.dumps(report,indent=2))
    expected=State.FACE_ID_ELIGIBLE if a.mode=="vulnerable" else State.PASSCODE_REQUIRED
    raise SystemExit(0 if lab.state==expected else 2)

if __name__=="__main__": main()
