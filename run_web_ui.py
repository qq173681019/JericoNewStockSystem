#!/usr/bin/env python3
"""
SIAPS Web UI Launcher
启动 Web 版本的股票智能分析预测系统
"""
import sys
import webbrowser
import time
from pathlib import Path
from threading import Timer

# Add project root to Python path
ROOT_DIR = Path(__file__).parent
sys.path.insert(0, str(ROOT_DIR))

from web_ui.app import run_server
from src.utils import setup_logger

logger = setup_logger()


def open_browser(url='http://127.0.0.1:5000', delay=2.0):
    """
    Open browser after a short delay
    
    Args:
        url: URL to open
        delay: Delay in seconds before opening browser
    """
    def _open():
        try:
            webbrowser.open(url)
            logger.info(f"Opened browser: {url}")
        except Exception as e:
            logger.warning(f"Could not open browser automatically: {e}")
            logger.info(f"Please manually open: {url}")
    
    Timer(delay, _open).start()


def main():
    """Main entry point for Web UI"""
    print("=" * 60)
    print("  SIAPS - 股票智能分析预测系统 (Web UI)")
    print("  Stock Intelligent Analysis & Prediction System")
    print("=" * 60)
    print()
    print("正在启动 Web 服务器...")
    print()
    print("服务器地址: http://127.0.0.1:5000")
    print("按 Ctrl+C 停止服务器")
    print()
    print("=" * 60)
    
    # Open browser automatically
    open_browser()
    
    try:
        # Run Flask server
        run_server(host='127.0.0.1', port=5000, debug=False)
    except KeyboardInterrupt:
        print("\n")
        print("=" * 60)
        print("服务器已停止")
        print("=" * 60)
        sys.exit(0)
    except Exception as e:
        logger.error(f"Server error: {str(e)}", exc_info=True)
        print(f"\n错误: {str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    main()
