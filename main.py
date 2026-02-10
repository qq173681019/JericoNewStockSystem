#!/usr/bin/env python3
"""
SIAPS - Stock Intelligent Analysis & Prediction System
Main entry point
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
    """Main entry point"""
    # Check if running in web/server mode (Railway, Vercel, etc.)
    is_web_mode = os.environ.get('RAILWAY_ENVIRONMENT') or \
                  os.environ.get('VERCEL') or \
                  os.environ.get('WEB_MODE', '').lower() == 'true'
    
    if is_web_mode:
        logger.info("Starting SIAPS in WEB mode...")
        try:
            # Import and run web app
            from src.web import app
            port = int(os.environ.get('PORT', 5000))
            app.run(host='0.0.0.0', port=port)
        except Exception as e:
            logger.error(f"Web application error: {str(e)}", exc_info=True)
            sys.exit(1)
    else:
        logger.info("Starting SIAPS in GUI mode...")
        try:
            # Import and run GUI app
            from src.gui import run_app
            run_app()
        except ImportError as e:
            logger.error(f"GUI dependencies not installed. Install with: pip install customtkinter")
            logger.error(f"Or run in web mode by setting environment variable: WEB_MODE=true")
            sys.exit(1)
        except Exception as e:
            logger.error(f"Application error: {str(e)}", exc_info=True)
            sys.exit(1)


if __name__ == "__main__":
    main()
