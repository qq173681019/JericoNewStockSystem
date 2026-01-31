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
    pause
    exit /b 1
)

REM Check if virtual environment exists
if not exist ".venv\Scripts\python.exe" (
    echo [!] 虚拟环境不存在，正在创建...
    echo [!] Virtual environment not found, creating...
    python -m venv .venv
    if errorlevel 1 (
        echo [错误] 创建虚拟环境失败！
        echo [ERROR] Failed to create virtual environment!
        pause
        exit /b 1
    )
)

REM Use virtual environment Python
set PYTHON=.venv\Scripts\python.exe
set PIP=.venv\Scripts\pip.exe

echo 正在启动 Web 界面服务器...
echo Starting Web UI server...
echo.

REM Check if Flask is installed in venv
%PYTHON% -c "import flask" 2>nul
if errorlevel 1 (
    echo [!] 检测到缺少依赖包，正在安装...
    echo [!] Installing required packages...
    %PIP% install Flask Flask-CORS python-dotenv requests
    echo.
)

REM Start the web server
echo 运行: %PYTHON% run_web_ui.py
echo Running: %PYTHON% run_web_ui.py
echo.
%PYTHON% run_web_ui.py

pause
