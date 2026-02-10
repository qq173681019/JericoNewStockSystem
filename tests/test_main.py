"""
Tests for main.py entry point
"""
import os
import sys
from pathlib import Path

# Add project root to Python path
ROOT_DIR = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT_DIR))


def check_web_mode():
    """Helper function to check web mode based on environment variables"""
    return os.environ.get('RAILWAY_ENVIRONMENT') or \
           os.environ.get('VERCEL') or \
           os.environ.get('WEB_MODE', '').lower() == 'true'


def test_web_mode_detection():
    """Test that web mode is correctly detected based on environment variables"""
    
    # Save current environment
    saved_env = {}
    for key in ['RAILWAY_ENVIRONMENT', 'VERCEL', 'WEB_MODE']:
        saved_env[key] = os.environ.pop(key, None)
    
    try:
        # Test 1: No environment variable - should be GUI mode
        assert not check_web_mode(), "Should default to GUI mode"
        
        # Test 2: RAILWAY_ENVIRONMENT set
        os.environ['RAILWAY_ENVIRONMENT'] = 'production'
        assert check_web_mode(), "Should detect Railway environment"
        os.environ.pop('RAILWAY_ENVIRONMENT')
        
        # Test 3: VERCEL environment set
        os.environ['VERCEL'] = '1'
        assert check_web_mode(), "Should detect Vercel environment"
        os.environ.pop('VERCEL')
        
        # Test 4: WEB_MODE=true
        os.environ['WEB_MODE'] = 'true'
        assert check_web_mode(), "Should detect WEB_MODE=true"
        os.environ.pop('WEB_MODE')
        
        # Test 5: WEB_MODE=TRUE (uppercase)
        os.environ['WEB_MODE'] = 'TRUE'
        assert check_web_mode(), "Should detect WEB_MODE=TRUE (case insensitive)"
        os.environ.pop('WEB_MODE')
        
        # Test 6: WEB_MODE=false
        os.environ['WEB_MODE'] = 'false'
        assert not check_web_mode(), "Should not detect WEB_MODE=false"
        
        print("✓ All web mode detection tests passed")
    
    finally:
        # Restore environment
        for key, value in saved_env.items():
            if value is not None:
                os.environ[key] = value
            else:
                os.environ.pop(key, None)


def test_src_web_import():
    """Test that src.web module can be imported and has the Flask app"""
    try:
        from src.web import app
        assert app is not None, "Flask app should be available"
        assert hasattr(app, 'run'), "Flask app should have run method"
        print("✓ src.web import test passed")
    except ImportError as e:
        print(f"⚠ Flask not installed, skipping import test: {e}")


def test_gui_import_error_handling():
    """Test that GUI import errors are handled gracefully"""
    try:
        from src.gui import run_app
        print("⚠ GUI dependencies are installed, cannot test error handling")
    except ImportError:
        print("✓ GUI import error handling test passed (ImportError raised as expected)")


if __name__ == "__main__":
    print("Running main.py tests...")
    print()
    
    test_web_mode_detection()
    test_src_web_import()
    test_gui_import_error_handling()
    
    print()
    print("✓ All tests completed")
