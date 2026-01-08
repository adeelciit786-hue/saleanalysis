@echo off
REM Sales Forecasting Dashboard - Quick Start
REM Run this file to start the application

echo.
echo ======================================================
echo  Enterprise Sales Forecasting Dashboard
echo ======================================================
echo.

cd /d "%~dp0"

REM Activate virtual environment
call venv\Scripts\activate.bat

REM Change to app directory
cd sales_app

REM Start Flask app
echo Starting Flask application on http://localhost:5000
echo Press Ctrl+C to stop the server
echo.
python app.py

pause
