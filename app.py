#!/usr/bin/env python3
"""
Flask application entry point for cloud deployment (Railway, Vercel, etc.)
"""
import os
from run_web_ui import app

# Export the app for serverless platforms
# This is automatically imported by platforms like Vercel

if __name__ == "__main__":
    # For Railway and other PaaS platforms
    port = int(os.getenv('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
