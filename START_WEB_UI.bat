@echo off
chcp 65001 >nul
echo ================================================================
echo   SIAPS Web UI Launcher
echo ================================================================
echo.
echo Installing dependencies if needed...
python -c "import flask" 2>nul || pip install Flask Flask-CORS
echo.
echo Starting Web UI...
python run_web_ui.py
pause
