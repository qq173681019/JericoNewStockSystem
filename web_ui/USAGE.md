# SIAPS Web UI - 使用说明

## 概述

SIAPS (Stock Intelligent Analysis & Prediction System) 现在提供了现代化的 Web 用户界面，使用简洁美观的设计，无需复杂的后端配置即可运行。

## 功能特点

### 1. 现代化设计
- **响应式布局**: 自动适配不同屏幕尺寸（桌面、平板、手机）
- **主题切换**: 支持浅色和深色两种主题模式
- **流畅动画**: 平滑的页面切换和交互效果
- **直观导航**: 侧边栏导航，快速访问各个功能模块

### 2. 核心功能模块

#### 股票预测
- 输入6位股票代码（如：000001）
- 选择预测类型（短期/中期/长期）
- 一键获取智能预测结果
- 显示预测趋势、目标价位、风险评估和操作建议
- 可视化价格走势图和技术指标（需要 Chart.js）

#### 观测池管理
- 添加关注的股票到观测池
- 实时显示股票价格和涨跌幅
- 支持查看详情、设置预警和移除操作
- 价格变动颜色提示（上涨绿色，下跌红色）

#### 历史记录
- 查看历史预测记录
- 对比预测值与实际值
- 准确率统计和分析
- 支持筛选和导出功能

#### 技术分析
- 多种技术指标（MACD、RSI、布林带、KDJ）
- 实时计算和可视化
- 买卖信号提示

#### 系统设置
- 主题模式设置
- 数据源配置
- 通知开关

## 快速开始

### 方式一：使用启动脚本（推荐）

```bash
python run_web_ui.py
```

启动脚本会：
1. 自动启动 Flask 服务器
2. 2秒后自动打开浏览器
3. 访问 http://127.0.0.1:5000

### 方式二：直接运行服务器

```bash
python web_ui/app.py
```

然后手动在浏览器中访问 http://127.0.0.1:5000

### 方式三：自定义配置

```python
from web_ui.app import run_server

# 自定义主机和端口
run_server(host='0.0.0.0', port=8080, debug=False)
```

## 使用指南

### 进行股票预测

1. 点击左侧导航栏的"股票预测"
2. 在"股票代码"输入框中输入6位数字代码（例如：000001）
3. 选择预测类型（短期、中期或长期）
4. 点击"开始预测"按钮
5. 等待2-3秒，查看预测结果

预测结果包括：
- **预测趋势**: 上涨/下跌百分比和置信度
- **目标价位**: 预测价格和当前价格
- **风险评估**: 风险等级和建议仓位
- **操作建议**: 买入/持有/观望建议
- **技术指标**: MACD、RSI、KDJ等指标值
- **详细分析**: 完整的分析报告

### 管理观测池

1. 点击"观测池"进入观测池管理页面
2. 点击"添加股票"按钮
3. 输入股票代码
4. 查看已添加的股票列表
5. 可以设置预警、查看详情或移除股票

### 查看历史记录

1. 点击"历史记录"
2. 查看所有历史预测记录
3. 使用筛选器筛选记录（全部/准确/偏差）
4. 点击"导出"按钮导出数据

### 切换主题

方式一：使用侧边栏底部的主题切换开关
方式二：在"设置"页面选择主题模式

## 技术细节

### 前端技术
- HTML5 + CSS3
- JavaScript (ES6+)
- Chart.js (数据可视化)
- Font Awesome (图标)

### 后端技术
- Flask 3.0+
- Flask-CORS (跨域支持)
- Python 3.8+

### API 接口

#### 健康检查
```
GET /api/health
返回: {"status": "healthy", "service": "SIAPS Web UI", "version": "0.1.0"}
```

#### 股票预测
```
POST /api/predict
请求体: {"stock_code": "000001", "prediction_type": "short"}
返回: 预测结果 JSON
```

#### 观测池
```
GET /api/watchlist - 获取观测池列表
POST /api/watchlist - 添加股票到观测池
```

#### 历史记录
```
GET /api/history - 获取历史记录
```

#### 技术分析
```
POST /api/technical-analysis - 技术分析
请求体: {"stock_code": "000001"}
```

## 浏览器支持

- Chrome 90+ (推荐)
- Firefox 88+
- Safari 14+
- Edge 90+
- 其他现代浏览器

## 常见问题

### Q: 图表不显示？
A: 如果使用的网络环境屏蔽了 CDN，图表库可能无法加载。数据仍会正常显示，只是没有可视化图表。

### Q: 如何更改服务器端口？
A: 编辑 `web_ui/app.py` 文件中的 `run_server()` 函数调用，修改 `port` 参数。

### Q: 预测结果是真实的吗？
A: 当前版本使用模拟数据。实际预测需要集成真实的预测模型（在 TODO 标记处实现）。

### Q: 如何部署到生产环境？
A: 不建议使用 Flask 开发服务器部署到生产环境。建议使用 Gunicorn 或 uWSGI：

```bash
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 web_ui.app:app
```

## 开发指南

### 项目结构
```
web_ui/
├── app.py              # Flask 应用主文件
├── templates/          # HTML 模板
│   └── index.html     # 主页面
├── static/            # 静态资源
│   ├── css/
│   │   └── style.css  # 样式文件
│   ├── js/
│   │   └── app.js     # JavaScript 逻辑
│   └── images/        # 图片资源
└── README.md          # 文档
```

### 自定义样式

修改 `web_ui/static/css/style.css` 中的 CSS 变量：

```css
:root {
    --primary-color: #3b82f6;  /* 主色调 */
    --success-color: #10b981;  /* 成功色 */
    --danger-color: #ef4444;   /* 危险色 */
    /* ... 更多颜色 */
}
```

### 集成真实预测模型

在 `web_ui/app.py` 中替换模拟数据：

```python
from src.prediction_models import PredictionEngine

@app.route('/api/predict', methods=['POST'])
def predict():
    data = request.get_json()
    stock_code = data.get('stock_code')
    
    # 使用实际预测引擎
    engine = PredictionEngine()
    result = engine.predict(stock_code)
    
    return jsonify(result)
```

## 贡献

欢迎提交 Issue 和 Pull Request 来改进 Web UI！

## 许可证

MIT License
