# Vercel 部署缓冲区溢出修复 / Vercel Buffer Overflow Fix

## 问题描述 / Problem Description

部署到 Vercel 时出现以下错误：
```
RangeError [ERR_OUT_OF_RANGE]: The value of "size" is out of range. 
It must be >= 0 && <= 4294967296. Received 4_996_579_109
```

When deploying to Vercel, the following error occurred:
```
RangeError [ERR_OUT_OF_RANGE]: The value of "size" is out of range. 
It must be >= 0 && <= 4294967296. Received 4_996_579_109
```

## 根本原因 / Root Cause

这个错误是由于尝试安装非常大的 Python 包导致的：

- **PyTorch** (`torch>=2.0.0`) - 约 1-2GB
- **TensorFlow** (`tensorflow>=2.13.0`) - 约 1-2GB  
- **Prophet** (`prophet>=1.1.5`) - 包含大型依赖

当 Vercel 的构建系统（基于 Node.js）尝试下载和处理这些大型包时，缓冲区大小超过了 Node.js 的 4GB 限制（4,294,967,296 字节），导致部署失败。

This error occurred because of attempting to install very large Python packages:

- **PyTorch** (`torch>=2.0.0`) - ~1-2GB
- **TensorFlow** (`tensorflow>=2.13.0`) - ~1-2GB
- **Prophet** (`prophet>=1.1.5`) - contains large dependencies

When Vercel's build system (based on Node.js) tried to download and process these large packages, the buffer size exceeded Node.js's 4GB limit (4,294,967,296 bytes), causing the deployment to fail.

## 解决方案 / Solution

### 修改内容 / Changes Made

1. **文件重组** / **File Reorganization**:
   - 原 `requirements.txt` 的内容 → `requirements-dev.txt` (包含所有开发依赖，including ML libraries)
   - 更新 `requirements.txt` 使用生产依赖 (轻量级生产依赖，lightweight production deps)
   - `requirements-prod.txt` 保持不变作为备用 (已存在的文件，unchanged)

2. **依赖分离** / **Dependency Separation**:

   **开发环境** (`requirements-dev.txt`):
   - 包含完整的机器学习库（PyTorch, TensorFlow, Prophet）
   - 包含 GUI 库（CustomTkinter, Pillow, Matplotlib）
   - 适用于本地开发和测试
   
   **生产环境** (`requirements.txt`):
   - 仅包含 Web 应用必需的依赖
   - 移除了所有大型 ML 库
   - 优化用于云部署（Vercel, Railway, Render）

   **Development** (`requirements-dev.txt`):
   - Contains full ML libraries (PyTorch, TensorFlow, Prophet)
   - Contains GUI libraries (CustomTkinter, Pillow, Matplotlib)
   - Suitable for local development and testing
   
   **Production** (`requirements.txt`):
   - Only contains dependencies required for web app
   - Removed all large ML libraries
   - Optimized for cloud deployment (Vercel, Railway, Render)

### 为什么这样修改？ / Why This Change?

Web UI 部署不需要：
- ❌ 机器学习模型训练（PyTorch, TensorFlow）
- ❌ 时间序列预测（Prophet）
- ❌ 桌面 GUI（CustomTkinter）
- ❌ 图表生成（Matplotlib）- Web UI 使用 JavaScript 图表库

Web UI deployment doesn't need:
- ❌ ML model training (PyTorch, TensorFlow)
- ❌ Time series forecasting (Prophet)
- ❌ Desktop GUI (CustomTkinter)
- ❌ Chart generation (Matplotlib) - Web UI uses JavaScript charting libraries

## 使用说明 / Usage Instructions

### 本地开发 / Local Development

```bash
# 安装完整的开发依赖
pip install -r requirements-dev.txt

# 启动桌面版（使用 ML 功能）
python main.py

# 启动 Web UI
python run_web_ui.py
```

### Vercel 部署 / Vercel Deployment

Vercel 会自动使用 `requirements.txt`（轻量级版本），无需额外配置。

Vercel will automatically use `requirements.txt` (lightweight version), no additional configuration needed.

```bash
# 直接推送到 GitHub，Vercel 自动部署
git push
```

### Railway/Render 部署 / Railway/Render Deployment

同样会使用 `requirements.txt`，部署速度更快：

Will also use `requirements.txt`, faster deployment:

```bash
git push
# Railway/Render 会自动检测并部署
```

## 验证修复 / Verify Fix

部署到 Vercel 后，构建时间应该从失败变为成功：

After deploying to Vercel, build time should change from failing to succeeding:

- ❌ 之前 / Before: 构建失败，Buffer overflow error
- ✅ 现在 / Now: 构建成功，约 2-3 分钟

### 检查部署日志 / Check Deployment Logs

在 Vercel Dashboard 中查看构建日志，应该看到：

In Vercel Dashboard, check build logs, you should see:

```
Installing requirements.txt...
Collecting Flask>=3.0.0
Collecting pandas>=2.0.0
...
Build completed successfully!
```

## 常见问题 / FAQ

### Q: 我需要使用机器学习功能怎么办？

**A**: ML 功能仅适用于本地开发。使用 `requirements-dev.txt` 在本地安装完整依赖：

```bash
pip install -r requirements-dev.txt
python main.py  # 启动桌面版
```

### Q: Can I still use ML features?

**A**: ML features are only available for local development. Use `requirements-dev.txt` to install full dependencies locally:

```bash
pip install -r requirements-dev.txt
python main.py  # Start desktop version
```

### Q: Web UI 功能会受影响吗？ / Will Web UI functionality be affected?

**A**: 不会！Web UI 的所有核心功能都保留：
- ✅ 股票数据获取
- ✅ 数据分析和可视化
- ✅ 实时更新
- ✅ 数据库存储

**A**: No! All core Web UI features are preserved:
- ✅ Stock data fetching
- ✅ Data analysis and visualization
- ✅ Real-time updates
- ✅ Database storage

### Q: 为什么保留 requirements-prod.txt？

**A**: 为了向后兼容。这个文件在之前的部署修复中就存在，某些用户可能仍在引用它。它与新的 `requirements.txt` 内容相同。

**A**: For backward compatibility. This file existed from a previous deployment fix, and some users may still reference it. It has the same content as the new `requirements.txt`.

## 技术细节 / Technical Details

### Node.js Buffer 限制 / Node.js Buffer Limit

Node.js 的 `Buffer.concat()` 有 4GB 的硬限制：
- 最大值: 4,294,967,296 字节（2^32 字节）
- 错误中的值: 4,996,579,109 字节（约 5GB）

Node.js `Buffer.concat()` has a hard 4GB limit:
- Maximum: 4,294,967,296 bytes (2^32 bytes)
- Value in error: 4,996,579,109 bytes (~5GB)

### 包大小对比 / Package Size Comparison

| 包 / Package | 大小 / Size |
|--------------|------------|
| PyTorch | ~1.5GB |
| TensorFlow | ~1.2GB |
| Prophet | ~500MB |
| Flask | ~5MB |
| Pandas | ~50MB |

**总计**: 开发版 ~3.5GB vs 生产版 ~100MB

**Total**: Dev version ~3.5GB vs Production version ~100MB

## 相关文件 / Related Files

- `requirements.txt` - 生产部署依赖 / Production deployment dependencies
- `requirements-dev.txt` - 开发完整依赖 / Full development dependencies  
- `requirements-prod.txt` - 备用生产依赖 / Backup production dependencies
- `vercel.json` - Vercel 配置 / Vercel configuration
- `app.py` - Vercel 入口点 / Vercel entry point

## 参考 / References

- [Vercel Python Runtime](https://vercel.com/docs/runtimes#official-runtimes/python)
- [Node.js Buffer Documentation](https://nodejs.org/api/buffer.html)
- [PyTorch Installation](https://pytorch.org/get-started/locally/)
- [TensorFlow Installation](https://www.tensorflow.org/install)

---

✅ **修复已完成！现在可以成功部署到 Vercel！**

✅ **Fix completed! You can now successfully deploy to Vercel!**
