@echo off
setlocal
title Tiny Dummy Detector :3
cd /d "%~dp0"
echo ==========================================
echo        TINY DUMMY DETECTOR :3
echo ==========================================
set "PY="
where py >nul 2>&1 && set "PY=py -3"
if not defined PY where python >nul 2>&1 && set "PY=python"
if not defined PY where python3 >nul 2>&1 && set "PY=python3"
if not defined PY (
  echo Python was not found.
  echo Install Python 3 or make it available in PATH, then run this again.
  pause
  exit /b 1
)
%PY% tiny_dummy_detector.py
if errorlevel 1 (
  echo.
  echo Detector failed. Do not treat this as a dummy verdict.
  pause
  exit /b 1
)
if not exist "cute-dummy-check\dummy-check.txt" (
  echo Result file was not created.
  pause
  exit /b 1
)
echo.
echo Opening result...
notepad.exe "%~dp0cute-dummy-check\dummy-check.txt"
pause
