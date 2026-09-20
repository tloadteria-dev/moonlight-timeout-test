# 🌸 tiny dummy detector 🌸

A read-only, fail-closed discriminator helper.

It runs only `irecovery -q`, records the raw result, and writes:
- `cute-dummy-check/dummy-check.txt`
- `cute-dummy-check/dummy-evidence.json`

It says **yup its a dummy** only when an explicit lab-only marker is returned. Normal iPhone identity values do not count as proof. Otherwise it says **not a dummy**.

This tool does not alter, unlock, restore, update, erase, or bypass authentication on the connected device.
