@echo off
REM YouTube SEO Analyzer - Windows Setup Script

echo ================================================
echo YouTube SEO Analyzer - Setup
echo ================================================
echo.

REM Check Python installation
echo Checking Python installation...
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python is not installed or not in PATH
    echo Please install Python 3.8 or higher from https://www.python.org/
    echo.
    pause
    exit /b 1
)

python --version
echo.

REM Upgrade pip
echo Upgrading pip...
python -m pip install --upgrade pip
echo.

REM Install requirements
echo Installing dependencies...
echo This may take a few minutes...
echo.
pip install -r requirements.txt

if errorlevel 1 (
    echo.
    echo [ERROR] Failed to install dependencies
    echo Please check your internet connection and try again
    echo.
    pause
    exit /b 1
)

echo.
echo ================================================
echo Setup Complete!
echo ================================================
echo.
echo To run the application, use:
echo     python main.py
echo.
echo For help, see README.md or QUICKSTART.md
echo.
pause

