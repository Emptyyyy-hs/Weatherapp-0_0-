@echo off
echo Starting Weather App...
echo.

REM check if python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo Python is not installed. Please install Python from https://python.org
    pause
    exit
)

REM install requests if not already installed
echo Installing required packages...
pip install requests --quiet

echo.
echo Launching app...
python weather_app.py

pause
