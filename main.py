#!/usr/bin/env python3
"""
SIAPS - Stock Intelligent Analysis & Prediction System
Main entry point with smart environment detection
"""
import sys
import os
from pathlib import Path

# Add project root to Python path
ROOT_DIR = Path(__file__).parent
sys.path.insert(0, str(ROOT_DIR))

# Detect production environment
is_production = (
    os.getenv('RAILWAY_ENVIRONMENT') or 
    os.getenv('VERCEL') or 
    os.getenv('PRODUCTION') or
    os.getenv('DYNO')  # Heroku
)

def main():
    """Main entry point with environment detection"""
    if is_production:
        # Production: Run Flask Web API
        print("🌐 Production environment detected - starting Web API")
        from run_web_ui import app
        port = int(os.getenv('PORT', 5000))
        app.run(host='0.0.0.0', port=port, debug=False)
    else:
        # Development: Run Desktop GUI
        print("💻 Development environment detected - starting Desktop GUI")
        try:
            from src.gui import run_app
            from src.utils import setup_logger
            logger = setup_logger()
            logger.info("Starting SIAPS application...")
            run_app()
        except ImportError as e:
            print(f"❌ GUI not available: {e}")
            print("💡 For web interface, run: python run_web_ui.py")
            sys.exit(1)
        except Exception as e:
            print(f"❌ Application error: {e}")
            sys.exit(1)

if __name__ == "__main__":
    main()
