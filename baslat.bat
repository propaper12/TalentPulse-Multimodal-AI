@echo off
title TalentPulse - AI Interview Stream Pipeline
cd /d "%~dp0"
echo ========================================================
echo   TalentPulse ⚡ AI Interview Stream & HR Analytics
echo   Gelistirici: Omer Cakan
echo ========================================================
echo.
echo Sunucu baslatiliyor (http://127.0.0.1:8000)...
echo Tarayicinizda dashboard acilacak...
start http://127.0.0.1:8000
python main.py
pause
