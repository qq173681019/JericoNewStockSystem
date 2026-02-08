@echo off
chcp 65001 >nul

REM Change to the directory where this batch file is located
cd /d "%~dp0"

echo ================================================================
echo   SIAPS - 股票智能分析预测系统 桌面版
echo   Stock Intelligent Analysis ^& Prediction System - Desktop
echo ================================================================
echo.
echo 当前目录: %CD%
echo Current directory: %CD%
echo.

REM Check if main.py exists
if not exist "main.py" (
    echo [错误] 找不到 main.py 文件！
    echo [ERROR] Cannot find main.py file!
    echo.
    echo 请确保您在正确的项目目录中
    echo Please make sure you are in the correct project directory
    echo.
    pause
    exit /b 1
)

echo 正在启动桌面版界面...
echo Starting Desktop GUI...
echo.

REM Check if customtkinter and python-dotenv are installed
python -c "import customtkinter" 2>nul
if errorlevel 1 (
    echo [!] 检测到缺少 customtkinter，正在安装...
    echo [!] Installing customtkinter...
    pip install customtkinter
    echo.
)

python -c "import dotenv" 2>nul
if errorlevel 1 (
    echo [!] 检测到缺少 python-dotenv，正在安装...
    echo [!] Installing python-dotenv...
    pip install python-dotenv
    echo.
)

echo 运行: python main.py
echo Running: python main.py
echo.
python main.py

if errorlevel 1 (
    echo.
    echo [错误] 程序运行失败
    echo [ERROR] Program failed to run
    echo.
    echo 如果看到 ModuleNotFoundError，请运行:
    echo If you see ModuleNotFoundError, please run:
    echo   pip install -r requirements.txt
    echo.
)

pause
