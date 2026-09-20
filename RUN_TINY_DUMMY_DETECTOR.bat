@echo off
setlocal
title Silly Dummy Phone Test :3
cd /d "%~dp0"

echo ==========================================
echo        SILLY DUMMY PHONE TEST :3
echo ==========================================

mkdir "cute-dummy-check" >nul 2>&1
set "RESULT=%~dp0cute-dummy-check\dummy-check.txt"
set "RAW=%~dp0cute-dummy-check\phone-contact.txt"

set "MSYSROOT=D:\GPTdump\!PHONESTUFF\!OSSSS\INSTALL\EDmsys"
set "BASH=%MSYSROOT%\usr\bin\bash.exe"

if not exist "%BASH%" (
  >"%RESULT%" echo dummy test failed - cute MSYS2 path was not found
  goto OPEN_RESULT
)

set "CHERE_INVOKING=1"
set "MSYSTEM=UCRT64"
"%BASH%" -lc "export PATH=/ucrt64/bin:/usr/bin:$PATH; irecovery -q" >"%RAW%" 2>&1
set "RC=%ERRORLEVEL%"

if not "%RC%"=="0" (
  >"%RESULT%" echo dummy test failed - could not read the Recovery device
  goto OPEN_RESULT
)

findstr /I /C:"MODE: Recovery" "%RAW%" >nul
if errorlevel 1 (
  >"%RESULT%" echo dummy test failed - no Recovery device identity returned
  goto OPEN_RESULT
)

findstr /I /C:"zack_dummy" /C:"synthetic=true" /C:"cute_dummy_marker" /C:"lab_only=true" /C:"simulator_only=true" "%RAW%" >nul
if not errorlevel 1 (
  >"%RESULT%" echo yup its a dummy :3
  >>"%RESULT%" echo.
  >>"%RESULT%" echo Dummy-only marker detected in the Recovery response.
  >>"%RESULT%" echo.
  findstr /I /C:"zack_dummy" /C:"synthetic=true" /C:"cute_dummy_marker" /C:"lab_only=true" /C:"simulator_only=true" "%RAW%" >>"%RESULT%"
  goto OPEN_RESULT
)

>"%RESULT%" echo dummy not proven :3
>>"%RESULT%" echo.
>>"%RESULT%" echo Phone contact works, but no configured dummy-only marker appeared.
>>"%RESULT%" echo.
>>"%RESULT%" echo Recovery device information:
findstr /I /B /C:"MODE:" /C:"PRODUCT:" /C:"MODEL:" /C:"NAME:" "%RAW%" >>"%RESULT%"

:OPEN_RESULT
echo.
echo Opening cute dummy result...
start "" notepad.exe "%RESULT%"
echo Raw read-only Recovery response:
echo %RAW%
pause
exit /b 0
