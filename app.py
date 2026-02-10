#!/usr/bin/env python3
"""
Flask application entry point for Railway/Vercel deployment
This file imports the Flask app from run_web_ui.py for production deployment
"""
import os

# Import the Flask app from run_web_ui.py
from run_web_ui import app

if __name__ == "__main__":
    # Get port from environment (Railway sets $PORT automatically)
    port = int(os.getenv('PORT', 5000))
    
    # Run the app (Railway requires host='0.0.0.0')
    app.run(host='0.0.0.0', port=port, debug=False)
