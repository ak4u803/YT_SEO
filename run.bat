@echo off
REM Quick run script for YouTube SEO Analyzer (Windows)

echo Starting YouTube SEO Analyzer...
echo.
python main.py

if errorlevel 1 (
    echo.
    echo [ERROR] Failed to start the application
    echo Make sure you have run setup.bat first
    echo.
    pause
)

