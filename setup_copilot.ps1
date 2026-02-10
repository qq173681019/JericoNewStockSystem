<#
.SYNOPSIS
    GitHub Copilot 资源自动配置脚本
.DESCRIPTION
    为 JericoNewStockSystem 项目配置 Copilot Skills、Agents、Prompts 和 Instructions
.AUTHOR
    Generated for ext.jgu
#>

# 设置错误处理
$ErrorActionPreference = "Stop"

Write-Host "╔═══════════════════════════════════════════════════════════╗" -ForegroundColor Cyan
Write-Host "║   🚀 GitHub Copilot 资源配置工具                         ║" -ForegroundColor Cyan
Write-Host "║   项目: JericoNewStockSystem                             ║" -ForegroundColor Cyan
Write-Host "╚═══════════════════════════��═══════════════════════════════╝" -ForegroundColor Cyan
Write-Host ""

# 定义路径
$ProjectRoot = $PSScriptRoot
$CopilotDir = Join-Path $ProjectRoot ".github\copilot"
$VSCodeDir = Join-Path $ProjectRoot ".vscode"

# ============================================================================
# 第一步：检查文件结构
# ============================================================================
Write-Host "📂 第一步: 检查文件结构..." -ForegroundColor Yellow
Write-Host ""

$requiredDirs = @{
    "Skills"       = $CopilotDir
    "Agents"       = Join-Path $CopilotDir "agents"
    "Prompts"      = Join-Path $CopilotDir "prompts"
    "Instructions" = Join-Path $CopilotDir "instructions"
}

$stats = @{}

foreach ($key in $requiredDirs.Keys) {
    $path = $requiredDirs[$key]
    
    if (Test-Path $path) {
        $files = Get-ChildItem -Path $path -File
        $count = $files.Count
        $stats[$key] = $count
        
        Write-Host "  ✅ $key 目录存在: " -ForegroundColor Green -NoNewline
        Write-Host "$count 个文件" -ForegroundColor White
        
        # 显示文件列表
        $files | ForEach-Object {
            Write-Host "     - $($_.Name)" -ForegroundColor Gray
        }
    } else {
        Write-Host "  ❌ $key 目录不存在: $path" -ForegroundColor Red
        $stats[$key] = 0
    }
}

Write-Host ""

# ============================================================================
# 第二步：创建 VS Code 配置
# ============================================================================
Write-Host "⚙️  第二步: 配置 VS Code 设置..." -ForegroundColor Yellow
Write-Host ""

# 创建 .vscode 目录
if (!(Test-Path $VSCodeDir)) {
    New-Item -ItemType Directory -Path $VSCodeDir -Force | Out-Null
    Write-Host "  ✅ 创建 .vscode 目录" -ForegroundColor Green
}

# 查找所有 instructions 文件
$instructionsFiles = Get-ChildItem -Path (Join-Path $CopilotDir "instructions") -Filter "*.instructions.md" -ErrorAction SilentlyContinue

# 构建 VS Code 配置
$vscodeSettings = @{
    "github.copilot.enable" = @{
        "*"        = $true
        "markdown" = $true
        "python"   = $true
        "yaml"     = $true
        "json"     = $true
    }
    "github.copilot.chat.codeGeneration.instructions" = @()
}

# 添加 instructions 引用
if ($instructionsFiles) {
    foreach ($file in $instructionsFiles) {
        $relativePath = ".github/copilot/instructions/$($file.Name)" -replace '\\', '/'
        $vscodeSettings["github.copilot.chat.codeGeneration.instructions"] += @{
            "file" = $relativePath
        }
        Write-Host "  📋 添加 Instruction: $($file.Name)" -ForegroundColor Cyan
    }
}

# 保存配置文件
$settingsPath = Join-Path $VSCodeDir "settings.json"
$vscodeSettings | ConvertTo-Json -Depth 10 | Set-Content $settingsPath -Encoding UTF8

Write-Host "  ✅ VS Code 配置已保存: .vscode\settings.json" -ForegroundColor Green
Write-Host ""

# ============================================================================
# 第三步：生成 Agents 清单
# ============================================================================
Write-Host "🤖 第三步: 分析 Agents..." -ForegroundColor Yellow
Write-Host ""

$agentsPath = Join-Path $CopilotDir "agents"
$agentsList = @()

if (Test-Path $agentsPath) {
    $agentFiles = Get-ChildItem -Path $agentsPath -Filter "*.agent.md"
    
    foreach ($file in $agentFiles) {
        $agentName = $file.BaseName -replace '\.agent$', ''
        $content = Get-Content $file.FullName -Raw
        
        # 尝试提取描述（从 YAML front matter）
        $description = "专业AI助手"
        if ($content -match '(?s)description:\s*[''"](.+?)[''"]') {
            $description = $matches[1]
        }
        
        $agentsList += [PSCustomObject]@{
            Name        = $agentName
            FileName    = $file.Name
            Description = $description
            Command     = "@$agentName"
        }
        
        Write-Host "  🤖 $agentName" -ForegroundColor Cyan
        Write-Host "     命令: @$agentName" -ForegroundColor Gray
    }
}

Write-Host ""

# ============================================================================
# 第四步：生成 Prompts 清单
# ============================================================================
Write-Host "📝 第四步: 分析 Prompts..." -ForegroundColor Yellow
Write-Host ""

$promptsPath = Join-Path $CopilotDir "prompts"
$promptsList = @()

if (Test-Path $promptsPath) {
    $promptFiles = Get-ChildItem -Path $promptsPath -Filter "*.prompt.md"
    
    foreach ($file in $promptFiles) {
        $promptName = $file.BaseName -replace '\.prompt$', ''
        
        $promptsList += [PSCustomObject]@{
            Name     = $promptName
            FileName = $file.Name
        }
        
        Write-Host "  📝 $promptName" -ForegroundColor Cyan
    }
}

Write-Host ""

# ============================================================================
# 第五步：生成使用指南
# ============================================================================
Write-Host "📚 第五步: 生成使用指南..." -ForegroundColor Yellow
Write-Host ""

$guideContent = @"
# 🎯 GitHub Copilot 资源使用指南

> 自动生成于: $(Get-Date -Format "yyyy-MM-dd HH:mm:ss")
> 项目: JericoNewStockSystem

---

## 📊 资源统计

| 资源类型 | 数量 | 说明 |
|---------|------|------|
| **Skills** | $($stats['Skills']) 个 | 可执行的技能集 |
| **Agents** | $($stats['Agents']) 个 | 专业AI助手 |
| **Prompts** | $($stats['Prompts']) 个 | 可复用提示词模板 |
| **Instructions** | $($stats['Instructions']) 个 | 全局最佳实践规则 |

---

## 🔧 1. Skills - 技能使用

### 已安装的 Skills：

``````powershell
# 查看所有 Skills
Get-ChildItem .github\copilot\*.skill.md