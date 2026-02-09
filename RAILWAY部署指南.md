# Railway 部署指南 🚂

## 📋 准备工作

本项目已完全配置好Railway部署，可以一键部署！

### ✅ 已配置的文件

1. **railway.json** - Railway配置文件
2. **requirements-prod.txt** - 生产环境依赖（已优化）
3. **nixpacks.toml** - Nixpacks构建配置
4. **Procfile** - 进程配置（备用）
5. **runtime.txt** - Python版本指定
6. **app.py** - 应用入口

### 📦 依赖大小

**生产环境依赖** (requirements-prod.txt):
```
Flask + gunicorn:    ~20MB
pandas + numpy:      ~100MB
scikit-learn:        ~100MB
akshare:            ~30MB
其他:               ~20MB
---------------------------------
总计:               ~270MB
```

**Railway优势**:
- ✅ 支持更大的构建（无4GB限制）
- ✅ 优秀的Python支持
- ✅ 自动检测配置文件
- ✅ 免费额度：$5/月，500小时运行时间

## 🚀 部署步骤

### 方法1: 通过GitHub连接（推荐）

#### 1. 注册Railway账号

访问 [Railway.app](https://railway.app/) 并注册：
- 可以使用GitHub账号直接登录
- 免费账号提供$5月度额度

#### 2. 创建新项目

1. 点击 **"New Project"**
2. 选择 **"Deploy from GitHub repo"**
3. 如果是第一次，需要授权Railway访问GitHub
4. 选择你的仓库 `qq173681019/JericoNewStockSystem`
5. 选择分支（如 `copilot/improve-price-forecast-algorithm` 或 `main`）

#### 3. Railway自动配置

Railway会自动：
- ✅ 检测到 `railway.json` 配置
- ✅ 使用 `nixpacks.toml` 构建设置
- ✅ 安装 `requirements-prod.txt` 依赖
- ✅ 使用 `app.py` 作为入口
- ✅ 自动分配域名和端口

#### 4. 等待部署完成

- 构建时间: 约3-5分钟
- 查看实时日志了解构建进度
- 看到 "Deployed" 状态即表示成功

#### 5. 访问应用

Railway会自动生成一个域名，如：
```
https://your-app-name.up.railway.app
```

### 方法2: 使用Railway CLI

#### 1. 安装Railway CLI

**macOS/Linux**:
```bash
sh -c "$(curl -fsSL https://railway.app/install.sh)"
```

**Windows** (PowerShell):
```powershell
iwr https://railway.app/install.ps1 | iex
```

#### 2. 登录Railway

```bash
railway login
```

#### 3. 初始化项目

在项目目录中：
```bash
cd /path/to/JericoNewStockSystem
railway init
```

选择 "Create a new project"

#### 4. 部署

```bash
railway up
```

#### 5. 查看日志

```bash
railway logs
```

#### 6. 获取URL

```bash
railway open
```

## 🔧 配置说明

### railway.json 配置

```json
{
  "build": {
    "builder": "NIXPACKS",
    "buildCommand": "pip install --upgrade pip setuptools wheel && pip install --no-cache-dir -r requirements-prod.txt"
  },
  "deploy": {
    "startCommand": "gunicorn --bind 0.0.0.0:$PORT --workers 2 --threads 4 --timeout 120 app:app",
    "restartPolicyType": "ON_FAILURE",
    "restartPolicyMaxRetries": 10,
    "healthcheckPath": "/",
    "healthcheckTimeout": 100
  }
}
```

**配置说明**:
- `builder: NIXPACKS`: 使用Nixpacks构建系统
- `--workers 2`: 2个工作进程（适合免费层）
- `--threads 4`: 每个进程4个线程
- `--timeout 120`: 120秒超时（处理长时间预测）
- `healthcheckPath: /`: 健康检查路径
- `restartPolicyType: ON_FAILURE`: 失败时自动重启

### 环境变量（可选）

在Railway控制台可以添加环境变量：

**推荐设置**:
```
PORT=8080                    # Railway自动设置
PYTHONUNBUFFERED=1          # 实时日志输出
WEB_CONCURRENCY=2           # 工作进程数
```

**可选设置**（如需使用数据库）:
```
DATABASE_URL=postgresql://... # 数据库连接
SECRET_KEY=your-secret-key    # Flask密钥
```

## 📊 监控和管理

### 查看日志

在Railway控制台：
1. 进入你的项目
2. 点击 "View Logs"
3. 实时查看应用日志

### 性能监控

Railway提供：
- ✅ CPU使用率
- ✅ 内存使用
- ✅ 网络流量
- ✅ 请求数量

### 重新部署

**方法1**: 推送代码到GitHub
- 每次推送，Railway自动重新部署

**方法2**: 手动触发
- Railway控制台 → "Deploy" → "Redeploy"

**方法3**: 使用CLI
```bash
railway up --detach
```

## 🔍 故障排查

### 构建失败

**查看构建日志**:
```bash
railway logs --deployment
```

**常见问题**:

1. **依赖安装失败**
   ```
   错误: Could not find a version that satisfies...
   ```
   解决: 检查 `requirements-prod.txt` 版本号

2. **内存不足**
   ```
   错误: Killed (out of memory)
   ```
   解决: 减少 `--workers` 数量到1

3. **超时**
   ```
   错误: Build timeout
   ```
   解决: 增加 `--timeout` 值

### 运行时错误

**查看应用日志**:
```bash
railway logs
```

**常见问题**:

1. **端口绑定错误**
   ```
   错误: Address already in use
   ```
   解决: 确保使用 `$PORT` 环境变量

2. **模块导入错误**
   ```
   错误: ModuleNotFoundError
   ```
   解决: 检查依赖是否在 `requirements-prod.txt`

3. **API错误**
   ```
   错误: 500 Internal Server Error
   ```
   解决: 查看详细日志，检查数据源连接

## 💰 费用说明

### 免费层

**每月免费额度**:
- $5 信用额度
- 约500小时运行时间
- 共享CPU和内存
- 无需信用卡

**适合**:
- 开发和测试
- 小流量应用
- 个人项目

### 付费层（可选）

**Hobby Plan** ($5/月):
- $5 额外信用额度
- 优先资源
- 更稳定的性能

**Pro Plan** ($20/月):
- $20 信用额度
- 专用资源
- 更高并发支持

## 🎯 性能优化

### 1. 调整Worker数量

根据Railway的内存限制：

**免费层** (512MB):
```json
"startCommand": "gunicorn --bind 0.0.0.0:$PORT --workers 1 --threads 4 ..."
```

**付费层** (1GB+):
```json
"startCommand": "gunicorn --bind 0.0.0.0:$PORT --workers 2 --threads 4 ..."
```

### 2. 启用缓存

在代码中添加缓存机制：
```python
from functools import lru_cache

@lru_cache(maxsize=100)
def get_stock_data(code):
    # 缓存股票数据
    pass
```

### 3. 数据库优化（如使用）

使用Railway提供的PostgreSQL：
1. Railway控制台 → "New" → "Database" → "PostgreSQL"
2. 自动获得 `DATABASE_URL` 环境变量
3. 在代码中使用连接池

## 📱 自定义域名

### 添加自定义域名

1. Railway控制台 → "Settings" → "Domains"
2. 点击 "Add Custom Domain"
3. 输入你的域名（如 `stock.example.com`）
4. 按照提示配置DNS：
   ```
   CNAME stock.example.com → your-app.up.railway.app
   ```
5. 等待DNS生效（通常5-30分钟）

## 🔐 安全建议

### 1. 环境变量

敏感信息使用环境变量：
```python
import os
SECRET_KEY = os.environ.get('SECRET_KEY', 'default-dev-key')
DATABASE_URL = os.environ.get('DATABASE_URL')
```

### 2. HTTPS

Railway自动提供HTTPS证书，无需额外配置

### 3. CORS配置

已在 `run_web_ui.py` 中配置：
```python
from flask_cors import CORS
CORS(app)
```

## ✅ 部署检查清单

部署前确认：

- [ ] 代码已推送到GitHub
- [ ] `requirements-prod.txt` 包含所有依赖
- [ ] `railway.json` 配置正确
- [ ] `app.py` 存在并可导入
- [ ] 本地测试通过

部署后验证：

- [ ] 应用成功启动（查看日志）
- [ ] 主页可以访问
- [ ] API端点正常工作
- [ ] 预测功能正常
- [ ] 没有明显错误日志

## 🎉 部署完成

恭喜！你的股票预测系统现已部署到Railway！

**访问应用**:
```
https://your-app-name.up.railway.app
```

**测试API**:
```bash
# 测试主页
curl https://your-app-name.up.railway.app

# 测试30分钟预测
curl https://your-app-name.up.railway.app/api/predict/multi/000001?timeframe=30min

# 测试1天预测
curl https://your-app-name.up.railway.app/api/predict/multi/000001?timeframe=1day
```

## 📚 相关文档

- [Railway官方文档](https://docs.railway.app/)
- [Nixpacks文档](https://nixpacks.com/)
- [Gunicorn文档](https://docs.gunicorn.org/)

## 💬 获取帮助

**遇到问题？**

1. 查看Railway控制台日志
2. 参考本文档的故障排查部分
3. 查看 `修改确认和部署问题说明.md`
4. 访问Railway社区论坛

---

**祝部署顺利！** 🚀
