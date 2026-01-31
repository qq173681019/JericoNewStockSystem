#!/usr/bin/env python3
"""
SIAPS Web UI - Minimal Flask Backend
A lightweight web interface for the Stock Intelligent Analysis & Prediction System
"""
import sys
from pathlib import Path
from flask import Flask, render_template, jsonify, request
from flask_cors import CORS
import webbrowser
import threading

# Add project root to Python path
ROOT_DIR = Path(__file__).parent
sys.path.insert(0, str(ROOT_DIR))

try:
    from src.utils import setup_logger
    logger = setup_logger(__name__)
except ImportError:
    import logging
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)

# Initialize Flask app
app = Flask(__name__, 
            template_folder='web_ui/templates',
            static_folder='web_ui/static')
CORS(app)  # Enable CORS for API calls

# Configuration
app.config['SECRET_KEY'] = 'siaps-secret-key-change-in-production'
app.config['JSON_AS_ASCII'] = False  # Support Chinese characters in JSON


@app.route('/')
def index():
    """Serve the main page"""
    return render_template('index.html')


@app.route('/api/predict/<stock_code>', methods=['GET'])
def predict_stock(stock_code):
    """
    API endpoint for stock prediction
    This is a minimal implementation that returns mock data.
    In production, this would call the actual prediction models.
    """
    try:
        # TODO: Integrate with actual prediction models
        # from src.prediction_models import PredictionEngine
        # engine = PredictionEngine()
        # result = engine.predict(stock_code)
        
        # For now, return mock data structure
        result = {
            'success': True,
            'stockCode': stock_code,
            'prediction': {
                'shortTerm': {
                    'direction': 'up',
                    'change': 2.5,
                    'confidence': 0.75
                },
                'mediumTerm': {
                    'targetPrice': 35.60,
                    'timeframe': '3个月',
                    'confidence': 0.68
                },
                'advice': '买入',
                'accuracy': 78.5
            },
            'technicalIndicators': {
                'RSI': 65.3,
                'MACD': 0.15,
                'KDJ': 72.8,
                'MA5': 33.45,
                'MA20': 32.10,
                'BOLL': '31.50-34.80'
            },
            'message': 'Prediction completed successfully'
        }
        
        logger.info(f"Prediction requested for stock: {stock_code}")
        return jsonify(result)
        
    except Exception as e:
        logger.error(f"Prediction error for {stock_code}: {str(e)}")
        return jsonify({
            'success': False,
            'error': str(e),
            'message': 'Prediction failed'
        }), 500


@app.route('/api/watchlist', methods=['GET', 'POST'])
def manage_watchlist():
    """
    API endpoint for watchlist management
    GET: Retrieve watchlist
    POST: Add stock to watchlist
    """
    try:
        if request.method == 'GET':
            # TODO: Retrieve watchlist from database
            # For now, return mock data
            watchlist = [
                {
                    'code': '000001',
                    'name': '平安银行',
                    'currentPrice': 12.45,
                    'change': 2.3,
                    'targetPrice': 13.50,
                    'alert': 'normal'
                },
                {
                    'code': '600036',
                    'name': '招商银行',
                    'currentPrice': 35.67,
                    'change': -1.2,
                    'targetPrice': 38.00,
                    'alert': 'watch'
                }
            ]
            return jsonify({'success': True, 'data': watchlist})
            
        elif request.method == 'POST':
            data = request.get_json()
            stock_code = data.get('stockCode')
            
            # TODO: Add to database
            logger.info(f"Added {stock_code} to watchlist")
            
            return jsonify({
                'success': True,
                'message': f'Stock {stock_code} added to watchlist'
            })
            
    except Exception as e:
        logger.error(f"Watchlist error: {str(e)}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/api/history', methods=['GET'])
def get_history():
    """
    API endpoint for prediction history
    """
    try:
        # TODO: Retrieve from database
        history = [
            {
                'timestamp': '2026-01-30 14:30:00',
                'stockCode': '000001',
                'predictionType': '短期',
                'predictedResult': '+2.5%',
                'actualResult': '+2.3%',
                'accuracy': 'accurate'
            },
            {
                'timestamp': '2026-01-29 10:15:00',
                'stockCode': '600036',
                'predictionType': '中期',
                'predictedResult': '¥38.50',
                'actualResult': 'pending',
                'accuracy': 'pending'
            }
        ]
        
        return jsonify({'success': True, 'data': history})
        
    except Exception as e:
        logger.error(f"History error: {str(e)}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'service': 'SIAPS Web UI',
        'version': '1.0.0'
    })


def open_browser(port=5000):
    """Open browser after a short delay"""
    import time
    time.sleep(1.5)
    webbrowser.open(f'http://127.0.0.1:{port}')


def main():
    """Main entry point"""
    port = 5000
    host = '127.0.0.1'
    
    print("=" * 70)
    print("  SIAPS - 股票智能分析预测系统 Web UI")
    print("  Stock Intelligent Analysis & Prediction System")
    print("=" * 70)
    print(f"\n🚀 Starting web server on http://{host}:{port}")
    print(f"📊 Open your browser and navigate to: http://{host}:{port}")
    print("\n💡 Features:")
    print("   - 股票预测 (Stock Prediction)")
    print("   - 观测池管理 (Watchlist Management)")
    print("   - 历史记录查询 (History)")
    print("   - 数据分析 (Analytics)")
    print("   - 深色/浅色主题 (Dark/Light Theme)")
    print("\n⚠️  Press Ctrl+C to stop the server")
    print("=" * 70 + "\n")
    
    # Open browser in a separate thread
    threading.Thread(target=open_browser, args=(port,), daemon=True).start()
    
    # Start Flask server
    try:
        app.run(host=host, port=port, debug=False)
    except KeyboardInterrupt:
        print("\n\n👋 Server stopped. Goodbye!")
    except Exception as e:
        logger.error(f"Server error: {str(e)}")
        print(f"\n❌ Error starting server: {str(e)}")
        sys.exit(1)


if __name__ == '__main__':
    main()
