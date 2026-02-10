"""
SIAPS Web Package
Flask application for web deployment
"""
import sys
from pathlib import Path

# Add project root to Python path
ROOT_DIR = Path(__file__).parent.parent.parent
sys.path.insert(0, str(ROOT_DIR))

# Import Flask app from run_web_ui.py
from run_web_ui import app

__all__ = ['app']
