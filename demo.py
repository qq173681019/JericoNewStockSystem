#!/usr/bin/env python3
"""
SIAPS Demo Script
Demonstrates the core functionality without GUI
"""
import sys
from pathlib import Path
from datetime import datetime

# Add project root to path
ROOT_DIR = Path(__file__).parent
sys.path.insert(0, str(ROOT_DIR))

print("=" * 60)
print("SIAPS - Stock Intelligent Analysis & Prediction System")
print("=" * 60)
print()

# 1. Test Configuration
print("1. Testing Configuration...")
from config import APP_NAME, APP_VERSION, DATABASE_URL, THEME
print(f"   App Name: {APP_NAME}")
print(f"   Version: {APP_VERSION}")
print(f"   Database: {DATABASE_URL}")
print(f"   Theme: {THEME}")
print("   ✓ Configuration loaded successfully")
print()

# 2. Test Utils
print("2. Testing Utilities...")
from src.utils import validate_stock_code, get_timestamp
test_codes = ["000001", "600000", "ABC123", "12345"]
for code in test_codes:
    valid = validate_stock_code(code)
    status = "✓" if valid else "✗"
    print(f"   {status} Code '{code}': {'Valid' if valid else 'Invalid'}")
print(f"   Current time: {get_timestamp()}")
print("   ✓ Utilities working")
print()

# 3. Test Database
print("3. Testing Database...")
from src.database import DatabaseManager
db = DatabaseManager("sqlite:///:memory:")
print("   ✓ Database initialized")

# Add sample data to watchlist
print("   Adding stocks to watchlist...")
db.add_to_watchlist("000001", "平安银行", target_price=15.0, stop_loss_price=12.0)
db.add_to_watchlist("600000", "浦发银行", target_price=10.0, stop_loss_price=8.0)
watchlist = db.get_watchlist()
print(f"   Watchlist contains {len(watchlist)} stocks:")
for item in watchlist:
    print(f"     - {item.stock_code}: {item.stock_name} (Target: ¥{item.target_price})")
print("   ✓ Watchlist operations working")
print()

# Add sample predictions
print("   Adding sample predictions...")
db.add_prediction(
    stock_code="000001",
    stock_name="平安银行",
    prediction_type="short_term",
    predicted_date=datetime.now(),
    prediction_value=15.5,
    prediction_direction="up",
    confidence_score=0.85
)
db.add_prediction(
    stock_code="600000",
    stock_name="浦发银行",
    prediction_type="long_term",
    predicted_date=datetime.now(),
    prediction_value=12.0,
    prediction_direction="neutral",
    confidence_score=0.70
)
history = db.get_prediction_history()
print(f"   Prediction history contains {len(history)} records:")
for pred in history:
    print(f"     - {pred.stock_code}: {pred.prediction_direction} "
          f"(Confidence: {pred.confidence_score:.0%})")
print("   ✓ Prediction history working")
print()

# 4. Test Data Acquisition
print("4. Testing Data Acquisition...")
from src.data_acquisition import get_data_fetcher
fetcher = get_data_fetcher("akshare")
if fetcher:
    print("   ✓ AKShare fetcher initialized")
    print("   Note: Actual data fetching requires network and AKShare installation")
else:
    print("   ✗ Failed to initialize fetcher")
print()

# 5. Project Structure Summary
print("5. Project Structure Summary...")
print("   Source modules:")
print("     ✓ config/ - Configuration management")
print("     ✓ src/data_acquisition/ - Data fetching (AKShare)")
print("     ✓ src/database/ - SQLAlchemy ORM")
print("     ✓ src/gui/ - CustomTkinter GUI")
print("     ✓ src/utils/ - Logging and utilities")
print("     ○ src/data_processing/ - Placeholder for Phase 2")
print("     ○ src/prediction_models/ - Placeholder for Phase 2")
print("     ○ src/business_logic/ - Placeholder for Phase 2")
print()

print("=" * 60)
print("✓ SIAPS Core Framework Initialized Successfully!")
print("=" * 60)
print()
print("Next Steps:")
print("1. Install dependencies: pip install -r requirements.txt")
print("2. Copy .env.example to .env and configure")
print("3. Run the application: python main.py")
print("4. Implement Phase 2 features (technical indicators, ML models)")
print()
print("For more information, see docs/DEVELOPMENT.md")
