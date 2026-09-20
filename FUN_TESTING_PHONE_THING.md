# fun testing phone thing

Synthetic Recovery validation for the iPhone14,7 / iOS 26.6.1 / 23G83 state profile.

The workflow exercises one deliberately vulnerable synthetic transition from PASSCODE_REQUIRED to FACE_ID_ELIGIBLE and verifies that patched mode blocks it.

This project has no USB, Bluetooth, libimobiledevice, irecovery, lockdown, iBoot, or physical-device control path. It cannot change Face ID state on an iPhone.
