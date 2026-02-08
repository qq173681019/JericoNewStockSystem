# SIAPS 安装与使用指南

## 目录
- [系统要求](#系统要求)
- [安装步骤](#安装步骤)
- [配置指南](#配置指南)
- [快速开始](#快速开始)
- [功能说明](#功能说明)
- [常见问题](#常见问题)

## 系统要求

### 硬件要求
- **CPU**: 双核及以上
- **内存**: 4GB及以上（推荐8GB）
- **硬盘**: 至少2GB可用空间
- **显示**: 1280x800分辨率及以上

### 软件要求
- **操作系统**: 
  - Windows 10/11
  - macOS 10.14+
  - Linux (Ubuntu 20.04+, CentOS 8+)
- **Python**: 3.8, 3.11, 或 3.13
- **pip**: 最新版本

## 安装步骤

### 方式一：从源码安装（推荐开发者）

#### 1. 安装Python
访问 [Python官网](https://www.python.org/downloads/) 下载并安装Python。

验证安装：
```bash
python --version  # 或 python3 --version
pip --version     # 或 pip3 --version
```

#### 2. 克隆仓库
```bash
git clone https://github.com/qq173681019/JericoNewStockSystem.git
cd JericoNewStockSystem
```

#### 3. 创建虚拟环境（推荐）

**Windows**:
```bash
python -m venv venv
venv\Scripts\activate
```

**macOS/Linux**:
```bash
python3 -m venv venv
source venv/bin/activate
```

#### 4. 安装依赖

**基础安装**（最小功能）:
```bash
pip install -r requirements-test.txt
```

**完整安装**（包含机器学习）:
```bash
pip install -r requirements.txt
```

**注意**: 某些依赖如`ta-lib`需要系统级安装：

**Windows**:
1. 下载 [TA-Lib Windows二进制文件](http://www.lfd.uci.edu/~gohlke/pythonlibs/#ta-lib)
2. 安装: `pip install TA_Lib‑0.4.XX‑cpXX‑cpXX‑win_amd64.whl`

**macOS**:
```bash
brew install ta-lib
pip install ta-lib
```

**Linux**:
```bash
sudo apt-get install ta-lib  # Ubuntu/Debian
# 或
sudo yum install ta-lib      # CentOS/RedHat
pip install ta-lib
```

#### 5. 配置环境
```bash
cp .env.example .env
# 编辑 .env 文件（可选）
```

#### 6. 验证安装
```bash
python demo.py
```

如果看到"✓ SIAPS Core Framework Initialized Successfully!"，说明安装成功！

### 方式二：使用pip安装（未来支持）
```bash
# 将来会支持
pip install siaps
```

## 配置指南

### 环境变量配置

编辑 `.env` 文件：

```env
# 应用配置
APP_NAME=SIAPS
DEBUG=True              # 生产环境设为 False
THEME=dark             # 可选: dark, light

# 数据源配置
AKSHARE_ENABLED=True
TUSHARE_ENABLED=False
TUSHARE_TOKEN=         # 从 https://tushare.pro 获取

# 数据库配置
DATABASE_URL=sqlite:///data/siaps.db

# GUI配置
WINDOW_WIDTH=1280
WINDOW_HEIGHT=800

# 日志配置
LOG_LEVEL=INFO         # 可选: DEBUG, INFO, WARNING, ERROR
```

### 数据源配置

#### AKShare（免费，推荐）
- 无需注册
- 自动启用
- 提供基础行情数据

#### TuShare（需注册）
1. 访问 [TuShare Pro](https://tushare.pro)
2. 注册并获取Token
3. 在 `.env` 中配置：
   ```env
   TUSHARE_ENABLED=True
   TUSHARE_TOKEN=your_token_here
   ```

## 快速开始

### 启动应用

```bash
python main.py
```

### 界面导航

应用启动后，您会看到以下界面：

```
┌────────────┬─────────────────────────────────────┐
│  侧边栏    │          主内容区域                  │
│            │                                     │
│  SIAPS     │                                     │
│            │                                     │
│  股票预测  │      [欢迎页面]                      │
│  观测池    │                                     │
│  历史记录  │                                     │
│  设置      │                                     │
│            │                                     │
│  深色模式  │                                     │
└────────────┴─────────────────────────────────────┘
```

## 功能说明

### 1. 股票预测

#### 短期预测（当日）
1. 点击侧边栏"股票预测"
2. 输入6位股票代码（如：000001）
3. 点击"开始预测"
4. 查看预测结果：
   - 涨跌方向
   - 预测价格
   - 置信度
   - 关键时间点

#### 长期预测（3个月）
1. 选择"长期预测"模式
2. 输入股票代码
3. 查看：
   - 目标价位
   - 趋势方向
   - 关键支撑/阻力位

### 2. 观测池管理

**添加股票到观测池**:
1. 点击"观测池"
2. 点击"添加股票"
3. 输入股票信息：
   - 股票代码
   - 目标价格（可选）
   - 止损价格（可选）
   - 止盈价格（可选）
   - 备注（可选）

**监控和预警**:
- 实时价格更新
- 价格触发预警
- 涨跌幅提醒

### 3. 历史记录查询

**查看预测历史**:
1. 点击"历史记录"
2. 选择筛选条件：
   - 股票代码
   - 日期范围
   - 预测类型
3. 查看准确率统计

**导出数据**:
- 导出为CSV
- 导出为Excel

### 4. 系统设置

**可配置项**:
- 数据源选择
- 模型参数
- 预警设置
- 显示偏好

## 常见问题

### Q1: 安装时提示"No module named 'XXX'"

**A**: 依赖包未安装完整，尝试：
```bash
pip install -r requirements.txt --upgrade
```

### Q2: AKShare数据获取失败

**A**: 可能的原因：
1. 网络问题 - 检查网络连接
2. 股票代码错误 - 确认6位数字代码
3. API限流 - 稍后重试

### Q3: GUI无法启动

**A**: 检查：
1. CustomTkinter是否安装：`pip install customtkinter`
2. tkinter是否可用：`python -m tkinter`
3. 查看日志文件：`logs/siaps.log`

### Q4: 数据库文件在哪里？

**A**: 默认位置：
- Linux/Mac: `./data/siaps.db`
- Windows: `.\data\siaps.db`

可通过 `.env` 文件的 `DATABASE_URL` 修改。

### Q5: 如何更新到最新版本？

**A**: 
```bash
git pull origin main
pip install -r requirements.txt --upgrade
```

### Q6: 预测准确吗？

**A**: 
- 本系统使用机器学习模型，准确率受多种因素影响
- 预测仅供参考，不构成投资建议
- 股市有风险，投资需谨慎

### Q7: 可以同时预测多只股票吗？

**A**: 
- Phase 1支持单只股票预测
- Phase 3将支持CSV批量导入和批量预测

### Q8: 支持哪些股票市场？

**A**: 当前支持：
- 上海证券交易所（代码以6开头）
- 深圳证券交易所（代码以0或3开头）

未来计划支持：
- 港股
- 美股

### Q9: 如何卸载？

**A**:
```bash
# 停用虚拟环境
deactivate

# 删除项目文件夹
rm -rf JericoNewStockSystem  # Linux/Mac
# 或手动删除文件夹 (Windows)
```

### Q10: 遇到Bug怎么办？

**A**: 请在GitHub Issues中报告：
1. 访问 [Issues页面](https://github.com/qq173681019/JericoNewStockSystem/issues)
2. 点击"New Issue"
3. 描述问题并附上：
   - 错误信息
   - 操作步骤
   - 系统信息
   - 日志文件（`logs/siaps.log`）

## 获取帮助

- **文档**: [docs/DEVELOPMENT.md](DEVELOPMENT.md)
- **架构**: [docs/ARCHITECTURE.md](ARCHITECTURE.md)
- **GitHub**: [项目主页](https://github.com/qq173681019/JericoNewStockSystem)
- **Issues**: [问题追踪](https://github.com/qq173681019/JericoNewStockSystem/issues)

## 贡献代码

欢迎贡献！请查看 [CONTRIBUTING.md](../CONTRIBUTING.md)

## 许可证

本项目采用 MIT 许可证 - 详见 [LICENSE](../LICENSE)

---

祝您使用愉快！如有问题，欢迎反馈。
