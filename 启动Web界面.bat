@echo off
chcp 65001 >nul
echo ================================================================
echo   SIAPS - 股票智能分析预测系统 Web 界面
echo   Stock Intelligent Analysis ^& Prediction System - Web UI
echo ================================================================
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
python run_web_ui.py

pause
