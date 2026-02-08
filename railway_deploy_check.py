#!/usr/bin/env python3
"""
Railway Deployment Verification Script
Checks if all required files and configurations are in place for Railway deployment
"""

import os
import sys
import json
from pathlib import Path

def check_file_exists(filepath, description):
    """Check if a file exists"""
    if os.path.exists(filepath):
        print(f"✅ {description}: {filepath}")
        return True
    else:
        print(f"❌ {description} NOT FOUND: {filepath}")
        return False

def check_directory_exists(dirpath, description):
    """Check if a directory exists"""
    if os.path.isdir(dirpath):
        print(f"✅ {description}: {dirpath}")
        return True
    else:
        print(f"❌ {description} NOT FOUND: {dirpath}")
        return False

def verify_railway_config():
    """Verify railway.json configuration"""
    try:
        with open('railway.json', 'r') as f:
            config = json.load(f)
        
        # Check builder
        if config.get('build', {}).get('builder') == 'DOCKERFILE':
            print("✅ Railway configured to use Dockerfile")
        else:
            print("⚠️  Railway not configured to use Dockerfile")
            return False
        
        # Check healthcheck
        if 'healthcheckPath' in config.get('deploy', {}):
            print(f"✅ Healthcheck configured: {config['deploy']['healthcheckPath']}")
        else:
            print("⚠️  No healthcheck configured")
        
        return True
    except Exception as e:
        print(f"❌ Error reading railway.json: {e}")
        return False

def verify_requirements():
    """Verify requirements-prod.txt has essential packages"""
    try:
        with open('requirements-prod.txt', 'r') as f:
            content = f.read()
        
        required_packages = ['Flask', 'gunicorn', 'pandas']
        missing = []
        
        for pkg in required_packages:
            if pkg.lower() in content.lower():
                print(f"✅ Required package found: {pkg}")
            else:
                print(f"❌ Required package missing: {pkg}")
                missing.append(pkg)
        
        return len(missing) == 0
    except Exception as e:
        print(f"❌ Error reading requirements-prod.txt: {e}")
        return False

def main():
    """Main verification function"""
    print("=" * 70)
    print("Railway Deployment Verification")
    print("=" * 70)
    print()
    
    checks = []
    
    # Check essential files
    print("📁 Checking essential files...")
    checks.append(check_file_exists('Dockerfile', 'Dockerfile'))
    checks.append(check_file_exists('railway.json', 'Railway config'))
    checks.append(check_file_exists('requirements-prod.txt', 'Production requirements'))
    checks.append(check_file_exists('app.py', 'Application entry point'))
    checks.append(check_file_exists('run_web_ui.py', 'Flask application'))
    checks.append(check_file_exists('.dockerignore', 'Docker ignore file'))
    print()
    
    # Check directories
    print("📁 Checking directories...")
    checks.append(check_directory_exists('src', 'Source directory'))
    checks.append(check_directory_exists('web_ui', 'Web UI directory'))
    checks.append(check_directory_exists('web_ui/templates', 'Templates directory'))
    checks.append(check_directory_exists('web_ui/static', 'Static files directory'))
    print()
    
    # Check nixpacks.toml doesn't exist
    print("🔍 Checking for deprecated files...")
    if os.path.exists('nixpacks.toml'):
        print("⚠️  WARNING: nixpacks.toml exists - Railway might use Nixpacks instead of Docker")
        print("   Consider removing this file for reliable Docker-based deployment")
        checks.append(False)
    else:
        print("✅ No nixpacks.toml found (good - using Docker)")
        checks.append(True)
    print()
    
    # Verify configurations
    print("⚙️  Verifying configurations...")
    checks.append(verify_railway_config())
    print()
    
    print("📦 Verifying dependencies...")
    checks.append(verify_requirements())
    print()
    
    # Summary
    print("=" * 70)
    passed = sum(checks)
    total = len(checks)
    
    if passed == total:
        print(f"✅ ALL CHECKS PASSED ({passed}/{total})")
        print()
        print("🚀 Your project is ready for Railway deployment!")
        print()
        print("Next steps:")
        print("1. Commit and push your code to GitHub")
        print("2. Go to Railway.app and create a new project")
        print("3. Connect your GitHub repository")
        print("4. Railway will automatically detect and use the Dockerfile")
        print("5. Wait for deployment to complete (~3-5 minutes)")
        print("6. Generate a domain in Railway settings")
        print("7. Access your deployed application!")
        return 0
    else:
        print(f"❌ SOME CHECKS FAILED ({passed}/{total})")
        print()
        print("Please fix the issues above before deploying to Railway.")
        return 1

if __name__ == '__main__':
    sys.exit(main())
