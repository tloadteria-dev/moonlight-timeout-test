import argparse
import json
from dataclasses import dataclass, asdict
from pathlib import Path

@dataclass
class AuthState:
    mode: str = "BFU"
    passcode_required: bool = True
    face_id_available: bool = False
    unlocked: bool = False

def run(profile: str):
    s = AuthState()
    before = asdict(s)
    if profile == "vulnerable":
        s.passcode_required = False
        s.face_id_available = True
        s.unlocked = True
    elif profile == "patched":
        pass
    else:
        raise ValueError("profile must be vulnerable or patched")
    return {
        "lab": "Snuggle Unlock Lab :3",
        "synthetic_only": True,
        "profile": profile,
        "before": before,
        "after": asdict(s),
        "result": "SIMULATED_UNLOCK" if s.unlocked else "AUTH_RETAINED",
    }

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--profile", choices=["vulnerable", "patched"], required=True)
    ap.add_argument("--out", default="snuggle-lab-results")
    args = ap.parse_args()
    out = Path(args.out)
    out.mkdir(parents=True, exist_ok=True)
    report = run(args.profile)
    target = out / f"snuggle-{args.profile}.json"
    target.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(report, indent=2))

if __name__ == "__main__":
    main()
