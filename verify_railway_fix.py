#!/usr/bin/env python3
"""
Verification script for Railway deployment fix
Tests that the ROOT_DIR path calculation bug has been fixed
"""
import sys
import os
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent))

def test_root_dir_calculation():
    """Test that ROOT_DIR is calculated correctly"""
    print("=" * 60)
    print("TEST 1: ROOT_DIR Calculation")
    print("=" * 60)
    
    from config import settings
    
    expected_root = Path(__file__).parent.resolve()
    actual_root = settings.ROOT_DIR.resolve()
    
    print(f"Expected ROOT_DIR: {expected_root}")
    print(f"Actual ROOT_DIR:   {actual_root}")
    
    if expected_root == actual_root:
        print("✅ PASS: ROOT_DIR is correct")
        return True
    else:
        print("❌ FAIL: ROOT_DIR mismatch!")
        return False

def test_local_environment():
    """Test local environment configuration"""
    print("\n" + "=" * 60)
    print("TEST 2: Local Environment Configuration")
    print("=" * 60)
    
    # Clear any cloud env vars
    for var in ['RAILWAY_PUBLIC_DOMAIN', 'VERCEL', 'RENDER']:
        if var in os.environ:
            del os.environ[var]
    
    # Reload settings
    import importlib
    from config import settings
    importlib.reload(settings)
    
    print(f"IS_CLOUD_ENV: {settings.IS_CLOUD_ENV}")
    print(f"DATA_DIR: {settings.DATA_DIR}")
    
    if not settings.IS_CLOUD_ENV:
        print("✅ PASS: Local environment detected correctly")
        return True
    else:
        print("❌ FAIL: Should not detect cloud environment")
        return False

def test_railway_environment():
    """Test Railway environment configuration"""
    print("\n" + "=" * 60)
    print("TEST 3: Railway Environment Configuration")
    print("=" * 60)
    
    # Set Railway environment variable
    os.environ['RAILWAY_PUBLIC_DOMAIN'] = 'test.railway.app'
    
    # Reload settings
    import importlib
    from config import settings
    importlib.reload(settings)
    
    print(f"IS_CLOUD_ENV: {settings.IS_CLOUD_ENV}")
    print(f"DATA_DIR: {settings.DATA_DIR}")
    
    success = True
    if not settings.IS_CLOUD_ENV:
        print("❌ FAIL: Railway environment not detected")
        success = False
    else:
        print("✅ PASS: Railway environment detected")
    
    if str(settings.DATA_DIR) != "/tmp/data":
        print(f"❌ FAIL: DATA_DIR should be /tmp/data, got {settings.DATA_DIR}")
        success = False
    else:
        print("✅ PASS: DATA_DIR set to /tmp/data")
    
    # Cleanup
    del os.environ['RAILWAY_PUBLIC_DOMAIN']
    
    return success

def test_app_import():
    """Test that the Flask app can be imported"""
    print("\n" + "=" * 60)
    print("TEST 4: Flask App Import")
    print("=" * 60)
    
    try:
        from run_web_ui import app
        print(f"✅ PASS: App imported successfully")
        
        routes = [rule.rule for rule in app.url_map.iter_rules()]
        print(f"✅ PASS: Found {len(routes)} routes")
        
        if '/' in routes and '/api/health' in routes:
            print("✅ PASS: Required routes (/, /api/health) exist")
            return True
        else:
            print("❌ FAIL: Missing required routes")
            return False
    except Exception as e:
        print(f"❌ FAIL: Could not import app: {e}")
        return False

def main():
    """Run all verification tests"""
    print("\n" + "🔍 " * 20)
    print("Railway Deployment Fix Verification")
    print("🔍 " * 20 + "\n")
    
    tests = [
        test_root_dir_calculation,
        test_local_environment,
        test_railway_environment,
        test_app_import
    ]
    
    results = []
    for test in tests:
        try:
            result = test()
            results.append(result)
        except Exception as e:
            print(f"❌ TEST FAILED WITH EXCEPTION: {e}")
            results.append(False)
    
    # Summary
    print("\n" + "=" * 60)
    print("VERIFICATION SUMMARY")
    print("=" * 60)
    
    passed = sum(results)
    total = len(results)
    
    print(f"Tests Passed: {passed}/{total}")
    
    if all(results):
        print("\n🎉 ALL TESTS PASSED!")
        print("✅ The Railway deployment fix is working correctly")
        print("✅ Ready to deploy to Railway")
        return 0
    else:
        print("\n❌ SOME TESTS FAILED")
        print("⚠️  Please review the failures above")
        return 1

if __name__ == "__main__":
    sys.exit(main())
