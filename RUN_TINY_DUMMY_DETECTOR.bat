@echo off
title 🌸 tiny dummy detector 🌸
echo ==========================================
echo        TINY DUMMY DETECTOR :3
echo ==========================================
where python >nul 2>&1 || (echo Python not found.& pause & exit /b 1)
python tiny_dummy_detector.py
echo.
echo Opening result...
notepad "cute-dummy-check\dummy-check.txt"
pause
