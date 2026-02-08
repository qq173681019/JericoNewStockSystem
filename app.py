#!/usr/bin/env python3
"""
Flask application entry point for Vercel deployment
This file imports the Flask app from run_web_ui.py for serverless deployment
"""

# Import the Flask app from run_web_ui.py
from run_web_ui import app

# Export the app for Vercel
# This is the entry point that Vercel expects
# The app object is automatically imported by the serverless platform

if __name__ == "__main__":
    # For local testing only (not used on Vercel)
    # On serverless platforms, the app object is imported directly
    app.run()
