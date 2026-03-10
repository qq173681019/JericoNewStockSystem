#!/usr/bin/env python3
"""
Deployment readiness verification script
Checks if all necessary files and configurations are in place for Railway deployment
"""

import os
import sys
from pathlib import Path
import json

def check_file_exists(filepath, description=""):
    """Check if a file exists and report status"""
    path = Path(filepath)
    exists = path.exists()
    status = "✅" if exists else "❌"
    print(f"{status} {description}: {filepath}")
    return exists

def check_content_contains(filepath, content_snippet, description=""):
    """Check if a file contains a specific content snippet"""
    path = Path(filepath)
    if not path.exists():
        print(f"❌ {description}: {filepath} (file does not exist)")
        return False
    
    try:
        content = path.read_text(encoding='utf-8')
        contains = content_snippet in content
        status = "✅" if contains else "❌"
        print(f"{status} {description}: {filepath} (contains '{content_snippet[:30]}...')")
        return contains
    except Exception as e:
        print(f"❌ {description}: {filepath} (error reading file: {e})")
        return False

def main():
    print("=" * 60)
    print("Railway Deployment Readiness Verification")
    print("=" * 60)
    
    project_root = Path(__file__).parent
    os.chdir(project_root)
    
    all_checks = []
    
    print("\n📁 Essential Files:")
    essential_files = [
        ("app.py", "Flask application entry point"),
        ("run_web_ui.py", "Main application backend"),
        ("requirements-prod.txt", "Production dependencies"),
        ("nixpacks.toml", "Nixpacks build configuration"),
        ("railway.json", "Railway platform configuration"),
        ("Procfile", "Start command configuration"),
    ]
    
    for filename, description in essential_files:
        all_checks.append(check_file_exists(filename, description))
    
    print("\nConfiguration Files:")
    config_files = [
        (".railwayignore", "Files to ignore during deployment"),
    ]
    
    for filename, description in config_files:
        all_checks.append(check_file_exists(filename, description))
    
    print("\nContent Verification:")
    content_checks = [
        ("app.py", "from run_web_ui import app", "App import in app.py"),
        ("run_web_ui.py", "import json", "JSON import in run_web_ui.py"),
        ("nixpacks.toml", "gunicorn", "Gunicorn start command in nixpacks.toml"),
        ("railway.json", "gunicorn", "Gunicorn start command in railway.json"),
        ("requirements-prod.txt", "gunicorn", "Gunicorn in production requirements"),
    ]
    
    for filename, content, description in content_checks:
        all_checks.append(check_content_contains(filename, content, description))
    
    print("\nImport Test:")
    try:
        # Temporarily add the project root to Python path
        sys.path.insert(0, str(project_root))
        
        # Try to import the app
        from app import app
        print("SUCCESS: Successfully imported Flask app from app.py")
        import_success = True
        
        # Test that the app has basic routes
        routes = [rule.rule for rule in app.url_map.iter_rules()]
        if '/api/health' in routes:
            print("SUCCESS: Health check route found")
        else:
            print("WARNING: Health check route not found (not critical)")
            
    except Exception as e:
        print(f"ERROR: Failed to import Flask app: {e}")
        import_success = False
    
    all_checks.append(import_success)
    
    print("\n" + "=" * 60)
    passed = sum(all_checks)
    total = len(all_checks)
    print(f"Results: {passed}/{total} checks passed")
    
    if passed == total:
        print("SUCCESS: All checks passed! Your project is ready for Railway deployment.")
        print("\nTo deploy now:")
        print("   1. Go to https://railway.app")
        print("   2. Click 'New Project' -> 'Deploy from GitHub repo'")
        print("   3. Select your repository")
        print("   4. Railway will auto-detect the configuration and deploy")
        return True
    else:
        print("ERROR: Some checks failed. Please fix the issues before deploying.")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)