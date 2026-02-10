# GitHub Copilot Skills 自动安装脚本 (Windows版)
# 适用于 JericoNewStockSystem 项目

Write-Host "🚀 开始安装 GitHub Copilot Skills..." -ForegroundColor Green

# 设置变量
$SkillsDir = ".github\copilot"
$RepoUrl = "https://raw.githubusercontent.com/github/awesome-copilot/main/skills"

# 技能列表
$Skills = @(
    "refactor",
    "webapp-testing",
    "github-issues",
    "plantuml-ascii",
    "git-commit"
)

# 创建目录
if (!(Test-Path $SkillsDir)) {
    New-Item -ItemType Directory -Path $SkillsDir -Force | Out-Null
    Write-Host "✅ 创建目录 $SkillsDir" -ForegroundColor Green
}

# 下载每个技能
foreach ($skill in $Skills) {
    Write-Host "📥 下载 $skill..." -ForegroundColor Yellow
    $url = "$RepoUrl/$skill/SKILL.md"
    $output = "$SkillsDir\$skill.skill.md"
    
    try {
        Invoke-WebRequest -Uri $url -OutFile $output -ErrorAction Stop
        Write-Host "✅ $skill 安装成功" -ForegroundColor Green
    }
    catch {
        Write-Host "❌ $skill 安装失败: $_" -ForegroundColor Red
    }
}

Write-Host ""
Write-Host "🎉 安装完成! 已安装技能:" -ForegroundColor Green
Get-ChildItem $SkillsDir | Format-Table Name

Write-Host ""
Write-Host "📝 下一步:" -ForegroundColor Cyan
Write-Host "1. 重启 VS Code"
Write-Host "2. 打开 GitHub Copilot Chat"
Write-Host "3. 输入 @ 查看已安装的技能"