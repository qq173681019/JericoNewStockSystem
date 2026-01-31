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

REM Check if run_web_ui.py exists
if not exist "run_web_ui.py" (
    echo [错误] 找不到 run_web_ui.py 文件！
    echo [ERROR] Cannot find run_web_ui.py file!
    echo.
    echo 可能的原因：
    echo Possible reasons:
    echo 1. 您的代码不是最新版本，需要从GitHub拉取最新代码
    echo    Your code is not up-to-date, need to pull latest from GitHub
    echo.
    echo 2. 您可能在错误的目录运行此文件
    echo    You might be running this file in wrong directory
    echo.
    echo 解决方案：
    echo Solution:
    echo 1. 打开Git Bash或命令提示符
    echo    Open Git Bash or Command Prompt
    echo.
    echo 2. 运行: git pull origin copilot/build-ui-with-pencil-plugin-again
    echo    Run: git pull origin copilot/build-ui-with-pencil-plugin-again
    echo.
    echo 3. 或者: git fetch ^&^& git checkout copilot/build-ui-with-pencil-plugin-again
    echo    Or: git fetch ^&^& git checkout copilot/build-ui-with-pencil-plugin-again
    echo.
    pause
    exit /b 1
)

echo 正在启动 Web 界面服务器...
echo Starting Web UI server...
echo.

REM Check if Flask is installed
python -c "import flask" 2>nul
if errorlevel 1 (
    echo [!] 检测到缺少依赖包，正在安装...
    echo [!] Installing required packages...
    pip install Flask Flask-CORS python-dotenv
    echo.
)

REM Start the web server
echo 运行: python run_web_ui.py
echo Running: python run_web_ui.py
echo.
python run_web_ui.py

pause
