# SIAPS Web UI

现代化的股票智能分析预测系统 Web 界面

## 功能特性

### 📱 美观的用户界面
- 响应式设计，支持桌面端和移动端
- 深色/浅色主题切换
- 流畅的动画和过渡效果
- 直观的导航和交互

### 📊 核心功能
1. **股票预测**
   - 输入股票代码进行预测
   - 支持短期、中期、长期预测
   - 实时显示预测结果和置信度
   - 可视化价格走势图和技术指标

2. **观测池管理**
   - 添加关注的股票到观测池
   - 实时查看价格变动
   - 设置价格预警

3. **历史记录**
   - 查看历史预测记录
   - 分析预测准确率
   - 导出数据报告

4. **技术分析**
   - MACD、RSI、布林带、KDJ等技术指标
   - 实时计算和可视化
   - 买卖信号提示

5. **系统设置**
   - 主题模式设置
   - 数据源配置
   - 通知设置

## 快速开始

### 1. 安装依赖

```bash
pip install -r requirements.txt
```

### 2. 启动 Web 服务器

```bash
# 方式一：直接运行 Web UI 服务器
python web_ui/app.py

# 方式二：使用启动脚本
python run_web_ui.py
```

### 3. 访问界面

打开浏览器访问：`http://127.0.0.1:5000`

## 技术栈

### 前端
- **HTML5/CSS3**: 现代化的界面布局和样式
- **JavaScript (ES6+)**: 交互逻辑和动态更新
- **Chart.js**: 数据可视化图表库
- **Font Awesome**: 图标库

### 后端
- **Flask**: 轻量级 Python Web 框架
- **Flask-CORS**: 跨域资源共享支持

### 特性
- **无需复杂后端**: 最小化后端依赖，前端可独立运行
- **RESTful API**: 标准的 API 接口设计
- **响应式设计**: 支持多种设备和屏幕尺寸
- **主题切换**: 支持深色和浅色主题

## API 接口

### 预测接口
```
POST /api/predict
Content-Type: application/json

{
  "stock_code": "000001",
  "prediction_type": "short"
}
```

### 观测池接口
```
GET /api/watchlist
POST /api/watchlist
```

### 历史记录接口
```
GET /api/history
```

### 技术分析接口
```
POST /api/technical-analysis
Content-Type: application/json

{
  "stock_code": "000001"
}
```

## 项目结构

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
└── README.md          # 本文件
```

## 开发说明

### 自定义主题
在 `style.css` 中修改 CSS 变量：

```css
:root {
    --primary-color: #3b82f6;
    --success-color: #10b981;
    /* ... 更多颜色变量 */
}
```

### 添加新功能
1. 在 `index.html` 中添加 UI 组件
2. 在 `app.js` 中添加交互逻辑
3. 在 `app.py` 中添加 API 接口
4. 更新样式文件 `style.css`

### 集成实际预测模型
在 `app.py` 的 API 接口中：

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

## 浏览器支持

- Chrome (推荐)
- Firefox
- Safari
- Edge
- 其他现代浏览器

## 许可证

MIT License

## 贡献

欢迎提交 Issue 和 Pull Request！
