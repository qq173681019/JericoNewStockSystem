"""
Test watchlist backup and restore functionality
"""
import sys
import json
from pathlib import Path
import tempfile

# Add project root to Python path
ROOT_DIR = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT_DIR))

from src.database.models import DatabaseManager


def test_export_import_watchlist():
    """Test exporting and importing watchlist"""
    # Create a temporary database for testing
    with tempfile.NamedTemporaryFile(suffix='.db', delete=False) as tmp_db:
        db_url = f"sqlite:///{tmp_db.name}"
        db_manager = DatabaseManager(database_url=db_url)
        
        # Add test data
        db_manager.add_to_watchlist(
            stock_code='000001',
            stock_name='平安银行',
            target_price=15.5,
            target_days=30,
            notes='测试股票1'
        )
        
        db_manager.add_to_watchlist(
            stock_code='600000',
            stock_name='浦发银行',
            target_price=10.2,
            target_days=20,
            notes='测试股票2'
        )
        
        # Export watchlist
        with tempfile.NamedTemporaryFile(suffix='.json', delete=False, mode='w') as tmp_export:
            export_path = tmp_export.name
        
        result_path = db_manager.export_watchlist_to_json(export_path)
        assert Path(result_path).exists(), "Export file should exist"
        
        # Verify exported content
        with open(result_path, 'r', encoding='utf-8') as f:
            exported_data = json.load(f)
        
        assert len(exported_data) == 2, "Should have 2 items"
        assert exported_data[0]['stock_code'] == '000001', "First item should be 000001"
        assert exported_data[1]['stock_code'] == '600000', "Second item should be 600000"
        
        # Clear watchlist
        watchlist = db_manager.get_watchlist()
        for item in watchlist:
            db_manager.remove_from_watchlist(item.stock_code)
        
        # Verify cleared
        watchlist_after_clear = db_manager.get_watchlist()
        assert len(watchlist_after_clear) == 0, "Watchlist should be empty"
        
        # Import watchlist
        count = db_manager.import_watchlist_from_json(result_path, merge=False)
        assert count == 2, "Should import 2 items"
        
        # Verify imported data
        watchlist_after_import = db_manager.get_watchlist()
        assert len(watchlist_after_import) == 2, "Should have 2 items after import"
        
        codes = [item.stock_code for item in watchlist_after_import]
        assert '000001' in codes, "Should have 000001"
        assert '600000' in codes, "Should have 600000"
        
        # Clean up
        Path(tmp_db.name).unlink()
        Path(export_path).unlink()
        
        print("✅ All watchlist backup/restore tests passed!")


def test_merge_import():
    """Test merging imported data with existing data"""
    # Create a temporary database for testing
    with tempfile.NamedTemporaryFile(suffix='.db', delete=False) as tmp_db:
        db_url = f"sqlite:///{tmp_db.name}"
        db_manager = DatabaseManager(database_url=db_url)
        
        # Add initial data
        db_manager.add_to_watchlist(
            stock_code='000001',
            stock_name='平安银行',
            target_price=15.5,
            target_days=30
        )
        
        # Create import data with one overlapping and one new item
        import_data = [
            {
                'stock_code': '000001',
                'stock_name': '平安银行更新',
                'target_price': 16.0,
                'target_days': 25,
                'stop_loss_price': None,
                'stop_profit_price': None,
                'notes': '更新的备注',
                'created_at': None,
                'updated_at': None
            },
            {
                'stock_code': '600000',
                'stock_name': '浦发银行',
                'target_price': 10.2,
                'target_days': 20,
                'stop_loss_price': None,
                'stop_profit_price': None,
                'notes': '新股票',
                'created_at': None,
                'updated_at': None
            }
        ]
        
        # Save import data to file
        with tempfile.NamedTemporaryFile(suffix='.json', delete=False, mode='w', encoding='utf-8') as tmp_import:
            json.dump(import_data, tmp_import, ensure_ascii=False, indent=2)
            import_path = tmp_import.name
        
        # Import with merge
        count = db_manager.import_watchlist_from_json(import_path, merge=True)
        assert count == 2, "Should import 2 items"
        
        # Verify merged data
        watchlist = db_manager.get_watchlist()
        assert len(watchlist) == 2, "Should have 2 items total (1 updated, 1 new)"
        
        # Find the updated item
        updated_item = next((item for item in watchlist if item.stock_code == '000001'), None)
        assert updated_item is not None, "Should find updated item"
        assert updated_item.stock_name == '平安银行更新', "Name should be updated"
        assert updated_item.target_price == 16.0, "Target price should be updated"
        
        # Find the new item
        new_item = next((item for item in watchlist if item.stock_code == '600000'), None)
        assert new_item is not None, "Should find new item"
        
        # Clean up
        Path(tmp_db.name).unlink()
        Path(import_path).unlink()
        
        print("✅ Merge import test passed!")


def test_auto_backup():
    """Test automatic backup functionality"""
    # Create a temporary database for testing
    with tempfile.NamedTemporaryFile(suffix='.db', delete=False) as tmp_db:
        db_url = f"sqlite:///{tmp_db.name}"
        db_manager = DatabaseManager(database_url=db_url)
        
        # Add test data
        db_manager.add_to_watchlist(
            stock_code='000001',
            stock_name='平安银行',
            target_price=15.5
        )
        
        # Create auto backup
        backup_path = db_manager.auto_backup_watchlist()
        assert Path(backup_path).exists(), "Auto backup file should exist"
        
        # Verify backup contains data
        with open(backup_path, 'r', encoding='utf-8') as f:
            backup_data = json.load(f)
        
        assert len(backup_data) == 1, "Backup should have 1 item"
        assert backup_data[0]['stock_code'] == '000001', "Backup should contain correct data"
        
        # Clean up
        Path(tmp_db.name).unlink()
        Path(backup_path).unlink()
        
        print("✅ Auto backup test passed!")


if __name__ == '__main__':
    test_export_import_watchlist()
    test_merge_import()
    test_auto_backup()
    print("\n🎉 All tests passed successfully!")
