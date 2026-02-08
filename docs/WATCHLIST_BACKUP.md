# 关注池备份与恢复功能

## 问题描述

在合并分支后，关注池（观测池）中的数据经常丢失。这是因为数据库文件（*.db）被 `.gitignore` 排除在版本控制之外，导致在分支合并时数据库无法合并。

## 解决方案

我们实现了全面的备份和恢复功能，确保您的关注池数据永远不会丢失。

## 功能特性

### 1. 自动备份

系统会在以下情况自动创建备份：
- 添加股票到关注池时
- 从关注池移除股票时

自动备份文件保存在 `data/backups/` 目录下，文件名格式为 `watchlist_backup_YYYYMMDD_HHMMSS.json`

### 2. 手动导出

在Web界面的"观测池管理"页面，点击"导出"按钮可以手动导出当前的关注池数据到JSON文件。

**使用步骤：**
1. 进入"观测池管理"页面
2. 点击"📥 导出"按钮
3. 浏览器会自动下载 `watchlist_backup_YYYY-MM-DD.json` 文件

### 3. 手动导入

您可以通过导入功能恢复之前导出的备份文件。

**使用步骤：**
1. 进入"观测池管理"页面
2. 点击"📤 导入"按钮
3. 选择之前导出的JSON备份文件
4. 选择导入模式：
   - **合并**：将导入的数据与现有数据合并（相同股票代码会更新）
   - **替换**：清空现有数据并导入新数据

### 4. 客户端缓存

Web界面使用 localStorage 缓存关注池数据，即使服务器重启，数据也会保留在浏览器中。

## API 接口

### 导出关注池
```
GET /api/watchlist/export
```

**响应示例：**
```json
{
  "success": true,
  "data": [
    {
      "stock_code": "000001",
      "stock_name": "平安银行",
      "target_price": 15.5,
      "target_days": 30,
      "stop_loss_price": null,
      "stop_profit_price": null,
      "notes": "测试备注",
      "created_at": "2026-02-06T09:30:00",
      "updated_at": "2026-02-06T09:30:00"
    }
  ],
  "message": "已导出 1 个股票",
  "filepath": "/path/to/backup.json"
}
```

### 导入关注池
```
POST /api/watchlist/import
Content-Type: application/json

{
  "data": [...],  // 关注池数据数组
  "merge": true   // true=合并, false=替换
}
```

**响应示例：**
```json
{
  "success": true,
  "message": "已导入 1 个股票",
  "count": 1
}
```

### 创建备份
```
POST /api/watchlist/backup
```

**响应示例：**
```json
{
  "success": true,
  "message": "备份已创建",
  "filepath": "/path/to/backup.json"
}
```

## Python API 使用

```python
from src.database.models import DatabaseManager

db_manager = DatabaseManager()

# 导出关注池到JSON文件
filepath = db_manager.export_watchlist_to_json('my_backup.json')

# 导入关注池（合并模式）
count = db_manager.import_watchlist_from_json('my_backup.json', merge=True)

# 导入关注池（替换模式）
count = db_manager.import_watchlist_from_json('my_backup.json', merge=False)

# 创建自动备份（带时间戳）
filepath = db_manager.auto_backup_watchlist()
```

## 命令行工具

提供了便捷的命令行工具 `backup_watchlist.py` 用于管理备份：

```bash
# 导出关注池到默认文件
python backup_watchlist.py export

# 导出关注池到指定文件
python backup_watchlist.py export my_backup.json

# 导入关注池（合并模式）
python backup_watchlist.py import my_backup.json

# 导入关注池（替换模式）
python backup_watchlist.py import my_backup.json --replace

# 创建带时间戳的自动备份
python backup_watchlist.py backup

# 列出所有备份文件
python backup_watchlist.py list
```

## 最佳实践

### 定期备份
建议定期导出关注池数据：
1. 每周导出一次作为长期备份
2. 在进行重要操作前导出
3. 在分支合并前导出

### 备份文件管理
- 自动备份保存在 `data/backups/` 目录
- 手动导出的文件建议保存在安全的位置
- 备份文件采用JSON格式，易于阅读和编辑

### 合并冲突处理
如果在合并分支后发现关注池为空：
1. 找到最近的备份文件（`data/backups/` 目录）
2. 使用"导入"功能恢复数据
3. 选择"合并"模式保留所有数据

## 数据格式

备份JSON文件格式：
```json
[
  {
    "stock_code": "000001",
    "stock_name": "平安银行",
    "target_price": 15.5,
    "target_days": 30,
    "stop_loss_price": 14.0,
    "stop_profit_price": 17.0,
    "notes": "重点关注",
    "created_at": "2026-02-06T09:30:00",
    "updated_at": "2026-02-06T09:30:00"
  }
]
```

## 故障排除

### 问题：无法导入备份
**解决方案：**
1. 检查JSON文件格式是否正确
2. 确认文件编码为UTF-8
3. 查看浏览器控制台的错误信息

### 问题：自动备份失败
**解决方案：**
1. 检查 `data/backups/` 目录是否有写入权限
2. 查看服务器日志获取详细错误信息
3. 确保磁盘空间充足

### 问题：导出的文件为空
**解决方案：**
1. 确认关注池中有数据
2. 刷新页面后重试
3. 查看服务器日志确认数据库连接正常

## 技术细节

### 自动备份触发时机
- `add_to_watchlist()` 后
- `remove_from_watchlist()` 后
- 每次操作都会创建带时间戳的备份文件

### 数据持久化
- 后端：SQLite数据库（`data/siaps.db`）
- 前端：localStorage缓存
- 备份：JSON文件（`data/backups/`）

### 安全性
- 备份文件不包含敏感信息
- JSON格式便于审查和编辑
- 支持版本控制（可选）

## 更新日志

**2026-02-06**
- ✅ 添加自动备份功能
- ✅ 添加手动导出/导入功能
- ✅ 添加Web UI界面
- ✅ 更新.gitignore以保留备份文件
- ✅ 添加完整的测试用例
