# Vercel 部署指南 / Vercel Deployment Guide

## 🎯 问题已修复！/ Issue Fixed!

本项目现已修复 Vercel 部署问题，可以成功部署到 Vercel 平台！

The Vercel deployment issue has been fixed! The project can now be successfully deployed to Vercel.

### 最新修复 / Latest Fix

**缓冲区溢出错误已解决！** 如果您之前遇到 `RangeError [ERR_OUT_OF_RANGE]` 错误，现已修复。[查看详情](VERCEL_FIX.md)

**Buffer overflow error fixed!** If you previously encountered `RangeError [ERR_OUT_OF_RANGE]` error, it's now fixed. [See details](VERCEL_FIX.md)

---

## 📋 修复内容 / What Was Fixed

### 问题原因 / Root Cause
Vercel 无法找到 Flask 应用入口点。Vercel 期望在以下位置找到 Flask 应用：
- `app.py`
- `index.py`
- `main.py`
- 等等...

但我们的 Flask 应用定义在 `run_web_ui.py` 中，导致部署失败。

Vercel couldn't find the Flask entrypoint. It expects the Flask app in specific locations like `app.py`, `index.py`, `main.py`, etc., but our app was defined in `run_web_ui.py`.

### 解决方案 / Solution
1. **创建 `app.py` 入口文件** - 从 `run_web_ui.py` 导入 Flask 应用
2. **创建 `vercel.json` 配置文件** - 指定 Vercel 构建和部署配置

---

## 🚀 一键部署到 Vercel / Deploy to Vercel

### 方法 1：使用 Vercel 按钮（推荐）

点击下面的按钮一键部署：

[![Deploy with Vercel](https://vercel.com/button)](https://vercel.com/new/clone?repository-url=https://github.com/qq173681019/JericoNewStockSystem)

### 方法 2：从 GitHub 导入

#### 步骤 1：准备工作 / Prerequisites
- 确保代码已推送到 GitHub
- 访问 [Vercel](https://vercel.com/)
- 使用 GitHub 账号登录

#### 步骤 2：导入项目 / Import Project
1. 点击 "Add New..." → "Project"
2. 选择 "Import Git Repository"
3. 授权 Vercel 访问您的 GitHub
4. 选择 `JericoNewStockSystem` 仓库
5. 点击 "Import"

#### 步骤 3：配置项目 / Configure Project
Vercel 会自动检测配置，无需修改：
- **Framework Preset**: 自动检测为 "Other"
- **Build Command**: 自动配置
- **Output Directory**: 自动配置

直接点击 "Deploy" 开始部署！

#### 步骤 4：等待部署 / Wait for Deployment
- Vercel 会自动构建和部署（约 2-3 分钟）
- 部署成功后会自动生成域名

#### 步骤 5：访问应用 / Access Your App
在浏览器中打开 Vercel 提供的域名即可访问！

---

## 📁 项目文件说明 / Project Files

### 新增文件 / New Files

#### `app.py`
```python
# Flask 应用入口点，Vercel 部署必需
# Flask entrypoint for Vercel deployment
from run_web_ui import app
```

这个文件是 Vercel 识别 Flask 应用的关键。它从 `run_web_ui.py` 导入已定义的 Flask 应用。

This file is essential for Vercel to recognize the Flask application. It imports the Flask app from `run_web_ui.py`.

#### `vercel.json`
```json
{
  "version": 2,
  "builds": [
    {
      "src": "app.py",
      "use": "@vercel/python"
    }
  ],
  "routes": [
    {
      "src": "/(.*)",
      "dest": "app.py"
    }
  ],
  "env": {
    "FLASK_APP": "app.py"
  }
}
```

Vercel 平台配置文件，指定：
- 使用 Python 构建器
- 入口文件为 `app.py`
- 所有路由指向 Flask 应用

Vercel platform configuration that specifies:
- Using Python builder
- Entrypoint is `app.py`
- All routes point to the Flask app

### 现有文件 / Existing Files

#### `run_web_ui.py`
包含完整的 Flask 应用定义和所有路由。`app.py` 从这里导入应用。

Contains the complete Flask application definition and all routes. `app.py` imports the app from here.

#### `requirements-prod.txt`
生产环境依赖列表，已优化用于云部署（移除了 TensorFlow、PyTorch 等重型库）。

Production dependencies, optimized for cloud deployment (removed TensorFlow, PyTorch, etc.).

---

## ⚙️ 环境变量 / Environment Variables

Vercel 会自动设置以下环境变量：
- `PORT` - Vercel 自动提供
- `VERCEL` - 标识在 Vercel 环境运行
- `VERCEL_ENV` - 环境类型（production/preview）

如需添加自定义环境变量，在 Vercel 项目设置中添加。

---

## 🔧 常见问题 / FAQ

### Q: Vercel 和 Railway 有什么区别？

**A**: 两个平台都支持部署，但有不同特点：

| 特性 | Vercel | Railway |
|-----|--------|---------|
| 部署速度 | 快 (1-2分钟) | 中等 (3-5分钟) |
| 免费额度 | 100 GB流量/月 | 500小时/月 |
| 适用场景 | 轻量级应用 | 长期运行服务 |
| 全球CDN | ✅ | ❌ |

### Q: 部署后无法访问怎么办？

**A**: 检查以下几点：
1. 查看 Vercel 部署日志是否有错误
2. 确认所有依赖都在 `requirements-prod.txt` 中
3. 检查 Vercel 函数日志（在项目 → Functions 查看）

### Q: 如何更新部署的应用？

**A**: 非常简单！
```bash
git add .
git commit -m "更新内容"
git push
```
推送到 GitHub 后，Vercel 会自动重新部署。

### Q: 可以使用自定义域名吗？

**A**: 可以！
1. 在 Vercel 项目设置中点击 "Domains"
2. 添加您的域名
3. 按照提示配置 DNS 记录

### Q: 部署到 Vercel 是免费的吗？

**A**: 是的！Vercel 提供免费计划：
- 无限部署
- 100 GB 带宽/月
- 自动 HTTPS
- 全球 CDN

但有函数执行时间限制（10秒）。如果需要更长时间，考虑升级或使用 Railway。

### Q: 数据会持久化吗？

**A**: 不会。Vercel 是无状态的 serverless 平台。
- SQLite 数据库会在每次部署后重置
- 如需持久化数据，考虑：
  - 使用外部数据库（PostgreSQL、MySQL）
  - 使用云存储服务
  - 或改用 Railway 部署

---

## 🎉 部署成功！/ Deployment Success!

现在您可以：
- 📱 在手机浏览器访问 Vercel 域名
- 🌍 分享给全球任何地方的用户
- 🔄 通过 Git Push 自动更新部署
- 📊 在 Vercel 控制台监控应用状态

**提示**: 将域名添加到手机主屏幕，当作 App 使用！

**Tip**: Add the domain to your phone's home screen to use it like an app!

---

## 📚 更多资源 / More Resources

- [Railway 部署指南](RAILWAY_DEPLOYMENT.md) - 另一个部署选择
- [Vercel 官方文档](https://vercel.com/docs)
- [Flask on Vercel](https://vercel.com/docs/frameworks/backend/flask)

---

如有问题，请在 GitHub Issues 中提出！

If you have any questions, please open a GitHub Issue!
