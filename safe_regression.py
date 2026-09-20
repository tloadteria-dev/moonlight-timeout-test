#!/usr/bin/env python3
import json
from dataclasses import dataclass, asdict

@dataclass
class Result:
    candidate: str
    unsafe_cases: int
    total_cases: int
    fixed_blocks_all_unsafe: bool
    reachability_weight: float
    direct_write_weight: float
    cross_platform_weight: float
    score: float
    notes: str

def le_audio():
    cap=256
    unsafe=0
    total=0
    fixed_ok=True
    for offset in range(0, cap+1, 8):
        for length in range(0, cap*2+1, 8):
            total+=1
            old_allows=True
            violates=(offset+length)>cap
            fixed_allows=(length <= max(0, cap-offset))
            if old_allows and violates:
                unsafe+=1
                if fixed_allows:
                    fixed_ok=False
    score = 0.50*1.0 + 0.25*1.0 + 0.25*0.25
    return Result("LE Audio fragmented-frame reassembly",unsafe,total,fixed_ok,0.25,1.0,1.0,round(score,3),
                  "Direct remaining-capacity guard before modeled copy; BFU/session prerequisites unresolved.")

def avrcp():
    cap=128
    unsafe=0
    total=0
    fixed_ok=True
    for n in range(0,257):
        total+=1
        old_writes=n
        violates=old_writes>cap
        fixed_allows=n<=cap
        if violates:
            unsafe+=1
            if fixed_allows:
                fixed_ok=False
    score = 0.50*0.9 + 0.25*1.0 + 0.25*0.65
    return Result("AVRCP GET_ELEMENT_ATTRIBUTES",unsafe,total,fixed_ok,0.65,0.9,1.0,round(score,3),
                  "Explicit 128-entry bound in fixed model; exact 23G83 inbound AVRCP machinery exists, final policy unresolved.")

def var32():
    unsafe=0
    total=0
    fixed_ok=True
    samples=[0,1,0xffff,0x10000,0x10001,0x12345678,0xffffffff]
    for v in samples:
        total+=1
        old=v & 0xffff
        fixed_reject=v>=0x10000
        diverges=(v>=0x10000 and old != v)
        if diverges:
            unsafe+=1
            if not fixed_reject:
                fixed_ok=False
    score = 0.50*0.45 + 0.25*1.0 + 0.25*0.2
    return Result("OI DataElement VAR32 / SDP",unsafe,total,fixed_ok,0.2,0.45,1.0,round(score,3),
                  "Strong parser divergence but direct write consequence is less immediate; observed path requires SDP client/request state.")

def main():
    results=[le_audio(),avrcp(),var32()]
    results=sorted(results,key=lambda x:x.score,reverse=True)
    out={
        "scope":"synthetic offline regression only; no packet generation or live-device interaction",
        "target_context":"iPhone14,7 / iOS 26.6.1 / 23G83 patch-shape comparison to 23H24",
        "ranking":[asdict(r) for r in results]
    }
    print(json.dumps(out,indent=2))
    with open("simulation-results.json","w",encoding="utf-8") as f:
        json.dump(out,f,indent=2)
if __name__=="__main__":
    main()
