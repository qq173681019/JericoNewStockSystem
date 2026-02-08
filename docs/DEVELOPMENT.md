# SIAPS 开发文档

## 快速开始指南

本文档提供SIAPS项目的开发环境配置和基本使用说明。

## 开发环境配置

### 1. Python环境

确保已安装Python 3.8或更高版本：

```bash
python --version  # 应显示 Python 3.8.x 或更高
```

### 2. 依赖安装

项目使用以下主要依赖：

- **CustomTkinter**: 现代化GUI框架
- **AKShare**: 金融数据获取
- **Pandas/NumPy**: 数据处理
- **SQLAlchemy**: 数据库ORM
- **PyTorch/TensorFlow**: 深度学习框架（Phase 2）

安装所有依赖：

```bash
pip install -r requirements.txt
```

### 3. 配置文件

复制环境变量模板并配置：

```bash
cp .env.example .env
```

编辑 `.env` 文件配置：

```env
APP_NAME=SIAPS
DEBUG=True
DATABASE_URL=sqlite:///data/siaps.db
THEME=dark
AKSHARE_ENABLED=True
```

## 项目结构说明

### 核心模块

#### 1. config/
配置管理模块，包含所有应用配置和环境变量加载。

#### 2. src/data_acquisition/
数据获取层，负责从各种数据源获取股票数据。

**主要类**:
- `DataFetcher`: 数据获取基类
- `AKShareFetcher`: AKShare数据源实现

**使用示例**:
```python
from src.data_acquisition import get_data_fetcher

fetcher = get_data_fetcher("akshare")
df = fetcher.fetch_daily_data("000001", "20240101", "20240131")
```

#### 3. src/database/
数据库层，使用SQLAlchemy ORM管理数据。

**主要表**:
- `PredictionHistory`: 预测历史记录
- `Watchlist`: 用户观测池

**使用示例**:
```python
from src.database import DatabaseManager

db = DatabaseManager()
db.add_to_watchlist("000001", "平安银行", target_price=15.0)
```

#### 4. src/gui/
GUI界面层，使用CustomTkinter构建。

**主要组件**:
- `MainApplication`: 主窗口类
- 侧边栏导航
- 多页面切换

#### 5. src/utils/
工具模块，提供通用功能。

**主要功能**:
- 日志配置
- 股票代码验证
- 时间戳处理

## 开发工作流

### 1. 启动应用

```bash
python main.py
```

### 2. 代码规范

项目遵循PEP 8代码规范。使用工具检查：

```bash
# 代码格式化
black src/

# 代码检查
flake8 src/
```

### 3. 测试

```bash
# 运行测试
pytest tests/

# 运行测试并生成覆盖率报告
pytest --cov=src tests/
```

## 常见问题

### Q: 如何添加新的数据源？

A: 在 `src/data_acquisition/fetcher.py` 中：
1. 创建新类继承 `DataFetcher`
2. 实现 `fetch_daily_data` 和 `fetch_realtime_data` 方法
3. 在 `get_data_fetcher` 函数中注册

### Q: 如何添加新的GUI页面？

A: 在 `src/gui/main_window.py` 中：
1. 创建新的视图方法 `show_xxx_view`
2. 在侧边栏添加导航按钮
3. 实现页面布局和交互逻辑

### Q: 数据库文件在哪里？

A: 默认在 `data/siaps.db`，可通过 `.env` 文件修改。

## 下一步计划

根据开发路线图，接下来将实现：

1. **技术指标计算模块**: 集成TA-Lib，计算常用技术指标
2. **机器学习模型**: 实现LSTM和XGBoost预测模型
3. **预测结果可视化**: 添加图表展示功能

## 参考资料

- [CustomTkinter文档](https://customtkinter.tomschimansky.com/)
- [AKShare文档](https://akshare.akfamily.xyz/)
- [SQLAlchemy文档](https://docs.sqlalchemy.org/)
- [Pandas文档](https://pandas.pydata.org/docs/)

## 联系方式

如有问题，请在GitHub Issues中提出。
