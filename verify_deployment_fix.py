#!/usr/bin/env python3
"""
Verification script for Vercel deployment fix
This script checks that the requirements files are properly configured
"""

import os
import sys

def read_requirements(filename):
    """Read and parse a requirements file"""
    if not os.path.exists(filename):
        return None
    
    with open(filename, 'r') as f:
        lines = f.readlines()
    
    packages = []
    for line in lines:
        line = line.strip()
        # Skip comments and empty lines
        if line and not line.startswith('#'):
            # Extract package name (before >= or ==)
            pkg = line.split('>=')[0].split('==')[0].strip()
            packages.append(pkg)
    
    return packages

def main():
    print("=" * 70)
    print("Vercel Deployment Fix Verification")
    print("=" * 70)
    print()
    
    # Check files exist
    files = {
        'requirements.txt': 'Production (Vercel uses this)',
        'requirements-dev.txt': 'Development (full ML features)',
        'requirements-prod.txt': 'Production backup (legacy)',
        'vercel.json': 'Vercel configuration',
        'app.py': 'Vercel entry point'
    }
    
    print("1. Checking required files...")
    all_exist = True
    for filename, description in files.items():
        exists = os.path.exists(filename)
        status = "✓" if exists else "✗"
        print(f"   {status} {filename:25} - {description}")
        if not exists:
            all_exist = False
    print()
    
    if not all_exist:
        print("❌ Some required files are missing!")
        return 1
    
    # Check requirements.txt (production)
    print("2. Checking production requirements (requirements.txt)...")
    prod_packages = read_requirements('requirements.txt')
    
    # Heavy packages that should NOT be in production
    heavy_packages = ['torch', 'tensorflow', 'prophet', 'customtkinter', 'matplotlib']
    
    found_heavy = [pkg for pkg in heavy_packages if pkg.lower() in [p.lower() for p in prod_packages]]
    
    if found_heavy:
        print(f"   ✗ Found heavy packages in production requirements: {', '.join(found_heavy)}")
        print(f"   ❌ This will cause buffer overflow on Vercel!")
        return 1
    else:
        print(f"   ✓ No heavy ML packages found (good!)")
    
    print(f"   ✓ Total packages: {len(prod_packages)}")
    print(f"   ✓ Packages: {', '.join(prod_packages[:5])}...")
    print()
    
    # Check requirements-dev.txt (development)
    print("3. Checking development requirements (requirements-dev.txt)...")
    dev_packages = read_requirements('requirements-dev.txt')
    
    found_heavy_in_dev = [pkg for pkg in heavy_packages if pkg.lower() in [p.lower() for p in dev_packages]]
    
    if not found_heavy_in_dev:
        print(f"   ⚠ No ML packages found in development requirements")
        print(f"   This might be intentional, but usually dev should have ML packages")
    else:
        print(f"   ✓ Found ML packages in dev: {', '.join(found_heavy_in_dev)}")
    
    print(f"   ✓ Total packages: {len(dev_packages)}")
    print()
    
    # Check vercel.json
    print("4. Checking Vercel configuration...")
    import json
    with open('vercel.json', 'r') as f:
        config = json.load(f)
    
    entry_point = config.get('builds', [{}])[0].get('src')
    if entry_point == 'app.py':
        print(f"   ✓ Entry point is correctly set to: {entry_point}")
    else:
        print(f"   ✗ Entry point is: {entry_point} (should be app.py)")
        return 1
    print()
    
    # Summary
    print("=" * 70)
    print("✅ VERIFICATION PASSED!")
    print("=" * 70)
    print()
    print("Summary:")
    print(f"  • Production requirements: {len(prod_packages)} packages (lightweight)")
    print(f"  • Development requirements: {len(dev_packages)} packages (full featured)")
    print(f"  • Heavy packages removed from production: {', '.join(heavy_packages)}")
    print(f"  • Vercel entry point: {entry_point}")
    print()
    print("The deployment should now work without buffer overflow errors!")
    print()
    print("Next steps:")
    print("  1. Push this branch to GitHub")
    print("  2. Deploy to Vercel")
    print("  3. Check deployment logs for success")
    print()
    
    return 0

if __name__ == '__main__':
    sys.exit(main())
