#!/usr/bin/env python3
"""
Flask application entry point for Vercel and Railway deployment
This file imports the Flask app from run_web_ui.py for serverless deployment
"""

# Import the Flask app from run_web_ui.py
from run_web_ui import app

# Export the app for Vercel/Railway
# This is the entry point that Vercel expects
if __name__ == "__main__":
    # For local development, you can run this directly
    app.run()
