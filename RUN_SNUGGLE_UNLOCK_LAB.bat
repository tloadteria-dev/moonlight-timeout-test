@echo off
setlocal
title Snuggle Unlock Lab :3
cd /d "%~dp0"
echo ==========================================
echo          SNUGGLE UNLOCK LAB :3
echo ==========================================
set "PY="
where py >nul 2>&1 && set "PY=py -3"
if not defined PY where python >nul 2>&1 && set "PY=python"
if not defined PY (
  echo Python 3 was not found.
  pause
  exit /b 1
)
%PY% snuggle_unlock_lab.py --profile vulnerable
if errorlevel 1 goto FAIL
%PY% snuggle_unlock_lab.py --profile patched
if errorlevel 1 goto FAIL
echo.
echo Cute Recovery comparison complete :3
start "" notepad.exe "%~dp0snuggle-lab-results\snuggle-vulnerable.json"
start "" notepad.exe "%~dp0snuggle-lab-results\snuggle-patched.json"
pause
exit /b 0
:FAIL
echo Snuggle lab failed.
pause
exit /b 1
