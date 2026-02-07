@echo off
cd /d "%~dp0"
title Trimurti LAW Server
echo.
echo  =======================================================
echo        TRIMURTI LAW - AI Legal Assistant
echo  =======================================================
echo.
echo  [INFO] Auto-initiating AI Services...
REM start /MIN "Trimurti Ingestion" cmd /c "py tools/ingest_scotus_bulk.py > ingest.log 2>&1"
echo.
echo  [INFO] Launching Interface...
echo  [INFO] Please wait while the browser opens...
echo.
py -m streamlit run trimurti_app.py
if %errorlevel% neq 0 (
    echo.
    echo [ERROR] Streamlit not found or crashed.
    echo Ensure you have streamlit installed: pip install streamlit
    pause
)
pause
