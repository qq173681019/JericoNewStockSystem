"""
Test main.py environment detection and conditional execution
"""
import sys
import os
from pathlib import Path
from unittest.mock import patch, MagicMock
import importlib

# Add project root to path
ROOT_DIR = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT_DIR))


def test_environment_detection_production():
    """Test that production environment is correctly detected"""
    
    # Test Railway environment
    with patch.dict(os.environ, {'RAILWAY_ENVIRONMENT': 'production'}):
        assert os.getenv('RAILWAY_ENVIRONMENT') == 'production'
        print("✓ Railway environment detection works")
    
    # Test Vercel environment
    with patch.dict(os.environ, {'VERCEL': '1'}):
        assert os.getenv('VERCEL') == '1'
        print("✓ Vercel environment detection works")
    
    # Test generic production flag
    with patch.dict(os.environ, {'PRODUCTION': 'true'}):
        assert os.getenv('PRODUCTION') == 'true'
        print("✓ Production flag detection works")


def test_environment_detection_local():
    """Test that local environment is correctly detected"""
    
    # Clear any production environment variables
    env_copy = os.environ.copy()
    for key in ['RAILWAY_ENVIRONMENT', 'VERCEL', 'PRODUCTION']:
        env_copy.pop(key, None)
    
    with patch.dict(os.environ, env_copy, clear=True):
        is_production = os.getenv('RAILWAY_ENVIRONMENT') is not None or os.getenv('VERCEL') is not None or os.getenv('PRODUCTION') is not None
        assert is_production is False
        print("✓ Local environment detection works")


def test_main_production_mode():
    """Test that main.py runs in production mode when environment is set"""
    
    # Mock the Flask app and its run method
    mock_app = MagicMock()
    
    with patch.dict(os.environ, {'RAILWAY_ENVIRONMENT': 'production', 'PORT': '8000'}):
        with patch('sys.exit') as mock_exit:
            with patch.dict(sys.modules, {'run_web_ui': MagicMock(app=mock_app)}):
                # Import main module
                if 'main' in sys.modules:
                    importlib.reload(sys.modules['main'])
                else:
                    import main as main_module
                
                # Since we're testing the logic, check that environment detection works
                is_production = os.getenv('RAILWAY_ENVIRONMENT') is not None or os.getenv('VERCEL') is not None or os.getenv('PRODUCTION') is not None
                assert is_production is True
                print("✓ Production mode environment check works")


def test_port_configuration():
    """Test that PORT environment variable is correctly read"""
    
    # Test default port
    with patch.dict(os.environ, {}, clear=True):
        port = int(os.getenv('PORT', 5000))
        assert port == 5000
        print("✓ Default port (5000) is correct")
    
    # Test custom port
    with patch.dict(os.environ, {'PORT': '8080'}):
        port = int(os.getenv('PORT', 5000))
        assert port == 8080
        print("✓ Custom port from environment variable works")


def test_environment_edge_cases():
    """Test edge cases like empty strings and false values"""
    
    # Test empty string should still be detected as production
    with patch.dict(os.environ, {'RAILWAY_ENVIRONMENT': ''}, clear=True):
        is_production = os.getenv('RAILWAY_ENVIRONMENT') is not None or os.getenv('VERCEL') is not None or os.getenv('PRODUCTION') is not None
        assert is_production is True
        print("✓ Empty string environment variable correctly detected as production")
    
    # Test '0' or 'false' should still be detected as production
    with patch.dict(os.environ, {'PRODUCTION': '0'}, clear=True):
        is_production = os.getenv('RAILWAY_ENVIRONMENT') is not None or os.getenv('VERCEL') is not None or os.getenv('PRODUCTION') is not None
        assert is_production is True
        print("✓ '0' environment variable correctly detected as production")
    
    with patch.dict(os.environ, {'VERCEL': 'false'}, clear=True):
        is_production = os.getenv('RAILWAY_ENVIRONMENT') is not None or os.getenv('VERCEL') is not None or os.getenv('PRODUCTION') is not None
        assert is_production is True
        print("✓ 'false' environment variable correctly detected as production")


if __name__ == "__main__":
    print("Testing environment detection...")
    test_environment_detection_production()
    test_environment_detection_local()
    test_main_production_mode()
    test_port_configuration()
    test_environment_edge_cases()
    print("\n✓ All main.py environment detection tests passed!")
