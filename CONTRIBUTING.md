# 贡献指南

首先，感谢您考虑为SIAPS项目做出贡献！正是像您这样的人使得开源社区如此出色。

## 行为准则

本项目及其参与者均遵守以下行为准则。通过参与，您同意遵守这些准则。

### 我们的承诺
- 使用友好和包容的语言
- 尊重不同的观点和经验
- 优雅地接受建设性批评
- 专注于对社区最有利的事情
- 对其他社区成员表示同理心

## 如何贡献

### 报告Bug

如果您发现了Bug，请通过以下步骤报告：

1. **检查是否已存在**：在[Issues](https://github.com/qq173681019/JericoNewStockSystem/issues)中搜索类似问题
2. **创建新Issue**：如果没有找到，创建新Issue
3. **提供详细信息**：
   - 清晰的标题和描述
   - 复现步骤
   - 预期行为
   - 实际行为
   - 系统信息（OS、Python版本等）
   - 相关日志或截图

### 建议新功能

我们欢迎新功能建议！请：

1. 检查[Issues](https://github.com/qq173681019/JericoNewStockSystem/issues)中是否已有类似建议
2. 创建新Issue，标题以"[Feature Request]"开头
3. 详细描述：
   - 功能的用途和价值
   - 建议的实现方式
   - 可能的替代方案

### 提交代码

#### 准备工作

1. **Fork仓库**
```bash
# 在GitHub上点击Fork按钮
```

2. **克隆您的Fork**
```bash
git clone https://github.com/YOUR_USERNAME/JericoNewStockSystem.git
cd JericoNewStockSystem
```

3. **添加上游仓库**
```bash
git remote add upstream https://github.com/qq173681019/JericoNewStockSystem.git
```

4. **创建虚拟环境**
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# 或
venv\Scripts\activate     # Windows
```

5. **安装开发依赖**
```bash
pip install -r requirements.txt
pip install -e ".[dev]"  # 安装开发工具
```

#### 开发流程

1. **创建特性分支**
```bash
git checkout -b feature/amazing-feature
# 或
git checkout -b bugfix/fix-issue-123
```

2. **编写代码**
   - 遵循项目代码风格
   - 添加必要的测试
   - 更新相关文档

3. **代码格式化**
```bash
# 格式化代码
black src/ tests/

# 检查代码风格
flake8 src/ tests/
```

4. **运行测试**
```bash
# 运行所有测试
pytest tests/

# 运行特定测试
pytest tests/test_utils.py

# 生成覆盖率报告
pytest --cov=src tests/
```

5. **提交更改**
```bash
git add .
git commit -m "feat: 添加某某功能"
```

**提交信息规范**:
- `feat`: 新功能
- `fix`: Bug修复
- `docs`: 文档更新
- `style`: 代码格式调整（不影响功能）
- `refactor`: 代码重构
- `test`: 测试相关
- `chore`: 构建/工具链相关

6. **推送到您的Fork**
```bash
git push origin feature/amazing-feature
```

7. **创建Pull Request**
   - 访问GitHub上您的Fork
   - 点击"New Pull Request"
   - 填写PR模板
   - 等待审查

#### Pull Request检查清单

提交PR前，请确认：

- [ ] 代码遵循项目风格指南
- [ ] 添加了必要的测试
- [ ] 所有测试都通过
- [ ] 更新了相关文档
- [ ] 提交信息清晰明确
- [ ] PR描述详细说明了更改内容

## 代码规范

### Python代码风格

我们遵循[PEP 8](https://www.python.org/dev/peps/pep-0008/)规范：

```python
# 好的示例
def fetch_stock_data(stock_code: str, start_date: str) -> pd.DataFrame:
    """
    获取股票数据
    
    Args:
        stock_code: 股票代码
        start_date: 开始日期
    
    Returns:
        pd.DataFrame: 股票数据
    """
    if not validate_stock_code(stock_code):
        raise ValueError(f"Invalid stock code: {stock_code}")
    
    return fetcher.fetch_daily_data(stock_code, start_date)
```

### 文档规范

- 所有公共函数/类都应有docstring
- 使用Google风格的docstring
- 复杂逻辑添加注释

### 测试规范

```python
def test_validate_stock_code():
    """测试股票代码验证功能"""
    # 有效代码
    assert validate_stock_code("000001") == True
    
    # 无效代码
    assert validate_stock_code("ABC") == False
    assert validate_stock_code("") == False
```

## 项目结构

贡献前，请熟悉项目结构：

```
JericoNewStockSystem/
├── config/              # 配置模块
├── src/                 # 源代码
│   ├── data_acquisition/   # 数据获取
│   ├── data_processing/    # 数据处理
│   ├── prediction_models/  # 预测模型
│   ├── business_logic/     # 业务逻辑
│   ├── gui/               # GUI界面
│   ├── database/          # 数据库
│   └── utils/             # 工具函数
├── tests/               # 测试文件
├── docs/                # 文档
└── main.py             # 入口文件
```

## 开发环境设置

### IDE推荐

- **VS Code**（推荐）
  - Python扩展
  - Pylance
  - Black Formatter
- **PyCharm**
- **Vim/Neovim**

### 有用的命令

```bash
# 运行应用
python main.py

# 运行演示
python demo.py

# 运行测试
pytest tests/

# 代码格式化
black src/ tests/

# 代码检查
flake8 src/ tests/

# 类型检查（可选）
mypy src/
```

## 发布流程

发布由维护者处理，但了解流程有助于贡献：

1. 更新版本号（`setup.py`, `config/settings.py`）
2. 更新CHANGELOG.md
3. 创建Git标签
4. 构建分发包
5. 上传到PyPI

## 获取帮助

如果您有任何问题：

1. 查看[文档](docs/)
2. 搜索[Issues](https://github.com/qq173681019/JericoNewStockSystem/issues)
3. 创建新Issue询问

## 致谢

感谢所有贡献者！您的努力使这个项目变得更好。

贡献者名单请见[CONTRIBUTORS.md](CONTRIBUTORS.md)

---

再次感谢您的贡献！🎉
