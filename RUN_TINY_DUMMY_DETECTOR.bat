@echo off
setlocal
title Silly Phone Test :3
cd /d "%~dp0"

echo ==========================================
echo          SILLY PHONE TEST :3
echo ==========================================

set "PY="
where py >nul 2>&1 && set "PY=py -3"
if not defined PY where python >nul 2>&1 && set "PY=python"
if not defined PY where python3 >nul 2>&1 && set "PY=python3"

if not defined PY (
  mkdir "cute-dummy-check" >nul 2>&1
  >"cute-dummy-check\dummy-check.txt" echo detector could not start - Python was not found
  echo Python was not found.
  goto OPEN_RESULT
)

set "IRECOVERY_EXE="
where irecovery >nul 2>&1 && for /f "delims=" %%I in ('where irecovery 2^>nul') do if not defined IRECOVERY_EXE set "IRECOVERY_EXE=%%I"

if not defined IRECOVERY_EXE (
  for %%I in (
    "C:\msys64\ucrt64\bin\irecovery.exe"
    "C:\msys64\mingw64\bin\irecovery.exe"
    "C:\msys64\usr\bin\irecovery.exe"
  ) do if exist "%%~I" if not defined IRECOVERY_EXE set "IRECOVERY_EXE=%%~I"
)

if not defined IRECOVERY_EXE (
  mkdir "cute-dummy-check" >nul 2>&1
  >"cute-dummy-check\dummy-check.txt" echo detector could not read the phone - MSYS2 irecovery was not found
  echo MSYS2 irecovery was not found.
  goto OPEN_RESULT
)

echo Using Recovery reader:
echo %IRECOVERY_EXE%
echo.

set "IRECOVERY_EXE=%IRECOVERY_EXE%"
%PY% tiny_dummy_detector.py
set "DETECTOR_EXIT=%ERRORLEVEL%"

:OPEN_RESULT
if not exist "cute-dummy-check\dummy-check.txt" (
  mkdir "cute-dummy-check" >nul 2>&1
  >"cute-dummy-check\dummy-check.txt" echo detector did not create a result
)

echo.
echo Opening cute result...
start "" notepad.exe "%~dp0cute-dummy-check\dummy-check.txt"
echo.
echo Evidence is saved in cute-dummy-check\dummy-evidence.json
pause
exit /b 0
