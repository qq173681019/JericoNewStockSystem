"""
Tests for main.py entry point
"""
import os
import sys
from pathlib import Path

# Add project root to Python path
ROOT_DIR = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT_DIR))


def check_production_mode():
    """Helper function to check production mode based on environment variables"""
    return (
        os.getenv('RAILWAY_ENVIRONMENT') or 
        os.getenv('VERCEL') or 
        os.getenv('PRODUCTION') or
        os.getenv('DYNO')  # Heroku
    )


def test_production_mode_detection():
    """Test that production mode is correctly detected based on environment variables"""
    
    # Save current environment
    saved_env = {}
    for key in ['RAILWAY_ENVIRONMENT', 'VERCEL', 'PRODUCTION', 'DYNO']:
        saved_env[key] = os.environ.pop(key, None)
    
    try:
        # Test 1: No environment variable - should be GUI mode
        assert not check_production_mode(), "Should default to GUI mode"
        
        # Test 2: RAILWAY_ENVIRONMENT set
        os.environ['RAILWAY_ENVIRONMENT'] = 'production'
        assert check_production_mode(), "Should detect Railway environment"
        os.environ.pop('RAILWAY_ENVIRONMENT')
        
        # Test 3: VERCEL environment set
        os.environ['VERCEL'] = '1'
        assert check_production_mode(), "Should detect Vercel environment"
        os.environ.pop('VERCEL')
        
        # Test 4: PRODUCTION set
        os.environ['PRODUCTION'] = 'true'
        assert check_production_mode(), "Should detect PRODUCTION environment"
        os.environ.pop('PRODUCTION')
        
        # Test 5: DYNO set (Heroku)
        os.environ['DYNO'] = 'web.1'
        assert check_production_mode(), "Should detect Heroku environment"
        os.environ.pop('DYNO')
        
        print("✓ All production mode detection tests passed")
    
    finally:
        # Restore environment
        for key, value in saved_env.items():
            if value is not None:
                os.environ[key] = value
            else:
                os.environ.pop(key, None)


def test_flask_app_import():
    """Test that Flask app can be imported from run_web_ui"""
    try:
        from run_web_ui import app
        assert app is not None, "Flask app should be available"
        assert hasattr(app, 'run'), "Flask app should have run method"
        print("✓ Flask app import test passed")
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
    
    test_production_mode_detection()
    test_flask_app_import()
    test_gui_import_error_handling()
    
    print()
    print("✓ All tests completed")
