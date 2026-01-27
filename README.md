# SIAPS - 股票智能分析预测系统

[![Python](https://img.shields.io/badge/Python-3.8%2B-blue.svg)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

**Stock Intelligent Analysis & Prediction System (SIAPS)** - 一个基于机器学习和深度学习的股票分析预测系统。

## 📋 项目概述

SIAPS是一个功能强大的股票智能分析预测系统，通过多维度数据分析提供短期(1天)和中长期(3个月)股票走势预测，并给出具体交易建议。

### 核心功能

- 🔮 **短期走势预测**: 当日涨跌预测、波动幅度、关键时间点
- 📈 **中长期走势预测**: 未来3个月目标价位、趋势方向
- 💡 **智能交易建议**: 板块热度分析、筹码健康度评估、T+0操作建议
- 📊 **技术指标分析**: MA、MACD、RSI、布林带等
- 📝 **历史记录管理**: 预测历史存储与查询、准确率统计
- 👁️ **观测池管理**: 自定义观察列表、价格监控和预警

## 🏗️ 项目结构

```
JericoNewStockSystem/
├── config/                 # 配置模块
│   ├── __init__.py
│   └── settings.py        # 应用配置
├── src/                    # 源代码
│   ├── data_acquisition/  # 数据获取层
│   │   ├── __init__.py
│   │   └── fetcher.py     # 数据获取器
│   ├── data_processing/   # 数据处理层
│   ├── prediction_models/ # 预测模型层
│   ├── business_logic/    # 业务逻辑层
│   ├── gui/               # GUI界面层
│   │   ├── __init__.py
│   │   └── main_window.py # 主窗口
│   ├── database/          # 数据库模块
│   │   ├── __init__.py
│   │   └── models.py      # 数据模型
│   └── utils/             # 工具模块
│       ├── __init__.py
│       └── logger.py      # 日志工具
├── tests/                 # 测试文件
├── docs/                  # 文档
├── data/                  # 数据目录（自动创建）
├── logs/                  # 日志目录（自动创建）
├── models/                # 模型目录（自动创建）
├── main.py               # 主程序入口
├── requirements.txt      # 依赖包列表
├── setup.py             # 安装脚本
└── README.md            # 项目说明

```

## 🚀 快速开始

### 环境要求

- Python 3.8+ / 3.11+ / 3.13+
- pip 或 conda 包管理器

### 安装步骤

1. **克隆仓库**
```bash
git clone https://github.com/qq173681019/JericoNewStockSystem.git
cd JericoNewStockSystem
```

2. **创建虚拟环境**（推荐）
```bash
# 使用 venv
python -m venv venv
source venv/bin/activate  # Linux/Mac
# 或
venv\Scripts\activate     # Windows

# 使用 conda
conda create -n siaps python=3.11
conda activate siaps
```

3. **安装依赖**
```bash
pip install -r requirements.txt
```

4. **配置环境变量**
```bash
cp .env.example .env
# 编辑 .env 文件，配置必要的参数
```

5. **运行应用**
```bash
python main.py
```

## 🔧 技术架构

### 系统分层

1. **表示层**: CustomTkinter GUI框架
2. **业务逻辑层**: 预测引擎 + 交易建议引擎
3. **数据处理层**: 特征工程 + 数据清洗
4. **数据获取层**: AKShare、TuShare等多源API
5. **数据存储层**: SQLite数据库

### 核心技术栈

- **GUI框架**: CustomTkinter
- **数据获取**: AKShare, TuShare
- **数据处理**: Pandas, NumPy
- **机器学习**: Scikit-learn
- **深度学习**: PyTorch, TensorFlow
- **时序分析**: Prophet
- **技术分析**: TA-Lib
- **数据库**: SQLAlchemy + SQLite

## 📖 使用指南

### 基本操作

1. **股票预测**
   - 在主界面输入股票代码（如：000001）
   - 点击"开始预测"按钮
   - 查看预测结果和交易建议

2. **观测池管理**
   - 添加关注的股票到观测池
   - 设置目标价格、止损止盈价格
   - 启用价格监控和预警

3. **历史记录查询**
   - 查看历史预测记录
   - 分析预测准确率
   - 导出数据报告

## 🎯 开发路线图

### Phase 1: 基础框架搭建 ✅
- [x] 项目结构创建
- [x] 基础配置和日志系统
- [x] 数据库模型设计
- [x] GUI框架搭建
- [x] 数据获取模块

### Phase 2: 核心预测功能（进行中）
- [ ] 技术指标计算模块
- [ ] LSTM时序预测模型
- [ ] XGBoost分类模型
- [ ] 交易建议生成器

### Phase 3: 高级功能
- [ ] Transformer长期预测
- [ ] 观测池与预警系统
- [ ] 批量处理功能
- [ ] 历史记录分析

### Phase 4: 优化与部署
- [ ] 性能优化
- [ ] 打包发布
- [ ] 用户手册

## 🤝 贡献指南

欢迎贡献代码、报告问题或提出建议！

1. Fork 本仓库
2. 创建特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 开启 Pull Request

## 📄 许可证

本项目采用 MIT 许可证 - 详见 [LICENSE](LICENSE) 文件

## 📧 联系方式

- 项目主页: [https://github.com/qq173681019/JericoNewStockSystem](https://github.com/qq173681019/JericoNewStockSystem)
- Issue Tracker: [https://github.com/qq173681019/JericoNewStockSystem/issues](https://github.com/qq173681019/JericoNewStockSystem/issues)

## 🙏 致谢

本项目参考了以下优秀开源项目：
- [Qlib (Microsoft)](https://github.com/microsoft/qlib)
- [FinRL (AI4Finance)](https://github.com/AI4Finance-Foundation/FinRL)
- [AlphaNet (Microsoft)](https://github.com/microsoft/AlphaNet)
- [TFT (Google Research)](https://github.com/google-research/google-research/tree/master/tft)

---

⭐ 如果这个项目对你有帮助，请给它一个星标！