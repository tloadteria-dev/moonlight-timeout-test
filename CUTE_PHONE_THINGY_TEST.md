# cute phone thingy test

Standalone synthetic passcode-recovery regression for the iPhone14,7 / D27AP / A15 / iOS 26.6.1 / 23G83 profile.

Vulnerable mode intentionally models PASSCODE_REQUIRED -> UNLOCKED, disables the simulated passcode, and verifies access to generated synthetic user data. Patched mode must keep PASSCODE_REQUIRED and deny that data.

This workflow has no device transport and cannot remove or bypass a passcode on a physical iPhone.
