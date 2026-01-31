"""
SIAPS - Web Server
Flask web server for the beautiful UI interface
"""
from flask import Flask, render_template, jsonify, request
from pathlib import Path
import sys

# Add project root to Python path
ROOT_DIR = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT_DIR))

from src.utils import setup_logger, validate_stock_code
from config.settings import APP_NAME, APP_VERSION

app = Flask(__name__, 
            template_folder='templates',
            static_folder='static',
            static_url_path='/static')

logger = setup_logger(__name__)


@app.route('/')
def index():
    """Serve the main page"""
    return render_template('index.html')


@app.route('/api/info')
def get_info():
    """Get application information"""
    return jsonify({
        'name': APP_NAME,
        'version': APP_VERSION,
        'status': 'running'
    })


@app.route('/api/validate_stock', methods=['POST'])
def validate_stock():
    """Validate stock code"""
    data = request.get_json()
    stock_code = data.get('code', '')
    
    is_valid = validate_stock_code(stock_code)
    
    return jsonify({
        'valid': is_valid,
        'code': stock_code
    })


@app.route('/api/predict', methods=['POST'])
def predict():
    """
    Run stock prediction
    This is a placeholder API endpoint for future ML integration
    """
    data = request.get_json()
    stock_code = data.get('code', '')
    prediction_type = data.get('type', 'short')
    
    if not validate_stock_code(stock_code):
        return jsonify({
            'success': False,
            'error': 'Invalid stock code'
        }), 400
    
    # TODO: Integrate with actual prediction models
    # For now, return a placeholder response
    logger.info(f"Prediction requested for {stock_code}, type: {prediction_type}")
    
    return jsonify({
        'success': True,
        'message': 'Prediction endpoint ready. ML models will be integrated in future versions.',
        'stock_code': stock_code,
        'prediction_type': prediction_type
    })


@app.errorhandler(404)
def not_found(e):
    """Handle 404 errors"""
    return jsonify({'error': 'Not found'}), 404


@app.errorhandler(500)
def server_error(e):
    """Handle 500 errors"""
    logger.error(f"Server error: {str(e)}")
    return jsonify({'error': 'Internal server error'}), 500


def run_web_server(host='127.0.0.1', port=5000, debug=True):
    """Run the Flask web server"""
    logger.info(f"Starting SIAPS Web Server on http://{host}:{port}")
    app.run(host=host, port=port, debug=debug)


if __name__ == '__main__':
    run_web_server()
