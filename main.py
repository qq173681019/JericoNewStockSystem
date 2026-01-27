#!/usr/bin/env python3
"""
SIAPS - Stock Intelligent Analysis & Prediction System
Main entry point
"""
import sys
from pathlib import Path

# Add project root to Python path
ROOT_DIR = Path(__file__).parent
sys.path.insert(0, str(ROOT_DIR))

from src.gui import run_app
from src.utils import setup_logger

logger = setup_logger()


def main():
    """Main entry point"""
    logger.info("Starting SIAPS application...")
    try:
        run_app()
    except Exception as e:
        logger.error(f"Application error: {str(e)}", exc_info=True)
        sys.exit(1)


if __name__ == "__main__":
    main()
