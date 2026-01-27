"""
Test database models
"""
import sys
from pathlib import Path
from datetime import datetime

# Add project root to path
ROOT_DIR = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT_DIR))

from src.database import DatabaseManager


def test_database_initialization():
    """Test database initialization"""
    # Use in-memory database for testing
    db = DatabaseManager("sqlite:///:memory:")
    assert db is not None
    assert db.engine is not None
    print("✓ Database initialization test passed")


def test_watchlist_operations():
    """Test watchlist CRUD operations"""
    db = DatabaseManager("sqlite:///:memory:")
    
    # Add to watchlist
    db.add_to_watchlist(
        stock_code="000001",
        stock_name="平安银行",
        target_price=15.0,
        stop_loss_price=12.0,
        stop_profit_price=18.0
    )
    
    # Get watchlist
    items = db.get_watchlist()
    assert len(items) == 1
    assert items[0].stock_code == "000001"
    assert items[0].stock_name == "平安银行"
    
    print("✓ Watchlist operations test passed")


def test_prediction_history():
    """Test prediction history operations"""
    db = DatabaseManager("sqlite:///:memory:")
    
    # Add prediction
    db.add_prediction(
        stock_code="000001",
        stock_name="平安银行",
        prediction_type="short_term",
        predicted_date=datetime.now(),
        prediction_value=15.5,
        prediction_direction="up",
        confidence_score=0.85
    )
    
    # Get prediction history
    history = db.get_prediction_history(stock_code="000001")
    assert len(history) == 1
    assert history[0].stock_code == "000001"
    assert history[0].prediction_direction == "up"
    
    print("✓ Prediction history test passed")


if __name__ == "__main__":
    test_database_initialization()
    test_watchlist_operations()
    test_prediction_history()
    print("\n✓ All database tests passed!")
