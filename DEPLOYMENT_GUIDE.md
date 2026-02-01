# 🚀 部署指南 / Deployment Guide

> **重要提示**: 本项目已针对 Railway 和 Vercel 部署进行了优化配置。按照本指南操作即可成功部署。

> **Important**: This project is optimized for Railway and Vercel deployment. Follow this guide for successful deployment.

---

## 📋 目录 / Table of Contents

1. [快速开始](#快速开始--quick-start)
2. [部署到 Railway](#部署到-railway)
3. [部署到 Vercel](#部署到-vercel)
4. [环境变量配置](#环境变量配置--environment-variables)
5. [常见问题](#常见问题--troubleshooting)

---

## 🚀 快速开始 / Quick Start

### 前提条件 / Prerequisites

- GitHub 账号 / GitHub account
- Railway 或 Vercel 账号 / Railway or Vercel account
- 本项目的 GitHub 仓库 / This project's GitHub repository

---

## 🚂 部署到 Railway

Railway 是推荐的部署平台，因为它：
- ✅ 支持持久化存储（数据库）
- ✅ 提供更长的构建时间
- ✅ 支持 WebSocket 和长连接
- ✅ 更适合数据密集型应用

Railway is the recommended platform because it:
- ✅ Supports persistent storage (database)
- ✅ Provides longer build times
- ✅ Supports WebSocket and long connections
- ✅ Better for data-intensive applications

### 步骤 1：连接到 Railway / Step 1: Connect to Railway

1. 访问 [Railway](https://railway.app/) 并登录
2. 点击 **"New Project"**
3. 选择 **"Deploy from GitHub repo"**
4. 授权 Railway 访问您的 GitHub 账号
5. 选择 `JericoNewStockSystem` 仓库

### 步骤 2：配置项目 / Step 2: Configure Project

Railway 会自动检测项目配置文件：
- ✅ `railway.json` - Railway 特定配置
- ✅ `nixpacks.toml` - 构建配置
- ✅ `Procfile` - 启动命令（备用）

Railway will automatically detect configuration files:
- ✅ `railway.json` - Railway specific configuration
- ✅ `nixpacks.toml` - Build configuration
- ✅ `Procfile` - Start command (fallback)

**不需要手动配置！项目已预配置。**

**No manual configuration needed! Project is pre-configured.**

### 步骤 3：设置环境变量（可选）/ Step 3: Set Environment Variables (Optional)

在 Railway Dashboard 中：
1. 选择您的项目
2. 点击 **"Variables"** 标签
3. 添加以下环境变量（如果需要）：

In Railway Dashboard:
1. Select your project
2. Click **"Variables"** tab
3. Add the following environment variables (if needed):

```bash
# 可选环境变量 / Optional Environment Variables
DEBUG=False
LOG_LEVEL=INFO
```

### 步骤 4：部署 / Step 4: Deploy

1. Railway 会自动开始构建和部署
2. 等待部署完成（大约 2-5 分钟）
3. 部署成功后，Railway 会提供一个公开 URL

1. Railway will automatically start building and deploying
2. Wait for deployment to complete (about 2-5 minutes)
3. After successful deployment, Railway provides a public URL

### 步骤 5：访问应用 / Step 5: Access Application

1. 在 Railway Dashboard 中找到您的项目
2. 点击 **"Settings"** → **"Networking"**
3. 点击生成的 URL 或配置自定义域名

1. Find your project in Railway Dashboard
2. Click **"Settings"** → **"Networking"**
3. Click the generated URL or configure a custom domain

---

## ☁️ 部署到 Vercel

Vercel 适合轻量级部署，但有一些限制：
- ⚠️ Serverless 函数有 10 秒超时限制
- ⚠️ 没有持久化存储（每次请求重新创建数据库）
- ⚠️ 不适合数据密集型操作
- ✅ 部署速度快
- ✅ 适合演示和测试

Vercel is suitable for lightweight deployments, but has limitations:
- ⚠️ Serverless functions have 10-second timeout
- ⚠️ No persistent storage (database recreated per request)
- ⚠️ Not suitable for data-intensive operations
- ✅ Fast deployment
- ✅ Good for demos and testing

### 方法 1：一键部署 / Method 1: One-Click Deploy

点击下面的按钮：

Click the button below:

[![Deploy with Vercel](https://vercel.com/button)](https://vercel.com/new/clone?repository-url=https://github.com/qq173681019/JericoNewStockSystem)

### 方法 2：从 Dashboard 部署 / Method 2: Deploy from Dashboard

#### 步骤 1：导入项目 / Step 1: Import Project

1. 访问 [Vercel Dashboard](https://vercel.com/dashboard)
2. 点击 **"Add New..."** → **"Project"**
3. 选择 **"Import Git Repository"**
4. 选择 `JericoNewStockSystem` 仓库
5. 点击 **"Import"**

#### 步骤 2：配置构建设置 / Step 2: Configure Build Settings

Vercel 会自动检测项目配置：
- ✅ `vercel.json` - 构建和路由配置
- ✅ `app.py` - Flask 应用入口点
- ✅ `requirements-prod.txt` - Python 依赖

Vercel will automatically detect project configuration:
- ✅ `vercel.json` - Build and routing configuration
- ✅ `app.py` - Flask application entry point
- ✅ `requirements-prod.txt` - Python dependencies

**不需要手动配置！** / **No manual configuration needed!**

#### 步骤 3：部署 / Step 3: Deploy

1. 点击 **"Deploy"**
2. 等待构建完成（大约 1-3 分钟）
3. 部署成功后访问提供的 URL

1. Click **"Deploy"**
2. Wait for build to complete (about 1-3 minutes)
3. Visit the provided URL after successful deployment

---

## 🔧 环境变量配置 / Environment Variables

### Railway 环境变量 / Railway Environment Variables

在 Railway 中不需要配置以下变量，因为它们会自动设置：

The following variables don't need to be configured in Railway as they are set automatically:

- `PORT` - 自动由 Railway 设置 / Automatically set by Railway
- `RAILWAY_ENVIRONMENT` - 自动设置为 "production" / Automatically set to "production"

### 可选环境变量 / Optional Environment Variables

您可以根据需要配置以下变量：

You can configure the following variables as needed:

| 变量名 / Variable | 默认值 / Default | 说明 / Description |
|-------------------|------------------|-------------------|
| `DEBUG` | `False` | 调试模式 / Debug mode |
| `LOG_LEVEL` | `INFO` | 日志级别 / Log level |
| `TUSHARE_TOKEN` | (空) | TuShare API 令牌 / TuShare API token |

### 设置环境变量 / Setting Environment Variables

**Railway:**
1. Dashboard → 选择项目 / Select project → Variables
2. 添加变量 / Add variable

**Vercel:**
1. Dashboard → 选择项目 / Select project → Settings → Environment Variables
2. 添加变量 / Add variable
3. 重新部署以应用更改 / Redeploy to apply changes

---

## ❓ 常见问题 / Troubleshooting

### 问题 1：构建超时 / Issue 1: Build Timeout

**症状 / Symptom:**
```
Build exceeded maximum time limit
```

**解决方案 / Solution:**
- 项目已使用 `requirements-prod.txt`，移除了重型 ML 库
- 确保使用的是 `requirements-prod.txt` 而不是 `requirements.txt`

- Project uses `requirements-prod.txt` with heavy ML libraries removed
- Ensure using `requirements-prod.txt` instead of `requirements.txt`

### 问题 2：应用启动失败 / Issue 2: Application Start Failure

**症状 / Symptom:**
```
Sandbox exited with unexpected code: {"code":1,"signal":null}
```

**解决方案 / Solution:**
1. 检查部署日志以获取详细错误信息
2. 确保所有依赖都在 `requirements-prod.txt` 中
3. 验证 Python 版本兼容性（需要 Python 3.11+）

1. Check deployment logs for detailed error messages
2. Ensure all dependencies are in `requirements-prod.txt`
3. Verify Python version compatibility (requires Python 3.11+)

### 问题 3：数据库错误 / Issue 3: Database Errors

**症状 / Symptom:**
```
sqlite3.OperationalError: unable to open database file
```

**解决方案 / Solution:**
- 已修复！项目现在在云环境中使用 `/tmp` 目录
- Railway: 数据会在重启时重置（临时存储）
- Vercel: 每次请求都会重新创建数据库（无状态）

- Fixed! Project now uses `/tmp` directory in cloud environments
- Railway: Data resets on restart (temporary storage)
- Vercel: Database recreated per request (stateless)

### 问题 4：502 Bad Gateway

**症状 / Symptom:**
应用部署成功但访问时显示 502 错误

Application deployed successfully but shows 502 error when accessing

**解决方案 / Solution:**
1. 检查应用是否正在监听正确的端口（`$PORT` 环境变量）
2. 确保 gunicorn 配置正确
3. 查看应用日志以获取详细信息

1. Check if app is listening on correct port (`$PORT` environment variable)
2. Ensure gunicorn is configured correctly
3. Check application logs for details

### 问题 5：Vercel 函数超时 / Issue 5: Vercel Function Timeout

**症状 / Symptom:**
```
Task timed out after 10.00 seconds
```

**解决方案 / Solution:**
- Vercel 免费计划有 10 秒超时限制
- 考虑使用 Railway 进行数据密集型操作
- 优化数据获取和处理逻辑

- Vercel free plan has 10-second timeout limit
- Consider using Railway for data-intensive operations
- Optimize data fetching and processing logic

---

## 📊 部署检查清单 / Deployment Checklist

部署前请确认：

Before deploying, confirm:

- [ ] ✅ 代码已推送到 GitHub / Code pushed to GitHub
- [ ] ✅ 选择了正确的部署平台（Railway 推荐）/ Selected correct platform (Railway recommended)
- [ ] ✅ 已配置必要的环境变量 / Configured necessary environment variables
- [ ] ✅ 查看了部署日志 / Reviewed deployment logs
- [ ] ✅ 测试了部署的应用 / Tested deployed application

---

## 🎉 成功部署后 / After Successful Deployment

部署成功后，您应该能够：

After successful deployment, you should be able to:

1. ✅ 访问 Web UI
2. ✅ 查询股票信息
3. ✅ 查看历史记录
4. ✅ 使用预测功能

访问应用的健康检查端点以确认运行状态：

Visit the health check endpoint to confirm running status:

```
https://your-app-url.com/api/health
```

应该返回：

Should return:

```json
{
  "status": "healthy",
  "service": "SIAPS Web UI",
  "version": "1.0.0"
}
```

---

## 📞 获取帮助 / Get Help

如果遇到问题，请：

If you encounter issues, please:

1. 查看部署日志以获取详细错误信息 / Check deployment logs for detailed error messages
2. 在 GitHub Issues 中搜索类似问题 / Search for similar issues in GitHub Issues
3. 创建新的 Issue 并提供：
   - 部署平台（Railway/Vercel）/ Deployment platform (Railway/Vercel)
   - 错误日志截图 / Screenshot of error logs
   - 详细的错误描述 / Detailed error description

---

## 🔗 有用的链接 / Useful Links

- [Railway 文档](https://docs.railway.app/)
- [Vercel 文档](https://vercel.com/docs)
- [Flask 部署指南](https://flask.palletsprojects.com/en/latest/deploying/)
- [Gunicorn 文档](https://docs.gunicorn.org/)

---

**祝您部署顺利！🚀**

**Happy Deploying! 🚀**
