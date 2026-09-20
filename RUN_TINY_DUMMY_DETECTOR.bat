@echo off
setlocal
title Silly Phone Contact Test :3
cd /d "%~dp0"

echo ==========================================
echo       SILLY PHONE CONTACT TEST :3
echo ==========================================

mkdir "cute-dummy-check" >nul 2>&1
set "RESULT=%~dp0cute-dummy-check\dummy-check.txt"
set "RAW=%~dp0cute-dummy-check\phone-contact.txt"

set "BASH="
for %%B in (
  "C:\msys64\usr\bin\bash.exe"
  "C:\tools\msys64\usr\bin\bash.exe"
  "D:\msys64\usr\bin\bash.exe"
) do if exist "%%~B" if not defined BASH set "BASH=%%~B"

if not defined BASH (
  for /f "delims=" %%B in ('where bash.exe 2^>nul') do if not defined BASH set "BASH=%%B"
)

if not defined BASH (
  >"%RESULT%" echo silly phone contact failed - MSYS2 bash was not found
  goto OPEN_RESULT
)

echo Contacting phone through MSYS2 UCRT64...
"%BASH%" -lc "export PATH=/ucrt64/bin:/usr/bin:$PATH; command -v irecovery; irecovery -q" >"%RAW%" 2>&1
set "RC=%ERRORLEVEL%"

if not "%RC%"=="0" (
  >"%RESULT%" echo silly phone contact failed - irecovery could not read a Recovery device
  goto OPEN_RESULT
)

findstr /I /C:"MODE: Recovery" "%RAW%" >nul
if errorlevel 1 (
  >"%RESULT%" echo silly phone contact failed - no Recovery device identity returned
  goto OPEN_RESULT
)

>"%RESULT%" echo silly phone contact works :3
>>"%RESULT%" echo.
>>"%RESULT%" echo Recovery device information:
findstr /I /B /C:"MODE:" /C:"PRODUCT:" /C:"MODEL:" /C:"NAME:" "%RAW%" >>"%RESULT%"

:OPEN_RESULT
echo.
echo Opening cute result...
start "" notepad.exe "%RESULT%"
echo Raw read-only contact log:
echo %RAW%
pause
exit /b 0
