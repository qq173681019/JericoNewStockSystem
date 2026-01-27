"""
Test utilities module
"""
import sys
from pathlib import Path

# Add project root to path
ROOT_DIR = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT_DIR))

from src.utils import validate_stock_code, get_timestamp


def test_validate_stock_code():
    """Test stock code validation"""
    # Valid codes
    assert validate_stock_code("000001") == True
    assert validate_stock_code("600000") == True
    assert validate_stock_code("300001") == True
    
    # Invalid codes
    assert validate_stock_code("") == False
    assert validate_stock_code("00001") == False  # Too short
    assert validate_stock_code("0000001") == False  # Too long
    assert validate_stock_code("ABC001") == False  # Contains letters
    assert validate_stock_code(None) == False
    
    print("✓ All stock code validation tests passed")


def test_get_timestamp():
    """Test timestamp generation"""
    timestamp = get_timestamp()
    assert isinstance(timestamp, str)
    assert len(timestamp) == 19  # YYYY-MM-DD HH:MM:SS format
    assert timestamp[4] == '-'
    assert timestamp[7] == '-'
    assert timestamp[10] == ' '
    assert timestamp[13] == ':'
    assert timestamp[16] == ':'
    
    print("✓ Timestamp generation test passed")


if __name__ == "__main__":
    test_validate_stock_code()
    test_get_timestamp()
    print("\n✓ All tests passed!")
