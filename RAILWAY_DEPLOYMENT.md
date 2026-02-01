# Railway 快速部署指南

## 🎯 部署问题已修复！

本项目最近修复了 Railway 部署超时和失败的问题：

### 🔧 修复内容
1. **优化依赖**: 移除了 matplotlib 等耗时的包（构建时间减少 60%+）
2. **添加 nixpacks.toml**: 优化 Railway 构建配置
3. **添加 railway.json**: 配置重启策略
4. **添加 .railwayignore**: 减少上传文件大小
5. **使用 --no-cache-dir**: 减少构建时内存使用

### ⏱️ 预计部署时间
- 首次部署：约 3-5 分钟
- 后续部署：约 2-3 分钟（有缓存）

---

## 🚀 一键部署到 Railway

本项目已经配置好 Railway 部署所需的所有文件，您可以直接部署。

### 📋 部署步骤

#### 1. 准备工作
- 确保您的代码已推送到 GitHub
- 访问 [Railway](https://railway.app/)
- 使用 GitHub 账号登录

#### 2. 创建新项目
1. 点击 "New Project"
2. 选择 "Deploy from GitHub repo"
3. 授权 Railway 访问您的 GitHub 仓库
4. 选择 `JericoNewStockSystem` 仓库

#### 3. 等待部署
- Railway 会自动检测项目配置
- 自动安装依赖（约 3-5 分钟）
- 自动启动应用

#### 4. 生成域名
1. 部署成功后，进入 "Settings" 标签
2. 点击 "Generate Domain"
3. 您会得到一个类似 `your-app-production.up.railway.app` 的域名

#### 5. 访问应用
在浏览器中打开生成的域名，即可访问您的股票分析系统！

### 🎯 项目配置说明

本项目包含以下 Railway 配置文件：

- **`nixpacks.toml`** - Nixpacks 构建配置，优化构建过程
- **`railway.json`** - Railway 平台配置
- **`Procfile`** - 启动命令配置
- **`runtime.txt`** - Python 版本指定 (3.11.7)
- **`requirements-prod.txt`** - 生产环境依赖（已优化）
- **`.railwayignore`** - 忽略不需要部署的文件

### ⚙️ 环境变量（可选）

如果需要配置环境变量，在 Railway 项目的 "Variables" 标签中添加：

```
FLASK_ENV=production
```

其他环境变量会自动设置：
- `PORT` - Railway 自动提供
- `PYTHON_VERSION` - 由 runtime.txt 指定

### 🔧 常见问题

#### Q: 部署超时怎么办？
**A**: 本项目已经优化了依赖安装，移除了 matplotlib 等耗时的包。如果仍然超时：
1. 检查 Railway 服务状态
2. 重新触发部署（点击 "Deploy" 按钮）
3. 查看构建日志排查问题
4. 确保使用的是 `requirements-prod.txt` 而不是 `requirements.txt`

**已知修复**：
- ✅ 移除了 matplotlib（构建时间减少 60%+）
- ✅ 添加了 nixpacks.toml 优化构建配置
- ✅ 使用 --no-cache-dir 减少内存使用
- ✅ 添加了 .railwayignore 减少上传文件

#### Q: 如何查看部署日志？
**A**: 
1. 在 Railway 项目中点击 "Deployments" 标签
2. 点击最新的部署记录
3. 点击 "View Logs" 查看详细日志

#### Q: 如何更新应用？
**A**: 
推送代码到 GitHub 后，Railway 会自动重新部署：
```bash
git add .
git commit -m "更新内容"
git push
```

#### Q: 免费额度够用吗？
**A**: 
Railway 提供每月 500 小时免费额度，对于个人使用完全足够：
- 500 小时 ≈ 20.8 天
- 如果只在需要时使用，可以在不用时暂停服务

#### Q: 如何暂停/重启服务？
**A**:
在 Railway 项目的 "Settings" 中：
- 暂停：不会计费，但无法访问
- 重启：点击 "Restart" 重新启动服务

#### Q: 部署后访问很慢？
**A**:
Railway 服务器在国外，国内访问可能较慢。如果需要更快速度：
- 考虑使用国内云服务器（腾讯云/阿里云）
- 参考 `docs/云端部署指南.md` 的详细说明

### 📱 手机访问

部署成功后，您可以：
1. 在手机浏览器直接访问 Railway 提供的域名
2. 添加到主屏幕（iOS/Android）当作 App 使用
3. 分享给朋友访问（但要注意数据安全）

### 🔒 安全建议

1. **不要在生产环境使用默认密钥**
   - 修改 `run_web_ui.py` 中的 `SECRET_KEY`

2. **考虑添加访问认证**
   - 参考 `docs/云端部署指南.md` 中的认证配置

3. **定期备份数据**
   - Railway 容器重启会丢失数据
   - 重要数据建议使用外部数据库

### 📊 性能优化

如果访问量增大，可以考虑：

1. **使用 Gunicorn**（已在 requirements-prod.txt 中）
   修改 `Procfile`：
   ```
   web: gunicorn -w 4 -b 0.0.0.0:$PORT --timeout 120 run_web_ui:app
   ```

2. **增加 Railway 资源**
   - 升级到 Hobby 计划获得更多资源
   - 提高并发处理能力

### 🎉 部署成功！

现在您可以随时随地访问您的股票分析系统了！

**记得：**
- 📱 将域名添加到手机书签
- 🔖 分享给需要的朋友
- ⭐ 给项目点个 Star 支持一下！

---

更多详细信息请参考：
- [云端部署指南](docs/云端部署指南.md) - 完整的云部署教程
- [手机端访问指南](docs/手机端访问指南.md) - 手机访问的详细说明
- [Railway 官方文档](https://docs.railway.app/)
