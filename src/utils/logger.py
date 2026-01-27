"""
SIAPS - Stock Intelligent Analysis & Prediction System
Utilities module
"""
import logging
from pathlib import Path
from datetime import datetime
import sys

# Add project root to Python path
ROOT_DIR = Path(__file__).parent.parent.parent
sys.path.insert(0, str(ROOT_DIR))

from config.settings import LOG_FILE, LOG_LEVEL


def setup_logger(name: str = "SIAPS", log_file: Path = LOG_FILE, level: str = LOG_LEVEL):
    """
    Setup logger with file and console handlers
    
    Args:
        name: Logger name
        log_file: Path to log file
        level: Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
    
    Returns:
        logging.Logger: Configured logger instance
    """
    logger = logging.getLogger(name)
    logger.setLevel(getattr(logging, level.upper()))
    
    # Create formatters
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    
    # File handler
    log_file.parent.mkdir(parents=True, exist_ok=True)
    file_handler = logging.FileHandler(log_file, encoding='utf-8')
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(formatter)
    
    # Console handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(formatter)
    
    # Add handlers
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)
    
    return logger


def validate_stock_code(code: str) -> bool:
    """
    Validate Chinese stock code format
    
    Args:
        code: Stock code to validate
    
    Returns:
        bool: True if valid, False otherwise
    """
    if not code:
        return False
    
    # Remove spaces
    code = code.strip()
    
    # Check length (6 digits for Chinese stocks)
    if len(code) != 6:
        return False
    
    # Check if all characters are digits
    if not code.isdigit():
        return False
    
    return True


def get_timestamp() -> str:
    """
    Get current timestamp as string
    
    Returns:
        str: Current timestamp in format YYYY-MM-DD HH:MM:SS
    """
    return datetime.now().strftime('%Y-%m-%d %H:%M:%S')
