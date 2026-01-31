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
echo 正在启动桌面版界面...
echo Starting Desktop GUI...
echo.

REM Check if customtkinter is installed
python -c "import customtkinter" 2>nul
if errorlevel 1 (
    echo [!] 检测到缺少依赖包，正在安装...
    echo [!] Installing required packages...
    pip install customtkinter
    echo.
)

echo 运行: python main.py
echo Running: python main.py
echo.
python main.py

pause
