#!/usr/bin/env python3
"""
SIAPS - Stock Intelligent Analysis & Prediction System
Main entry point - supports both GUI (local) and Web API (production)
"""
import sys
import os
from pathlib import Path

# Add project root to Python path
ROOT_DIR = Path(__file__).parent
sys.path.insert(0, str(ROOT_DIR))

from src.utils import setup_logger

logger = setup_logger()


def main():
    """Main entry point - decides between GUI and Web mode"""
    # Check if running in cloud environment (Railway, Vercel, etc.)
    # Treat environment variable as set if it exists and is not explicitly disabled
    railway = os.getenv('RAILWAY_ENVIRONMENT', '').lower() not in ('', '0', 'false', 'no', 'off')
    vercel = os.getenv('VERCEL', '').lower() not in ('', '0', 'false', 'no', 'off')
    production = os.getenv('PRODUCTION', '').lower() not in ('', '0', 'false', 'no', 'off')
    is_production = railway or vercel or production
    
    if is_production:
        # Production mode: Run Flask Web API
        logger.info("Starting SIAPS in Web API mode (production)...")
        try:
            from run_web_ui import app
            port = int(os.getenv('PORT', 5000))
            app.run(host='0.0.0.0', port=port)
        except Exception as e:
            logger.error(f"Web API startup error: {str(e)}", exc_info=True)
            sys.exit(1)
    else:
        # Local mode: Run Desktop GUI
        logger.info("Starting SIAPS in GUI mode (local)...")
        try:
            from src.gui import run_app
            run_app()
        except ImportError as e:
            logger.error(
                "GUI dependencies not installed. "
                "Install with: pip install customtkinter matplotlib\n"
                "Or run the Web UI with: python run_web_ui.py"
            )
            sys.exit(1)
        except Exception as e:
            logger.error(f"Application error: {str(e)}", exc_info=True)
            sys.exit(1)


if __name__ == "__main__":
    main()
