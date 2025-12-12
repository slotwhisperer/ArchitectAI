@echo off
title Architect AI Launcher

echo Starting Architect AI...
echo.

REM Navigate to project folder
cd /d C:\Architect AI

REM Activate virtual environment
call venv\Scripts\activate

REM Launch Streamlit UI
python main.py ui

pause
