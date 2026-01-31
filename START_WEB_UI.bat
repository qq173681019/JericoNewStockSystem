@echo off
chcp 65001 >nul

REM Change to the directory where this batch file is located
cd /d "%~dp0"

echo ================================================================
echo   SIAPS Web UI Launcher
echo ================================================================
echo.
echo Current directory: %CD%
echo.
echo Installing dependencies if needed...
python -c "import flask" 2>nul
if errorlevel 1 (
    echo Installing Flask and Flask-CORS...
    pip install Flask Flask-CORS
)
echo.
echo Starting Web UI...
echo Running: python run_web_ui.py
echo.
python run_web_ui.py
pause
