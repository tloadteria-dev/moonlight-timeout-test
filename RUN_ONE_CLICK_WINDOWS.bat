@echo off
setlocal
cd /d "%~dp0"
set "OUT=one-click-results"
if exist "%OUT%" rmdir /s /q "%OUT%"
if exist "%OUT%" goto :fail
if exist "fun-testing-phone-thing-results.zip" del /q "fun-testing-phone-thing-results.zip"
where python >nul 2>nul || goto :fail
echo [1/4] Read-only Recovery query
python recovery_inspector.py --output "%OUT%"
if errorlevel 1 goto :fail
echo [2/4] Synthetic vulnerable Face-ID eligibility model
python fun_testing_phone_thing.py --mode vulnerable --out "%OUT%\vulnerable.json"
if errorlevel 1 goto :fail
echo [3/4] Synthetic patched control
python fun_testing_phone_thing.py --mode patched --out "%OUT%\patched.json"
if errorlevel 1 goto :fail
echo [4/4] Packaging
powershell -NoProfile -Command "Compress-Archive -Path '%OUT%\*' -DestinationPath 'fun-testing-phone-thing-results.zip' -Force"
if errorlevel 1 goto :fail
echo.
echo RECOVERY VALIDATION COMPLETE
echo Results: %CD%\%OUT%
echo Package: %CD%\fun-testing-phone-thing-results.zip
pause
exit /b 0
:fail
echo.
echo RECOVERY VALIDATION STOPPED. Capture this window and the one-click-results folder.
pause
exit /b 1
