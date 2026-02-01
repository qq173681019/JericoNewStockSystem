"""
SIAPS - Stock Intelligent Analysis & Prediction System
Configuration module
"""
import os
from pathlib import Path

# Try to load environment variables, but don't fail if dotenv is not installed
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    print("Warning: python-dotenv not installed. Using default configuration.")
    print("To install: pip install python-dotenv")

# Project root directory
ROOT_DIR = Path(__file__).parent.parent.parent
SRC_DIR = ROOT_DIR / "src"

# Use /tmp for data in cloud environments (Railway, Vercel, etc.)
# These platforms have read-only file systems except for /tmp
IS_CLOUD_ENV = (
    os.getenv("RAILWAY_ENVIRONMENT") is not None or 
    os.getenv("VERCEL") is not None or 
    os.getenv("RENDER") is not None
)
if IS_CLOUD_ENV:
    DATA_DIR = Path("/tmp/data")
    LOGS_DIR = Path("/tmp/logs")
    MODELS_DIR = Path("/tmp/models")
else:
    DATA_DIR = ROOT_DIR / "data"
    LOGS_DIR = ROOT_DIR / "logs"
    MODELS_DIR = ROOT_DIR / "models"

# Create necessary directories
for directory in [DATA_DIR, LOGS_DIR, MODELS_DIR, DATA_DIR / "cache", MODELS_DIR / "saved"]:
    directory.mkdir(parents=True, exist_ok=True)

# Application settings
APP_NAME = os.getenv("APP_NAME", "SIAPS")
APP_VERSION = os.getenv("APP_VERSION", "0.1.0")
DEBUG = os.getenv("DEBUG", "True").lower() == "true"

# Data source settings
AKSHARE_ENABLED = os.getenv("AKSHARE_ENABLED", "True").lower() == "true"
TUSHARE_ENABLED = os.getenv("TUSHARE_ENABLED", "False").lower() == "true"
TUSHARE_TOKEN = os.getenv("TUSHARE_TOKEN", "")

# Database settings
DATABASE_URL = os.getenv("DATABASE_URL", f"sqlite:///{DATA_DIR}/siaps.db")

# GUI settings
THEME = os.getenv("THEME", "dark")
WINDOW_WIDTH = int(os.getenv("WINDOW_WIDTH", "1280"))
WINDOW_HEIGHT = int(os.getenv("WINDOW_HEIGHT", "800"))

# Model settings
MODEL_CACHE_DIR = MODELS_DIR / "saved"
DATA_CACHE_DIR = DATA_DIR / "cache"

# Logging settings
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
LOG_FILE = LOGS_DIR / "siaps.log"
