@echo off
REM Launch EOC Log Analyzer Streamlit UI

echo =====================================
echo EOC Log Analyzer - Web UI
echo =====================================
echo.

cd /d %~dp0

REM Check if virtual environment exists
if not exist venv\Scripts\python.exe (
    echo ERROR: Virtual environment not found!
    echo Please run: setup_venv.bat first
    pause
    exit /b 1
)

REM Activate virtual environment and run Streamlit
echo Starting Streamlit UI...
echo.
echo The UI will open in your browser automatically.
echo Press Ctrl+C to stop the server.
echo.

venv\Scripts\python.exe -m streamlit run streamlit_app.py

pause
