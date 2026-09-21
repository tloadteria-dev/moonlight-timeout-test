# 🌸 Snuggle Unlock Lab :3

Synthetic authentication-state Recovery harness.

It compares two local models:

- vulnerable: simulated BFU/passcode-required state transitions to simulated unlocked
- patched: authentication requirements remain enforced

Run `RUN_SNUGGLE_UNLOCK_LAB.bat`.

Outputs are written to `snuggle-lab-results/`.

This harness does not send commands or payloads to an iPhone and does not modify device authentication state.
