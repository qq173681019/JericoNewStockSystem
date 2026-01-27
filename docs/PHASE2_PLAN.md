# SIAPS Phase 2 Implementation Plan

## 项目状态: 🚀 Phase 2 计划中

**规划日期**: 2026-01-27  
**目标版本**: v0.2.0  
**预计完成时间**: TBD

---

## 📋 Phase 2 概述

Phase 2 将实现 SIAPS 的核心预测功能，包括技术指标计算、机器学习模型和交易建议生成器。

### 主要目标

1. **技术指标模块** - 实现常用技术分析指标
2. **时序预测模型** - 使用 LSTM/GRU 进行短期预测
3. **分类模型** - 使用 XGBoost 进行趋势分类
4. **交易建议引擎** - 生成具体的买卖建议

---

## 🎯 Phase 2 功能清单

### 1. 技术指标计算模块 (`src/data_processing/`)

#### 1.1 基础指标
- [ ] **移动平均线 (MA)**
  - Simple Moving Average (SMA)
  - Exponential Moving Average (EMA)
  - Weighted Moving Average (WMA)
  
- [ ] **趋势指标**
  - MACD (Moving Average Convergence Divergence)
  - DMI (Directional Movement Index)
  - ADX (Average Directional Index)
  
- [ ] **动量指标**
  - RSI (Relative Strength Index)
  - Stochastic Oscillator
  - Williams %R
  - CCI (Commodity Channel Index)

- [ ] **波动率指标**
  - Bollinger Bands
  - ATR (Average True Range)
  - Standard Deviation

- [ ] **成交量指标**
  - OBV (On-Balance Volume)
  - Volume Weighted Average Price (VWAP)
  - Accumulation/Distribution Line

#### 1.2 技术指标计算器类
```python
class TechnicalIndicators:
    """技术指标计算器"""
    
    def calculate_ma(self, data, period, ma_type='SMA'):
    def calculate_macd(self, data, fast=12, slow=26, signal=9):
    def calculate_rsi(self, data, period=14):
    def calculate_bollinger_bands(self, data, period=20, std=2):
    def calculate_all_indicators(self, data):
```

#### 1.3 数据预处理
- [ ] 数据清洗（缺失值处理、异常值检测）
- [ ] 特征工程（时间特征、价格特征、技术特征）
- [ ] 数据标准化/归一化
- [ ] 时间序列数据窗口化

---

### 2. 预测模型模块 (`src/prediction_models/`)

#### 2.1 LSTM 短期预测模型
- [ ] **模型架构**
  - Multi-layer LSTM
  - Bidirectional LSTM (可选)
  - Dropout layers for regularization
  
- [ ] **训练流程**
  - 数据集划分（训练/验证/测试）
  - 超参数配置
  - 模型训练与验证
  - 模型保存与加载
  
- [ ] **预测功能**
  - 单日价格预测
  - 多日价格预测（可选）
  - 置信区间估计

#### 2.2 XGBoost 分类模型
- [ ] **特征工程**
  - 技术指标特征
  - 价格变化特征
  - 成交量特征
  
- [ ] **模型训练**
  - 三分类（上涨/下跌/横盘）
  - 超参数调优
  - 交叉验证
  
- [ ] **预测输出**
  - 趋势方向
  - 预测概率
  - 特征重要性

#### 2.3 模型评估
- [ ] 回归指标（LSTM）
  - MAE, MSE, RMSE
  - MAPE (Mean Absolute Percentage Error)
  - R² Score
  
- [ ] 分类指标（XGBoost）
  - Accuracy, Precision, Recall, F1-Score
  - Confusion Matrix
  - ROC Curve & AUC

---

### 3. 业务逻辑模块 (`src/business_logic/`)

#### 3.1 预测引擎
```python
class PredictionEngine:
    """预测引擎 - 整合多个模型"""
    
    def predict_short_term(self, stock_code) -> ShortTermPrediction:
    def predict_long_term(self, stock_code) -> LongTermPrediction:
    def get_ensemble_prediction(self, stock_code) -> EnsemblePrediction:
```

**短期预测 (1天)**
- [ ] LSTM 价格预测
- [ ] XGBoost 趋势分类
- [ ] 技术指标信号
- [ ] 置信度评分

**长期预测 (3个月)**
- [ ] 趋势方向判断
- [ ] 目标价位估算
- [ ] 风险评估

#### 3.2 交易建议生成器
```python
class TradingRecommendation:
    """交易建议生成器"""
    
    def generate_recommendation(self, prediction) -> TradingAdvice:
    def calculate_entry_exit_points(self, stock_data) -> EntryExitPoints:
    def assess_risk(self, stock_code) -> RiskAssessment:
```

**功能实现**
- [ ] **入场建议**
  - 买入时机识别
  - 建议买入价格
  - 仓位建议
  
- [ ] **出场建议**
  - 止损价格计算
  - 止盈价格计算
  - 风险收益比评估
  
- [ ] **风险评估**
  - 波动率分析
  - 最大回撤预估
  - 风险等级评分

#### 3.3 结果聚合器
- [ ] 多模型结果融合
- [ ] 置信度加权
- [ ] 异常检测与过滤

---

## 🔧 技术实现细节

### 数据流程

```
原始数据 (AKShare)
    ↓
数据清洗与预处理 (data_processing)
    ↓
特征工程 (技术指标计算)
    ↓
模型预测 (prediction_models)
    ↓
结果聚合 (business_logic)
    ↓
交易建议生成 (business_logic)
    ↓
GUI 展示 (gui)
```

### 模型训练流程

1. **数据准备**
   - 获取历史数据（至少 1 年）
   - 计算技术指标
   - 特征工程

2. **模型训练**
   - LSTM: 时序数据训练
   - XGBoost: 标注数据训练
   - 超参数调优

3. **模型验证**
   - 回测验证
   - 性能评估
   - 模型选择

4. **模型部署**
   - 模型保存
   - 版本管理
   - 在线预测

---

## 📦 新增依赖

Phase 2 将使用以下库（已在 requirements.txt 中列出）：

### 机器学习框架
- **PyTorch** (>=2.0.0) - LSTM/GRU 实现
- **TensorFlow** (>=2.13.0) - 备选深度学习框架
- **XGBoost** - 梯度提升树模型

### 技术分析
- **TA-Lib** (>=0.4.28) - 技术指标库
- **pandas-ta** - Python 技术分析库（可选）

### 时序预测
- **Prophet** (>=1.1.5) - Facebook 时序预测库（可选用于长期预测）

### 工具库
- **scikit-learn** (>=1.3.0) - 数据预处理、模型评估
- **joblib** - 模型序列化

---

## 🏗️ 项目结构更新

```
src/
├── data_processing/          # 📊 数据处理模块
│   ├── __init__.py
│   ├── preprocessor.py       # 数据预处理
│   ├── feature_engineer.py   # 特征工程
│   └── indicators.py         # 技术指标计算
│
├── prediction_models/        # 🤖 预测模型模块
│   ├── __init__.py
│   ├── base_model.py         # 模型基类
│   ├── lstm_model.py         # LSTM 时序模型
│   ├── xgboost_model.py      # XGBoost 分类模型
│   ├── model_trainer.py      # 模型训练器
│   └── model_evaluator.py    # 模型评估器
│
└── business_logic/           # 💼 业务逻辑模块
    ├── __init__.py
    ├── prediction_engine.py  # 预测引擎
    ├── recommendation.py     # 交易建议
    └── risk_manager.py       # 风险管理
```

---

## 📝 GUI 更新

### 预测页面增强
- [ ] 实时预测结果展示
- [ ] 技术指标图表可视化
- [ ] 置信度可视化
- [ ] 历史预测准确率统计

### 新增功能页面
- [ ] 模型管理页面（训练、评估、版本）
- [ ] 技术指标详情页面
- [ ] 交易建议详情页面

---

## 🧪 测试计划

### 单元测试
- [ ] `test_indicators.py` - 技术指标计算
- [ ] `test_preprocessor.py` - 数据预处理
- [ ] `test_models.py` - 模型训练与预测
- [ ] `test_recommendation.py` - 交易建议生成

### 集成测试
- [ ] 端到端预测流程测试
- [ ] 模型性能回测
- [ ] GUI 功能测试

### 性能测试
- [ ] 预测响应时间
- [ ] 批量处理性能
- [ ] 内存使用优化

---

## 📚 文档更新

- [ ] **API 文档** - 新增模块的 API 说明
- [ ] **模型文档** - 模型架构、参数说明
- [ ] **用户手册** - 如何使用预测功能
- [ ] **开发指南** - 如何训练和部署模型

---

## 🎯 里程碑

### Milestone 1: 技术指标模块 (Week 1-2)
- 实现 TA-Lib 集成
- 实现常用技术指标
- 单元测试通过

### Milestone 2: 数据预处理 (Week 2-3)
- 数据清洗流程
- 特征工程
- 数据集准备

### Milestone 3: LSTM 模型 (Week 3-4)
- 模型架构设计
- 模型训练流程
- 预测功能实现

### Milestone 4: XGBoost 模型 (Week 4-5)
- 特征工程
- 模型训练
- 分类预测

### Milestone 5: 业务逻辑 (Week 5-6)
- 预测引擎实现
- 交易建议生成
- 风险评估

### Milestone 6: GUI 集成 (Week 6-7)
- 预测页面更新
- 结果可视化
- 用户体验优化

### Milestone 7: 测试与文档 (Week 7-8)
- 全面测试
- 文档完善
- Bug 修复

---

## 🚀 成功标准

Phase 2 完成后，系统应该能够：

1. ✅ **技术指标**
   - 计算至少 10 种常用技术指标
   - 指标准确性验证通过

2. ✅ **预测功能**
   - 短期预测（1天）平均误差 < 5%
   - 趋势分类准确率 > 60%
   - 预测响应时间 < 3 秒

3. ✅ **交易建议**
   - 生成可操作的买卖建议
   - 包含止损止盈价格
   - 提供风险评估

4. ✅ **用户体验**
   - GUI 界面完整展示预测结果
   - 结果可视化清晰
   - 操作流程顺畅

---

## 🔜 Phase 3 预告

Phase 3 将实现高级功能：

- **Transformer 模型** - 长期趋势预测
- **观测池预警** - 自动监控与通知
- **批量分析** - 多股票并行分析
- **回测系统** - 策略回测与优化
- **实时监控** - 盘中实时分析

---

## 📞 参考资源

### 技术文档
- [PyTorch 官方文档](https://pytorch.org/docs/)
- [XGBoost 文档](https://xgboost.readthedocs.io/)
- [TA-Lib 文档](https://ta-lib.org/)
- [scikit-learn 文档](https://scikit-learn.org/)

### 学术论文
- LSTM for Stock Prediction: 时序预测基础
- XGBoost: A Scalable Tree Boosting System
- Technical Analysis Indicators: 技术分析指标

### 开源项目参考
- [Qlib (Microsoft)](https://github.com/microsoft/qlib) - 量化投资平台
- [FinRL](https://github.com/AI4Finance-Foundation/FinRL) - 强化学习交易
- [Stock-Prediction-Models](https://github.com/huseinzol05/Stock-Prediction-Models) - 各类预测模型实现

---

## ✅ 前置条件

在开始 Phase 2 之前，确保：

- [x] Phase 1 所有功能已完成
- [x] 所有 Phase 1 测试通过
- [x] 文档已更新
- [ ] 所需依赖已安装（需要时再安装 ML 库）
- [ ] 训练数据已准备（至少 1 年历史数据）

---

**项目地址**: [https://github.com/qq173681019/JericoNewStockSystem](https://github.com/qq173681019/JericoNewStockSystem)

**当前版本**: v0.1.0  
**目标版本**: v0.2.0

**许可证**: MIT

---

*Created with ❤️ by the SIAPS Team*
