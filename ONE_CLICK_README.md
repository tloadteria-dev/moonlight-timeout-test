# fun testing phone thing - one click

Windows one-click runner combining the existing read-only Recovery query with the already-passing synthetic 23G83 authentication-state validation.

## Run
1. Connect only the test/dummy phone by USB.
2. Put it in Recovery Mode.
3. Ensure Python 3 and `irecovery.exe` are available in PATH.
4. Double-click `RUN_ONE_CLICK_WINDOWS.bat`.

The runner executes, in order:
- read-only `irecovery -q` collection;
- synthetic vulnerable `PASSCODE_REQUIRED -> FACE_ID_ELIGIBLE` model;
- synthetic patched control;
- ZIP packaging.

Device-facing behavior is read-only. The Face-ID eligibility transition exists only in the synthetic model; this package has no USB/Bluetooth/lockdown/iBoot authentication-mutation path.
