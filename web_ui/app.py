"""
Web UI Server for SIAPS
Lightweight Flask server to serve the modern web interface
"""
from flask import Flask, render_template, jsonify, request
from flask_cors import CORS
import sys
import os
import secrets
from pathlib import Path

# Add project root to path
ROOT_DIR = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT_DIR))

from src.utils import setup_logger

logger = setup_logger(__name__)

# Initialize Flask app
app = Flask(__name__, 
            template_folder='templates',
            static_folder='static')
CORS(app)

# Configure Flask
# Use environment variable for secret key, or generate a random one for development
app.config['SECRET_KEY'] = os.environ.get('FLASK_SECRET_KEY') or secrets.token_hex(32)
app.config['JSON_AS_ASCII'] = False  # Support Chinese characters


@app.route('/')
def index():
    """Render the main page"""
    logger.info("Serving main page")
    return render_template('index.html')


@app.route('/api/predict', methods=['POST'])
def predict():
    """
    Stock prediction API endpoint
    Expected JSON: {"stock_code": "000001", "prediction_type": "short"}
    """
    try:
        data = request.get_json()
        stock_code = data.get('stock_code')
        prediction_type = data.get('prediction_type', 'short')
        
        if not stock_code:
            return jsonify({'error': '股票代码不能为空'}), 400
        
        logger.info(f"Prediction request for {stock_code}, type: {prediction_type}")
        
        # TODO: Integrate with actual prediction models
        # For now, return mock data
        import random
        from datetime import datetime
        
        current_price = 15.50 + random.random() * 5
        price_change = (random.random() - 0.5) * 2
        target_price = current_price + price_change
        
        result = {
            'success': True,
            'stock_code': stock_code,
            'prediction_type': prediction_type,
            'current_price': round(current_price, 2),
            'target_price': round(target_price, 2),
            'trend': '上涨' if price_change > 0 else '下跌',
            'trend_percent': round((price_change / current_price) * 100, 2),
            'confidence': round(85 + random.random() * 10, 1),
            'risk_level': '高' if abs(price_change) > 1 else '中' if abs(price_change) > 0.5 else '低',
            'position': '70%' if price_change > 0 else '30%',
            'advice': '建议买入' if price_change > 0 else '建议观望',
            'update_time': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'indicators': {
                'macd': round((random.random() - 0.5), 3),
                'rsi': round(30 + random.random() * 40, 1),
                'kdj': round(40 + random.random() * 30, 1),
                'volume': int(random.random() * 1000000)
            }
        }
        
        return jsonify(result)
        
    except Exception as e:
        logger.error(f"Prediction error: {str(e)}", exc_info=True)
        return jsonify({'error': '预测失败，请重试'}), 500


@app.route('/api/watchlist', methods=['GET'])
def get_watchlist():
    """Get user's watchlist"""
    try:
        # TODO: Implement actual watchlist retrieval from database
        watchlist = [
            {
                'stock_code': '000001',
                'stock_name': '平安银行',
                'current_price': 15.68,
                'change_percent': 2.3,
                'trend': 'up'
            },
            {
                'stock_code': '600000',
                'stock_name': '浦发银行',
                'current_price': 8.92,
                'change_percent': -1.1,
                'trend': 'down'
            }
        ]
        
        return jsonify({'success': True, 'watchlist': watchlist})
        
    except Exception as e:
        logger.error(f"Watchlist error: {str(e)}", exc_info=True)
        return jsonify({'error': '获取观测池失败'}), 500


@app.route('/api/watchlist', methods=['POST'])
def add_to_watchlist():
    """Add stock to watchlist"""
    try:
        data = request.get_json()
        stock_code = data.get('stock_code')
        
        if not stock_code:
            return jsonify({'error': '股票代码不能为空'}), 400
        
        logger.info(f"Adding {stock_code} to watchlist")
        
        # TODO: Implement actual database insertion
        
        return jsonify({
            'success': True,
            'message': f'股票 {stock_code} 已添加到观测池'
        })
        
    except Exception as e:
        logger.error(f"Add to watchlist error: {str(e)}", exc_info=True)
        return jsonify({'error': '添加失败'}), 500


@app.route('/api/history', methods=['GET'])
def get_history():
    """Get prediction history"""
    try:
        # TODO: Implement actual history retrieval from database
        history = [
            {
                'date': '2026-01-30',
                'stock_code': '000001',
                'prediction_type': '短期',
                'predicted_value': '+2.5%',
                'actual_value': '+2.3%',
                'accuracy': 92,
                'trend': 'up'
            },
            {
                'date': '2026-01-29',
                'stock_code': '600000',
                'prediction_type': '短期',
                'predicted_value': '-1.0%',
                'actual_value': '-1.1%',
                'accuracy': 95,
                'trend': 'down'
            }
        ]
        
        return jsonify({'success': True, 'history': history})
        
    except Exception as e:
        logger.error(f"History error: {str(e)}", exc_info=True)
        return jsonify({'error': '获取历史记录失败'}), 500


@app.route('/api/technical-analysis', methods=['POST'])
def technical_analysis():
    """Perform technical analysis on a stock"""
    try:
        data = request.get_json()
        stock_code = data.get('stock_code')
        
        if not stock_code:
            return jsonify({'error': '股票代码不能为空'}), 400
        
        logger.info(f"Technical analysis for {stock_code}")
        
        # TODO: Integrate with actual technical analysis modules
        import random
        
        result = {
            'success': True,
            'stock_code': stock_code,
            'indicators': {
                'macd': {
                    'value': round(random.random() - 0.5, 3),
                    'signal': '买入信号' if random.random() > 0.5 else '卖出信号'
                },
                'rsi': {
                    'value': round(30 + random.random() * 40, 1),
                    'signal': '超买' if random.random() > 0.7 else '中性' if random.random() > 0.3 else '超卖'
                },
                'bollinger': {
                    'position': '中轨',
                    'signal': '观望'
                },
                'kdj': {
                    'value': round(40 + random.random() * 30, 1),
                    'signal': '卖出信号' if random.random() > 0.5 else '买入信号'
                }
            }
        }
        
        return jsonify(result)
        
    except Exception as e:
        logger.error(f"Technical analysis error: {str(e)}", exc_info=True)
        return jsonify({'error': '技术分析失败'}), 500


@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'service': 'SIAPS Web UI',
        'version': '0.1.0'
    })


def run_server(host='127.0.0.1', port=5000, debug=True):
    """Run the Flask development server"""
    logger.info(f"Starting SIAPS Web UI Server on http://{host}:{port}")
    app.run(host=host, port=port, debug=debug)


if __name__ == '__main__':
    run_server()
