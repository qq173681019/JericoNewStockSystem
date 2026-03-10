# Railway 部署指南

## 项目状态检查

您的项目已经包含了所有必要的部署文件：

- ✅ `app.py` - Flask应用入口点
- ✅ `railway.json` - Railway平台配置
- ✅ `nixpacks.toml` - Nixpacks构建配置  
- ✅ `Procfile` - 启动命令配置
- ✅ `requirements-prod.txt` - 生产环境依赖（已优化）
- ✅ `.railwayignore` - 忽略不需要部署的文件
- ✅ `config/settings.py` - 云环境兼容配置

## 部署步骤

### 方式一：使用Railway网页界面（推荐）

1. **访问 [Railway](https://railway.app/) 并使用 GitHub 账号登录**

2. **点击 "New Project"**

3. **选择 "Deploy from GitHub repo"**

4. **选择您的 `JericoNewStockSystem` 仓库**

5. **在配置页面，确保以下设置正确**：
   - Build Command: `pip install --upgrade pip setuptools wheel && pip install --no-cache-dir -r requirements-prod.txt`
   - Start Command: `gunicorn --bind 0.0.0.0:$PORT --workers 2 --timeout 120 --access-logfile - --error-logfile - app:app`
   - Builder: Nixpacks (这是自动检测的)

6. **点击 "Deploy" 按钮**

### 方式二：使用Railway CLI

如果要使用CLI部署：

1. **安装 Railway CLI**
   ```bash
   npm install -g @railway/cli
   ```

2. **登录 Railway**
   ```bash
   railway login
   ```

3. **初始化并部署**
   ```bash
   cd C:\Users\admin\Documents\GitHub\JericoNewStockSystem
   railway init
   railway up
   ```

## 重要配置说明

### 云环境兼容性
- 项目已配置为在云环境中使用 `/tmp` 目录存储数据（解决文件系统权限问题）
- 使用 Gunicorn 作为生产级 WSGI 服务器

### 依赖优化
- 使用 `requirements-prod.txt`（轻量化版本，移除了matplotlib等大体积包）
- 构建时间已优化，减少部署超时风险

## 故障排除

### 常见错误及解决方案

1. **"No flask entrypoint found" 错误**
   - 确保您部署的是包含 `app.py` 的分支
   - 检查 `app.py` 是否存在并正确导出 Flask app 对象

2. **构建超时错误**
   - 确保使用 `requirements-prod.txt` 而不是 `requirements.txt`
   - 检查 `nixpacks.toml` 配置是否正确

3. **启动失败**
   - 检查日志中是否有 Python 包导入错误
   - 确保所有依赖包在 `requirements-prod.txt` 中定义

### 检查部署状态

部署完成后，访问健康检查端点：
```
https://your-app-name-production.up.railway.app/api/health
```

应返回：
```json
{
  "status": "healthy",
  "service": "SIAPS Web UI",
  "version": "1.0.0"
}
```

## 部署后配置

### 环境变量（可选）
如有需要，可在 Railway 项目的 "Variables" 标签中添加：
- `FLASK_ENV=production`

## 注意事项

- Railway 提供每月 500 小时免费额度
- 重启容器时，保存在 `/tmp` 的数据会丢失
- 如需持久化数据，考虑连接外部数据库服务

## 支持

如果部署仍有问题，请检查：
1. 确认使用的是 `main` 分支
2. 检查构建日志获取详细错误信息
3. 确认所有部署配置文件存在且格式正确