#!/usr/bin/env python3
"""
SIAPS - Web UI Launcher
Launch the web-based user interface
"""
import sys
from pathlib import Path

# Add project root to Python path
ROOT_DIR = Path(__file__).parent
sys.path.insert(0, str(ROOT_DIR))

from web.app import run_web_server
from src.utils import setup_logger

logger = setup_logger(__name__)


def main():
    """Main entry point for web UI"""
    logger.info("Starting SIAPS Web UI...")
    print("=" * 60)
    print("SIAPS - Stock Intelligent Analysis & Prediction System")
    print("=" * 60)
    print()
    print("🚀 Starting web server...")
    print("📱 Open your browser and navigate to: http://127.0.0.1:5000")
    print("💡 Press Ctrl+C to stop the server")
    print()
    
    try:
        # Use None to let run_web_server use the DEBUG setting from config
        run_web_server(host='127.0.0.1', port=5000, debug=None)
    except KeyboardInterrupt:
        print("\n\n👋 Shutting down server...")
        logger.info("Server stopped by user")
    except Exception as e:
        logger.error(f"Server error: {str(e)}", exc_info=True)
        sys.exit(1)


if __name__ == "__main__":
    main()
