# Recovery Inspector v1

Read-only Recovery Mode evidence collector for the current iPhone 14 recovery project.

## Safety invariant

This branch invokes exactly one device-facing operation:

`irecovery -q`

It contains no restore, erase, update, reboot, arbitrary iBoot command, USB write, exploit delivery, Bluetooth pairing, forced session, malformed packet, or passcode functionality.

## Foundation

Uses the command-line interface from the official libimobiledevice/libirecovery project:
https://github.com/libimobiledevice/libirecovery

## Run

Install/build `irecovery` from the official project so it is on PATH, connect the iPhone while it is already in Recovery Mode, then:

```
python recovery_inspector.py
```

Outputs:
- `recovery-inspector-output/recovery_report.json`
- `recovery-inspector-output/SHA256SUMS.txt`

The report records the raw read-only query, hashes, parsed fields, and comparison against the known iPhone14,7 / 23G83 project baseline.

## Target baseline

- ProductType: iPhone14,7
- Board: d27ap
- CPID: 0x8110
- BDID: 0x18
- iOS: 26.6.1
- Build: 23G83
- observed iBoot family: mBoot-18000.162.10

Recovery Mode does not expose BFU plaintext or passcode-derived Data Protection keys through this query.
