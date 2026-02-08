#!/usr/bin/env python3
"""
关注池备份管理工具
Watchlist Backup Management Tool

用法 Usage:
  python backup_watchlist.py export [filepath]     # 导出关注池
  python backup_watchlist.py import <filepath>     # 导入关注池（合并）
  python backup_watchlist.py import <filepath> --replace  # 导入关注池（替换）
  python backup_watchlist.py backup                # 创建自动备份
  python backup_watchlist.py list                  # 列出所有备份文件
"""

import sys
import argparse
from pathlib import Path
from datetime import datetime

# Add project root to Python path
ROOT_DIR = Path(__file__).parent
sys.path.insert(0, str(ROOT_DIR))

from src.database.models import DatabaseManager
from config.settings import DATA_DIR


def main():
    parser = argparse.ArgumentParser(
        description='关注池备份管理工具 - Watchlist Backup Management Tool',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例 Examples:
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
        """
    )
    
    subparsers = parser.add_subparsers(dest='command', help='可用命令')
    
    # Export command
    export_parser = subparsers.add_parser('export', help='导出关注池到JSON文件')
    export_parser.add_argument('filepath', nargs='?', help='导出文件路径（可选）')
    
    # Import command
    import_parser = subparsers.add_parser('import', help='从JSON文件导入关注池')
    import_parser.add_argument('filepath', help='导入文件路径')
    import_parser.add_argument('--replace', action='store_true', 
                              help='替换模式（默认为合并模式）')
    
    # Backup command
    subparsers.add_parser('backup', help='创建自动备份（带时间戳）')
    
    # List command
    subparsers.add_parser('list', help='列出所有备份文件')
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return 1
    
    # Initialize database manager
    db_manager = DatabaseManager()
    
    if args.command == 'export':
        # Export watchlist
        filepath = args.filepath if args.filepath else None
        result_path = db_manager.export_watchlist_to_json(filepath)
        print(f"✅ 关注池已导出到: {result_path}")
        
        # Show count
        watchlist = db_manager.get_watchlist()
        print(f"📊 导出了 {len(watchlist)} 个股票")
        
    elif args.command == 'import':
        # Import watchlist
        filepath = args.filepath
        if not Path(filepath).exists():
            print(f"❌ 错误: 文件不存在: {filepath}")
            return 1
        
        merge = not args.replace
        mode_text = "合并" if merge else "替换"
        print(f"📥 正在导入关注池（{mode_text}模式）...")
        
        count = db_manager.import_watchlist_from_json(filepath, merge=merge)
        print(f"✅ 成功导入 {count} 个股票")
        
    elif args.command == 'backup':
        # Create automatic backup
        filepath = db_manager.auto_backup_watchlist()
        print(f"✅ 备份已创建: {filepath}")
        
        # Show count
        watchlist = db_manager.get_watchlist()
        print(f"📊 备份了 {len(watchlist)} 个股票")
        
    elif args.command == 'list':
        # List all backup files
        backup_dir = DATA_DIR / "backups"
        if not backup_dir.exists():
            print("📁 备份目录不存在")
            return 0
        
        backup_files = sorted(backup_dir.glob("*.json"), key=lambda p: p.stat().st_mtime, reverse=True)
        
        if not backup_files:
            print("📁 没有找到备份文件")
            return 0
        
        print(f"📁 找到 {len(backup_files)} 个备份文件:\n")
        
        for i, filepath in enumerate(backup_files, 1):
            stat = filepath.stat()
            size = stat.st_size / 1024  # KB
            mtime = datetime.fromtimestamp(stat.st_mtime).strftime('%Y-%m-%d %H:%M:%S')
            print(f"  {i}. {filepath.name}")
            print(f"     大小: {size:.2f} KB | 修改时间: {mtime}")
            print()
    
    return 0


if __name__ == '__main__':
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        print("\n\n⚠️  操作已取消")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ 错误: {str(e)}")
        sys.exit(1)
