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

def main():
    """Main entry point with environment detection"""
    # Check if running in cloud environment (Railway, Vercel, Heroku, etc.)
    # Treat environment variable as set if it exists and is not explicitly disabled
    railway = os.getenv('RAILWAY_ENVIRONMENT', '').lower() not in ('', '0', 'false', 'no', 'off')
    vercel = os.getenv('VERCEL', '').lower() not in ('', '0', 'false', 'no', 'off')
    production = os.getenv('PRODUCTION', '').lower() not in ('', '0', 'false', 'no', 'off')
    dyno = os.getenv('DYNO', '').lower() not in ('', '0', 'false', 'no', 'off')
    is_production = railway or vercel or production or dyno
    
    if is_production:
        # Production mode: Run Flask Web API
        # Note: Using print() instead of logger for production to avoid logger initialization overhead
        # Flask provides its own logging infrastructure
        print("🌐 Production environment detected - starting Web API")
        try:
            from run_web_ui import app
            port = int(os.getenv('PORT', 5000))
            app.run(host='0.0.0.0', port=port, debug=False)
        except Exception as e:
            print(f"❌ Web API startup error: {str(e)}")
            sys.exit(1)
    else:
        # Local mode: Run Desktop GUI
        print("💻 Development environment detected - starting Desktop GUI")
        try:
            from src.utils import setup_logger
            logger = setup_logger()
            logger.info("Starting SIAPS application in GUI mode (local)...")
            
            from src.gui import run_app
            run_app()
        except ImportError as e:
            print(f"❌ GUI not available: {e}")
            print("💡 For web interface, run: python run_web_ui.py")
            print("   Install GUI dependencies with: pip install customtkinter matplotlib")
            sys.exit(1)
        except Exception as e:
            print(f"❌ GUI startup error: {e}")
            sys.exit(1)

if __name__ == "__main__":
    main()
