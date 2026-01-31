@echo off
chcp 65001 >nul

REM Change to the directory where this batch file is located
cd /d "%~dp0"

echo ================================================================
echo   SIAPS - 股票智能分析预测系统 Web 界面
echo   Stock Intelligent Analysis ^& Prediction System - Web UI
echo ================================================================
echo.
echo 当前目录: %CD%
echo Current directory: %CD%
echo.
echo 正在启动 Web 界面服务器...
echo Starting Web UI server...
echo.

REM Check if Flask is installed
python -c "import flask" 2>nul
if errorlevel 1 (
    echo [!] 检测到缺少依赖包，正在安装...
    echo [!] Installing required packages...
    pip install Flask Flask-CORS
    echo.
)

REM Start the web server
echo 运行: python run_web_ui.py
echo Running: python run_web_ui.py
echo.
python run_web_ui.py

pause
