from __future__ import annotations
import argparse, hashlib, json, time
from dataclasses import dataclass, asdict
from enum import Enum

class State(str, Enum):
    BOOTED_BFU="BOOTED_BFU"
    PASSCODE_REQUIRED="PASSCODE_REQUIRED"
    UNLOCKED="UNLOCKED"

@dataclass
class Event:
    ts: float
    before: str
    action: str
    after: str
    mode: str

class CutePhoneLab:
    def __init__(self, mode: str):
        self.mode=mode
        self.state=State.PASSCODE_REQUIRED
        self.passcode_enabled=True
        self.synthetic_user_data={"photos":3,"notes":2,"messages":5}
        self.events=[]
    def simulated_passcode_removal(self):
        before=self.state
        if self.mode=="vulnerable" and self.state==State.PASSCODE_REQUIRED:
            self.passcode_enabled=False
            self.state=State.UNLOCKED
        self.events.append(Event(time.time(),before.value,"simulated_passcode_removal",self.state.value,self.mode))
    def report(self):
        accessible=self.synthetic_user_data if self.state==State.UNLOCKED else None
        payload={"project":"cute phone thingy test","profile":"iPhone14,7 / D27AP / A15 / iOS 26.6.1 / 23G83",
                 "synthetic":True,"mode":self.mode,"state":self.state.value,"passcode_enabled":self.passcode_enabled,
                 "synthetic_user_data_accessible":accessible,"events":[asdict(e) for e in self.events]}
        raw=json.dumps(payload,sort_keys=True).encode()
        payload["sha256"]=hashlib.sha256(raw).hexdigest()
        return payload

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--mode",choices=["vulnerable","patched"],default="vulnerable")
    ap.add_argument("--out",default="cute-phone-result.json")
    a=ap.parse_args()
    lab=CutePhoneLab(a.mode)
    lab.simulated_passcode_removal()
    report=lab.report()
    with open(a.out,"w",encoding="utf-8") as f: json.dump(report,f,indent=2)
    print(json.dumps(report,indent=2))
    expected=State.UNLOCKED if a.mode=="vulnerable" else State.PASSCODE_REQUIRED
    raise SystemExit(0 if lab.state==expected else 2)

if __name__=="__main__": main()
