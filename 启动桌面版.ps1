# SIAPS - 股票智能分析预测系统 桌面版启动脚本

# 清除环境变量
$env:PYTHONHOME = ""
$env:PYTHONPATH = ""

# 改变工作目录
Push-Location (Split-Path -Parent $MyInvocation.MyCommand.Path)

Write-Host "================================================================"
Write-Host "  SIAPS - 股票智能分析预测系统 桌面版"
Write-Host '  Stock Intelligent Analysis & Prediction System - Desktop'
Write-Host "================================================================"
Write-Host ""
Write-Host "当前目录: $(Get-Location)"
Write-Host "Current directory: $(Get-Location)"
Write-Host ""

# 检查 main.py 是否存在
if (-not (Test-Path "main.py")) {
    Write-Host "[错误] 找不到 main.py 文件！"
    Write-Host "[ERROR] Cannot find main.py file!"
    Write-Host ""
    Write-Host "请确保您在正确的项目目录中"
    Write-Host "Please make sure you are in the correct project directory"
    Write-Host ""
    Read-Host "按 Enter 继续... / Press Enter to continue..."
    exit 1
}

Write-Host "正在启动桌面版界面..."
Write-Host "Starting Desktop GUI..."
Write-Host ""

Write-Host "[√] 使用系统 Python / Using system Python"
Write-Host ""

# 安装依赖
Write-Host "[!] 安装依赖包 / Installing requirements..."
& "C:\Users\龚若兰\AppData\Local\Programs\Python\Python312\python.exe" -m pip install -r requirements.txt -q
Write-Host ""

Write-Host "运行: python main.py"
Write-Host "Running: python main.py"
Write-Host ""

# 从其他目录运行 Python  
$projectDir = Get-Location
Push-Location "d:\"
& "C:\Users\龚若兰\AppData\Local\Programs\Python\Python312\python.exe" "$projectDir/main.py"
Pop-Location

Pop-Location
