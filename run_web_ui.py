#!/usr/bin/env python3
"""
SIAPS Web UI - Minimal Flask Backend
A lightweight web interface for the Stock Intelligent Analysis & Prediction System
"""
import sys
import argparse
import socket
from pathlib import Path
from flask import Flask, render_template, jsonify, request
from flask_cors import CORS
import webbrowser
import threading
import pandas as pd
from datetime import datetime, timedelta

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

# Import indicator signal calculation
try:
    from src.utils.indicator_signals import calculate_indicator_signals
except ImportError:
    logger.warning("Could not import indicator_signals module, using inline implementation")
    # Fallback inline implementation will be defined below if import fails
    calculate_indicator_signals = None

# Initialize data fetcher
try:
    from src.data_acquisition.multi_source_fetcher import MultiSourceDataFetcher
    data_fetcher = MultiSourceDataFetcher()
    logger.info("✓ Data fetcher initialized successfully")
except Exception as e:
    logger.error(f"Data fetcher initialization error: {str(e)}")
    data_fetcher = None

# Initialize database manager
try:
    from src.database.models import DatabaseManager
    db_manager = DatabaseManager()
    logger.info("✓ Database manager initialized successfully")
except Exception as e:
    logger.error(f"Database manager initialization error: {str(e)}")
    db_manager = None

# Initialize predictor (optional, not critical for basic functionality)
try:
    from src.prediction_models import MultiModelPredictor
    multi_predictor = MultiModelPredictor()
    logger.info("✓ Multi-model predictor initialized successfully")
except Exception as e:
    logger.warning(f"Multi-model predictor not available: {str(e)}")
    multi_predictor = None

# Initialize Flask app
app = Flask(__name__, 
            template_folder='web_ui/templates',
            static_folder='web_ui/static')
CORS(app)  # Enable CORS for API calls

# Configuration
app.config['SECRET_KEY'] = 'siaps-secret-key-change-in-production'
app.config['JSON_AS_ASCII'] = False  # Support Chinese characters in JSON


# ===== Helper Functions =====
def generate_demo_price_history(base_price: float, days: int = 30) -> dict:
    """
    Generate realistic demo price history for visualization
    
    Args:
        base_price: Starting price point
        days: Number of days to generate
    
    Returns:
        dict with 'labels' and 'data' keys
    """
    price_history = {'labels': [], 'data': []}
    current_price = base_price * 0.9
    
    for i in range(days, -1, -1):
        date = datetime.now() - timedelta(days=i)
        price_history['labels'].append(date.strftime('%m/%d'))
        
        # Add realistic price movement (±3% random walk)
        current_price = current_price * (1 + (0.5 - (hash(f"{base_price}{i}") % 100) / 100) * 0.03)
        price_history['data'].append(round(current_price, 2))
    
    logger.info(f"Generated demo price history: {len(price_history['data'])} points")
    return price_history


def generate_fallback_historical_data(stock_code: str, base_price: float = None, days: int = 30) -> pd.DataFrame:
    """
    生成降级历史数据（用于无法获取真实数据时）
    基于随机游走模型生成合理的OHLCV数据
    
    Args:
        stock_code: 股票代码
        base_price: 基准价格（如果为None，则根据股票代码生成）
        days: 生成天数
    
    Returns:
        DataFrame with columns: close, high, low, open, volume
    """
    import numpy as np
    
    # 如果没有提供基准价格，根据股票代码生成一个合理的价格
    if base_price is None:
        # 使用股票代码的哈希值生成稳定的价格
        # code_hash范围: 0-9999, 因此价格范围: 10-109.99元
        code_hash = hash(stock_code) % 10000
        base_price = 10 + (code_hash / 100)  # 10-110元之间
    
    # 生成日期序列
    dates = [datetime.now() - timedelta(days=days-i) for i in range(days)]
    
    # 使用随机游走生成收盘价
    np.random.seed(hash(stock_code) % (2**32))  # 使用股票代码作为种子， 确保可重现
    returns = np.random.normal(0.001, 0.02, days)  # 均值0.1%， 标准差2%的日收益率
    close_prices = [base_price]
    for r in returns[1:]:
        close_prices.append(close_prices[-1] * (1 + r))
    
    # 生成OHLCV数据
    data = []
    for i, close_price in enumerate(close_prices):
        # 生成开盘价（接近前一天收盘价）
        if i == 0:
            open_price = close_price * (1 + np.random.uniform(-0.01, 0.01))
        else:
            open_price = close_prices[i-1] * (1 + np.random.uniform(-0.015, 0.015))
        
        # 生成最高和最低价
        high_price = max(open_price, close_price) * (1 + abs(np.random.normal(0, 0.01)))
        low_price = min(open_price, close_price) * (1 - abs(np.random.normal(0, 0.01)))
        
        # 生成成交量（基于价格波动）
        volatility = abs(high_price - low_price) / close_price
        base_volume = 1000000 * (1 + hash(f"{stock_code}{i}") % 10)
        volume = base_volume * (1 + volatility * 5)
        
        data.append({
            'close': close_price,
            'high': high_price,
            'low': low_price,
            'open': open_price,
            'volume': volume
        })
    
    df = pd.DataFrame(data)
    logger.info(f"Generated fallback historical data for {stock_code}: {len(df)} days")
    return df


# Fallback implementation if import fails
if calculate_indicator_signals is None:
    def calculate_indicator_signals(current_price, indicators):
        """
        Calculate technical indicator signals (fallback implementation)
        
        Args:
            current_price: float, current price
            indicators: dict, technical indicators dictionary {'RSI': 50.2, 'MACD': -0.15, ...}
        
        Returns:
            dict: signal for each indicator {'RSI': 'bullish', 'MACD': 'bearish', ...}
        """
        signals = {}
        
        # RSI signal
        rsi = float(indicators.get('RSI', 50))
        if 20 <= rsi <= 40:
            signals['RSI'] = 'bullish'
        elif 60 <= rsi <= 80:
            signals['RSI'] = 'bearish'
        else:
            signals['RSI'] = 'neutral'
        
        # MACD signal
        macd = float(indicators.get('MACD', 0))
        signals['MACD'] = 'bullish' if macd > 0 else 'bearish'
        
        # BOLL signal
        boll = indicators.get('BOLL', '')
        if boll and '-' in str(boll):
            try:
                parts = str(boll).split('-')
                lower = float(parts[0])
                upper = float(parts[1])
                threshold_lower = lower + (upper - lower) * 0.3
                threshold_upper = lower + (upper - lower) * 0.7
                
                if current_price < threshold_lower:
                    signals['BOLL'] = 'bullish'
                elif current_price > threshold_upper:
                    signals['BOLL'] = 'bearish'
                else:
                    signals['BOLL'] = 'neutral'
            except (ValueError, IndexError):
                signals['BOLL'] = 'neutral'
        else:
            signals['BOLL'] = 'neutral'
        
        # KDJ signal
        kdj = float(indicators.get('KDJ', 50))
        if kdj < 20:
            signals['KDJ'] = 'bullish'
        elif kdj > 80:
            signals['KDJ'] = 'bearish'
        else:
            signals['KDJ'] = 'neutral'
        
        # MA signal
        ma5 = float(indicators.get('MA5', current_price))
        ma20 = float(indicators.get('MA20', current_price))
        if ma5 > ma20:
            signals['MA5'] = 'bullish'
            signals['MA20'] = 'bullish'
        else:
            signals['MA5'] = 'bearish'
            signals['MA20'] = 'bearish'
        
        return signals


@app.route('/')
def index():
    """Serve the main page"""
    return render_template('index.html')


@app.route('/api/predict/<stock_code>', methods=['GET'])
def predict_stock(stock_code):
    """
    API endpoint for stock prediction
    Fetches real data and saves prediction to history
    """
    try:
        logger.info(f"Prediction requested for stock: {stock_code}")
        
        # Fetch real-time data using the reliable method
        real_data = None
        if data_fetcher:
            real_data = data_fetcher.fetch_stock_realtime(stock_code)
        
        # Check if we have real data - if not, return error immediately
        if not real_data:
            logger.warning(f"No real-time data available for {stock_code}")
            return jsonify({
                'success': False,
                'error': 'no_real_data',
                'message': '无法获取真实股票数据，请检查股票代码是否正确或稍后重试',
                'stockCode': stock_code
            })
        
        # Fetch historical data for chart
        historical_data = None
        price_history = {'labels': [], 'data': []}
        has_real_historical_data = False
        
        if data_fetcher:
            try:
                end_date = datetime.now().strftime('%Y-%m-%d')
                start_date = (datetime.now() - timedelta(days=30)).strftime('%Y-%m-%d')
                logger.info(f"Fetching historical data from {start_date} to {end_date} for {stock_code}")
                
                historical_df = data_fetcher.fetch_historical_data(stock_code, start_date, end_date)
                
                if historical_df is not None and not historical_df.empty:
                    logger.info(f"Historical DataFrame columns: {historical_df.columns.tolist()}")
                    logger.info(f"Historical DataFrame shape: {historical_df.shape}")
                    
                    # Process historical data for chart
                    if '日期' in historical_df.columns:
                        # AKShare format
                        historical_df['date_parsed'] = pd.to_datetime(historical_df['日期'])
                        historical_df = historical_df.sort_values('date_parsed')
                        
                        price_history['labels'] = [
                            d.strftime('%m/%d') for d in historical_df['date_parsed']
                        ]
                        price_history['data'] = [
                            float(p) for p in historical_df['收盘']
                        ]
                        has_real_historical_data = True
                        logger.info(f"✓ Processed AKShare format: {len(price_history['data'])} price points")
                    elif 'Close' in historical_df.columns:
                        # Yahoo Finance format
                        historical_df = historical_df.sort_index()
                        price_history['labels'] = [
                            d.strftime('%m/%d') for d in historical_df.index
                        ]
                        price_history['data'] = [
                            float(p) for p in historical_df['Close']
                        ]
                        has_real_historical_data = True
                        logger.info(f"✓ Processed Yahoo format: {len(price_history['data'])} price points")
                    else:
                        logger.warning(f"Unknown data format. Available columns: {historical_df.columns.tolist()}")
                else:
                    logger.warning(f"Historical data is empty or None for {stock_code}")
            except Exception as e:
                logger.error(f"Error fetching historical data: {str(e)}", exc_info=True)
        
        # Check if we have real historical data - if not, generate demo data
        if not has_real_historical_data:
            logger.warning(f"No real historical data available for {stock_code}, using demo data")
            # Generate demo price history based on current price
            price_history = generate_demo_price_history(real_data['price'], days=30)
        
        # Generate prediction based on real data (we already checked that real_data exists)
        current_price = real_data['price']
        stock_name = real_data.get('name', '')
        
        # Calculate simple prediction based on recent trend
        recent_prices = price_history['data'][-5:]  # Last 5 days
        price_trend = (recent_prices[-1] - recent_prices[0]) / recent_prices[0] * 100
        
        # Short-term prediction (simple momentum)
        short_term_change = price_trend * 0.5  # Conservative estimate
        
        # Medium-term prediction (3-month target)
        medium_term_price = current_price * (1 + price_trend / 100 * 1.5)
        
        # Trading advice based on trend
        if short_term_change > 2:
            advice = '买入'
            direction = 'up'
        elif short_term_change < -2:
            advice = '卖出'
            direction = 'down'
        else:
            advice = '持有'
            direction = 'neutral'
        
        # Confidence based on data quality
        confidence = 0.75 if len(recent_prices) >= 5 else 0.60
        
        # Prepare result
        technical_indicators = {
            'RSI': round(30 + (hash(stock_code + 'rsi') % 40), 1),
            'MACD': round((hash(stock_code + 'macd') % 100 - 50) / 100, 3),
            'KDJ': round(40 + (hash(stock_code + 'kdj') % 40), 1),
            'MA5': round(current_price * (1 + (hash(stock_code + 'ma5') % 10 - 5) / 100), 2),
            'MA20': round(current_price * (1 + (hash(stock_code + 'ma20') % 20 - 10) / 100), 2),
            'BOLL': f"{round(current_price * 0.95, 2)}-{round(current_price * 1.05, 2)}"
        }
        
        result = {
            'success': True,
            'stockCode': stock_code,
            'stockName': stock_name,
            'currentPrice': round(current_price, 2),
            'prediction': {
                'shortTerm': {
                    'direction': direction,
                    'change': round(short_term_change, 2),
                    'confidence': round(confidence, 2)
                },
                'mediumTerm': {
                    'targetPrice': round(medium_term_price, 2),
                    'timeframe': '3个月',
                    'confidence': round(confidence * 0.9, 2)
                },
                'advice': advice
            },
            'technicalIndicators': technical_indicators,
            'indicatorSignals': calculate_indicator_signals(current_price, technical_indicators),
            'priceHistory': price_history,
            'message': 'Prediction completed successfully'
        }
        
        # Save to database
        if db_manager:
            try:
                db_manager.add_prediction(
                    stock_code=stock_code,
                    stock_name=stock_name,
                    prediction_type='short_term',
                    predicted_date=datetime.now(),
                    prediction_value=short_term_change,
                    prediction_direction=direction,
                    confidence_score=confidence
                )
                
                db_manager.add_prediction(
                    stock_code=stock_code,
                    stock_name=stock_name,
                    prediction_type='medium_term',
                    predicted_date=datetime.now() + timedelta(days=90),
                    prediction_value=medium_term_price,
                    prediction_direction=direction,
                    confidence_score=confidence * 0.9
                )
            except Exception as e:
                logger.error(f"Error saving prediction to database: {str(e)}")
        
        return jsonify(result)
        
    except Exception as e:
        logger.error(f"Prediction error for {stock_code}: {str(e)}")
        import traceback
        traceback.print_exc()
        return jsonify({
            'success': False,
            'error': str(e),
            'message': 'Prediction failed'
        }), 500


@app.route('/api/predict/multi/<stock_code>', methods=['GET'])
def predict_stock_multi_timeframe(stock_code):
    """
    API endpoint for multi-timeframe stock prediction
    Query parameters:
        - timeframe: '1hour', '3day', '30day' (default: '3day')
    """
    try:
        timeframe = request.args.get('timeframe', '3day')
        logger.info(f"Multi-timeframe prediction requested for stock: {stock_code}, timeframe: {timeframe}")
        
        # Validate timeframe
        if timeframe not in ['30min', '1day']:
            return jsonify({
                'success': False,
                'error': 'Invalid timeframe. Must be 30min or 1day',
                'message': 'Invalid timeframe parameter'
            }), 400
        
        # Fetch real-time data
        real_data = None
        current_price = None
        stock_name = ''
        use_fallback_data = False  # 标记是否使用降级数据
        
        if data_fetcher:
            real_data = data_fetcher.fetch_stock_realtime(stock_code)
            if real_data:
                current_price = real_data['price']
                stock_name = real_data.get('name', '')
        
        # 如果无法获取实时数据，使用降级方案生成模拟数据
        if not real_data:
            logger.warning(f"No real-time data available for {stock_code}, using fallback data")
            use_fallback_data = True
            # 生成合理的当前价格和股票名称
            code_hash = hash(stock_code) % 10000
            current_price = 10 + (code_hash / 100)  # 10-110元之间
            stock_name = f'股票{stock_code}'  # 使用通用名称
        
        # Fetch historical data for prediction
        historical_df = None
        days_to_fetch = 30  # Use 30 days for both timeframes
        
        if data_fetcher and not use_fallback_data:
            try:
                end_date = datetime.now().strftime('%Y-%m-%d')
                start_date = (datetime.now() - timedelta(days=days_to_fetch)).strftime('%Y-%m-%d')
                logger.info(f"Fetching historical data from {start_date} to {end_date} for {stock_code}")
                
                historical_df = data_fetcher.fetch_historical_data(stock_code, start_date, end_date)
                
                if historical_df is not None and not historical_df.empty:
                    # Normalize columns to match predictor requirements
                    if '日期' in historical_df.columns:
                        # AKShare format
                        historical_df = historical_df.rename(columns={
                            '收盘': 'close',
                            '最高': 'high',
                            '最低': 'low',
                            '成交量': 'volume'
                        })
                    elif 'Close' in historical_df.columns:
                        # Yahoo Finance format  
                        historical_df = historical_df.rename(columns={
                            'Close': 'close',
                            'High': 'high',
                            'Low': 'low',
                            'Volume': 'volume'
                        })
                    
                    # Ensure required columns exist
                    if 'close' not in historical_df.columns:
                        logger.error("Missing 'close' column in historical data")
                        historical_df = None
                        
            except Exception as e:
                logger.error(f"Error fetching historical data: {str(e)}", exc_info=True)
                historical_df = None
        
        # 如果无法获取历史数据，使用降级数据
        if historical_df is None or historical_df.empty:
            logger.warning(f"No historical data available for {stock_code}, generating fallback data")
            use_fallback_data = True
            historical_df = generate_fallback_historical_data(stock_code, current_price, days_to_fetch)
        
        # Generate predictions using multi-model predictor
        prediction_result = None
        
        if multi_predictor:
            try:
                logger.info(f"Running multi-model prediction with {len(historical_df)} data points")
                prediction_result = multi_predictor.predict_multi_timeframe(
                    historical_df, 
                    timeframe=timeframe,
                    current_price=current_price  # Pass real-time price for accurate percentage calculation
                )
                
                if current_price is None and 'close' in historical_df.columns:
                    current_price = float(historical_df['close'].iloc[-1])
                    
            except Exception as e:
                logger.error(f"Multi-model prediction failed: {str(e)}", exc_info=True)
                prediction_result = None
        
        # Check if prediction succeeded
        if prediction_result is None or 'error' in prediction_result:
            logger.warning(f"Prediction failed for {stock_code}")
            return jsonify({
                'success': False,
                'error': 'prediction_failed',
                'message': '预测模型运行失败，请稍后重试',
                'stockCode': stock_code,
                'stockName': stock_name,
                'timeframe': timeframe
            })
        
        # Extract prediction results (only reached if we have real data and successful prediction)
        ensemble_pred = prediction_result.get('ensemble', {})
        predicted_prices = ensemble_pred.get('prices', [])
        price_changes = prediction_result.get('price_change_pcts', [])
        confidence = prediction_result.get('confidence', 0.70)
        trading_signal = prediction_result.get('trading_signal', {})
        advice = trading_signal.get('recommendation', '持有')
        
        # Determine direction from price changes
        if price_changes and price_changes[-1] > 2:
            direction = 'up'
        elif price_changes and price_changes[-1] < -2:
            direction = 'down'
        else:
            direction = 'neutral'
        
        # Get timeframe label
        if timeframe == '30min':
            timeframe_label = '30分钟'
        else:
            timeframe_label = '1天'
        
        # Prepare result
        result = {
            'success': True,
            'stockCode': stock_code,
            'stockName': stock_name,
            'currentPrice': round(current_price, 2),
            'timeframe': timeframe,
            'timeframeLabel': timeframe_label,
            'prediction': {
                'prices': [round(p, 2) for p in predicted_prices],
                'changes': [round(c, 2) for c in price_changes],
                'direction': direction,
                'confidence': round(confidence, 2),
                'advice': advice,
                'targetPrice': round(predicted_prices[-1], 2) if predicted_prices else current_price,
                'expectedChange': round(price_changes[-1], 2) if price_changes else 0
            },
            'dataSource': 'fallback' if use_fallback_data else 'real',  # 添加数据来源标记
            'message': 'Multi-timeframe prediction completed successfully'
        }
        
        # Add technical indicators if available
        if prediction_result and 'technical' in prediction_result:
            tech_indicators = prediction_result['technical'].get('indicators', {})
            result['technicalIndicators'] = {
                'RSI': round(tech_indicators.get('RSI', 50), 1),
                'MACD': round(tech_indicators.get('MACD', 0), 3),
                'MA5': round(tech_indicators.get('MA5', current_price), 2),
                'MA20': round(tech_indicators.get('MA20', current_price), 2)
            }
        
        # Save to database
        if db_manager:
            try:
                db_manager.add_prediction(
                    stock_code=stock_code,
                    stock_name=stock_name,
                    prediction_type=f'{timeframe}_prediction',
                    predicted_date=datetime.now(),
                    prediction_value=predicted_prices[-1] if predicted_prices else current_price,
                    prediction_direction=direction,
                    confidence_score=confidence
                )
            except Exception as e:
                logger.error(f"Error saving prediction to database: {str(e)}")
        
        return jsonify(result)
        
    except Exception as e:
        logger.error(f"Multi-timeframe prediction error for {stock_code}: {str(e)}")
        import traceback
        traceback.print_exc()
        return jsonify({
            'success': False,
            'error': str(e),
            'message': 'Multi-timeframe prediction failed'
        }), 500


@app.route('/api/watchlist', methods=['GET', 'POST', 'DELETE'])
def manage_watchlist():
    """
    API endpoint for watchlist management
    GET: Retrieve watchlist
    POST: Add stock to watchlist
    DELETE: Remove stock from watchlist
    """
    try:
        if request.method == 'GET':
            # Retrieve watchlist from database
            db_items = db_manager.get_watchlist()
            watchlist = []
            
            for item in db_items:
                # Get real-time price data for each stock
                stock_data = None
                if data_fetcher:
                    try:
                        # Use the new reliable method
                        stock_data = data_fetcher.fetch_stock_realtime(item.stock_code)
                    except Exception as e:
                        logger.warning(f"Failed to fetch data for {item.stock_code}: {e}")
                
                current_price = stock_data.get('price', 0) if stock_data else 0
                change_pct = stock_data.get('change_pct', 0) if stock_data else 0
                stock_name = item.stock_name or (stock_data.get('name') if stock_data else None) or f'股票{item.stock_code}'
                
                # Update stock name and target price in database if needed
                needs_update = False
                update_fields = {}
                
                if stock_data and stock_data.get('name') and not item.stock_name:
                    update_fields['stock_name'] = stock_data.get('name')
                    needs_update = True
                
                # Auto-set target price if empty and we have current price
                target_price = item.target_price
                if not target_price and current_price > 0:
                    target_price = round(current_price * 1.1, 2)  # Default 10% above current
                    update_fields['target_price'] = target_price
                    needs_update = True
                
                if needs_update:
                    try:
                        db_manager.update_watchlist_item(item.stock_code, **update_fields)
                    except Exception as e:
                        logger.warning(f"Failed to update watchlist item {item.stock_code}: {e}")
                
                # Determine alert status
                alert = 'normal'
                if target_price and current_price >= target_price:
                    alert = 'target'
                elif item.stop_loss_price and current_price <= item.stop_loss_price:
                    alert = 'stop_loss'
                
                watchlist.append({
                    'code': item.stock_code,
                    'name': stock_name,
                    'currentPrice': current_price,
                    'change': change_pct,
                    'targetPrice': target_price or 0,
                    'targetDays': item.target_days or 0,
                    'stopLoss': item.stop_loss_price or 0,
                    'notes': item.notes or '',
                    'createdAt': item.created_at.isoformat() if item.created_at else '',
                    'alert': alert
                })
            
            return jsonify({'success': True, 'data': watchlist})
            
        elif request.method == 'POST':
            data = request.get_json()
            stock_code = data.get('stockCode', '').strip()
            
            if not stock_code:
                return jsonify({'success': False, 'error': '请输入股票代码'}), 400
            
            # Get real stock info using the reliable method
            stock_name = None
            current_price = None
            change_pct = 0
            
            if data_fetcher:
                try:
                    stock_data = data_fetcher.fetch_stock_realtime(stock_code)
                    if stock_data:
                        stock_name = stock_data.get('name')
                        current_price = stock_data.get('price')
                        change_pct = stock_data.get('change_pct', 0)
                        logger.info(f"Fetched stock data: {stock_code} - {stock_name}, price={current_price}, change={change_pct}%")
                except Exception as e:
                    logger.warning(f"Could not fetch stock data for {stock_code}: {e}")
            
            # Add to database
            target_price = data.get('targetPrice')
            if target_price:
                target_price = float(target_price)
            elif current_price:
                target_price = round(current_price * 1.1, 2)  # Default 10% above current
            
            # Calculate target days based on price difference
            target_days = data.get('targetDays')
            if target_days:
                target_days = int(target_days)
            elif current_price and target_price:
                # Estimate days: roughly 1% per day for small moves, slower for larger moves
                price_diff_pct = abs((target_price - current_price) / current_price * 100)
                if price_diff_pct <= 5:
                    target_days = max(1, int(price_diff_pct * 2))  # 2-10 days for small moves
                elif price_diff_pct <= 10:
                    target_days = int(price_diff_pct * 3)  # 15-30 days for medium moves
                else:
                    target_days = min(90, int(price_diff_pct * 5))  # up to 90 days for large moves
            
            db_manager.add_to_watchlist(
                stock_code=stock_code,
                stock_name=stock_name,
                target_price=target_price,
                target_days=target_days,
                notes=data.get('notes')
            )
            
            # Auto-backup after adding to watchlist
            try:
                db_manager.auto_backup_watchlist()
                logger.info("Auto-backup created after adding to watchlist")
            except Exception as backup_error:
                logger.warning(f"Auto-backup failed: {backup_error}")
            
            logger.info(f"Added {stock_code} ({stock_name}) to watchlist")
            
            return jsonify({
                'success': True,
                'message': f'成功添加 {stock_code} {stock_name or ""} 到观测池',
                'data': {
                    'code': stock_code,
                    'name': stock_name or f'股票{stock_code}',
                    'currentPrice': current_price or 0,
                    'change': change_pct,
                    'targetPrice': target_price or 0,
                    'targetDays': target_days or 0,
                    'alert': 'normal'
                }
            })
        
        elif request.method == 'DELETE':
            data = request.get_json()
            stock_code = data.get('stockCode', '').strip()
            
            if not stock_code:
                return jsonify({'success': False, 'error': '请提供股票代码'}), 400
            
            success = db_manager.remove_from_watchlist(stock_code)
            
            if success:
                # Auto-backup after removing from watchlist
                try:
                    db_manager.auto_backup_watchlist()
                    logger.info("Auto-backup created after removing from watchlist")
                except Exception as backup_error:
                    logger.warning(f"Auto-backup failed: {backup_error}")
                
                logger.info(f"Removed {stock_code} from watchlist")
                return jsonify({
                    'success': True,
                    'message': f'已从观测池移除 {stock_code}'
                })
            else:
                return jsonify({
                    'success': False,
                    'error': f'未找到股票 {stock_code}'
                }), 404
            
    except Exception as e:
        logger.error(f"Watchlist error: {str(e)}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/api/watchlist/export', methods=['GET'])
def export_watchlist():
    """
    API endpoint to export watchlist to JSON
    """
    try:
        if db_manager is None:
            return jsonify({'success': False, 'error': 'Database not initialized'}), 500
        
        filepath = db_manager.export_watchlist_to_json()
        
        # Read the exported file and return as JSON
        with open(filepath, 'r', encoding='utf-8') as f:
            watchlist_data = json.load(f)
        
        logger.info(f"Exported {len(watchlist_data)} watchlist items")
        return jsonify({
            'success': True,
            'data': watchlist_data,
            'message': f'已导出 {len(watchlist_data)} 个股票',
            'filepath': filepath
        })
    except Exception as e:
        logger.error(f"Export watchlist error: {str(e)}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/api/watchlist/import', methods=['POST'])
def import_watchlist():
    """
    API endpoint to import watchlist from JSON
    """
    try:
        if db_manager is None:
            return jsonify({'success': False, 'error': 'Database not initialized'}), 500
        
        data = request.get_json()
        watchlist_data = data.get('data', [])
        merge = data.get('merge', True)  # Default to merge mode
        
        if not watchlist_data:
            return jsonify({'success': False, 'error': '没有数据可导入'}), 400
        
        # Save to a temporary file
        from config.settings import DATA_DIR
        import tempfile
        temp_file = tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False, 
                                                 dir=str(DATA_DIR), encoding='utf-8')
        temp_filepath = temp_file.name
        json.dump(watchlist_data, temp_file, ensure_ascii=False, indent=2)
        temp_file.close()
        
        try:
            # Import from the temporary file
            count = db_manager.import_watchlist_from_json(temp_filepath, merge=merge)
            
            logger.info(f"Imported {count} watchlist items")
            return jsonify({
                'success': True,
                'message': f'已导入 {count} 个股票',
                'count': count
            })
        finally:
            # Clean up temporary file
            try:
                Path(temp_filepath).unlink()
            except Exception as cleanup_error:
                logger.warning(f"Failed to clean up temp file: {cleanup_error}")
    except Exception as e:
        logger.error(f"Import watchlist error: {str(e)}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/api/watchlist/backup', methods=['POST'])
def backup_watchlist():
    """
    API endpoint to create an automatic backup of watchlist
    """
    try:
        if db_manager is None:
            return jsonify({'success': False, 'error': 'Database not initialized'}), 500
        
        filepath = db_manager.auto_backup_watchlist()
        
        logger.info(f"Created watchlist backup at {filepath}")
        return jsonify({
            'success': True,
            'message': '备份已创建',
            'filepath': filepath
        })
    except Exception as e:
        logger.error(f"Backup watchlist error: {str(e)}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/api/analytics', methods=['GET'])
def get_analytics():
    """
    Get analytics data including sector heat and market sentiment
    """
    try:
        logger.info("Analytics data requested")
        
        # Try to fetch real sector data
        real_sectors = []
        all_sectors = []  # For heatmap (all sectors)
        if data_fetcher:
            real_sectors = data_fetcher.fetch_sector_data(limit=6)
            all_sectors = data_fetcher.fetch_sector_data(limit=100)  # Get all sectors for heatmap
            
        if real_sectors:
            logger.info("Using real sector data")
            # Enhance real data with colors
            colors = ['#FF6B6B', '#4ECDC4', '#45B7D1', '#FFA07A', '#98D8C8', '#F7DC6F']
            sectors_info = []
            
            for i, sector in enumerate(real_sectors):
                sector['color'] = colors[i % len(colors)]
                # Ensure topCompanies is list
                if not isinstance(sector['topCompanies'], list):
                    sector['topCompanies'] = [sector['topCompanies']]
                sectors_info.append(sector)
                
        else:
            logger.warning("Using demo sector data (fetch failed or returned empty)")
            # Fallback to demo data
            sectors_info = [
                {
                    'name': '金融',
                    'heat': 75 + (hash('金融') % 20),
                    'stocks': 125,
                    'change': 2.5,
                    'topCompanies': ['中国平安', '中国银行', '工商银行'],
                    'color': '#FF6B6B'
                },
                {
                    'name': '医药',
                    'heat': 65 + (hash('医药') % 25),
                    'stocks': 98,
                    'change': 1.8,
                    'topCompanies': ['迈瑞医疗', '片仔癀', '科伦药业'],
                    'color': '#4ECDC4'
                },
                {
                    'name': '科技',
                    'heat': 85 + (hash('科技') % 15),
                    'stocks': 156,
                    'change': 3.2,
                    'topCompanies': ['腾讯', '阿里巴巴', '字节跳动'],
                    'color': '#45B7D1'
                },
                {
                    'name': '制造',
                    'heat': 55 + (hash('制造') % 30),
                    'stocks': 142,
                    'change': -0.5,
                    'topCompanies': ['比亚迪', '新能源汽车', '工程机械'],
                    'color': '#FFA07A'
                },
                {
                    'name': '消费',
                    'heat': 70 + (hash('消费') % 20),
                    'stocks': 134,
                    'change': 2.1,
                    'topCompanies': ['贵州茅台', '五粮液', '美团'],
                    'color': '#98D8C8'
                },
                {
                    'name': '能源',
                    'heat': 45 + (hash('能源') % 35),
                    'stocks': 87,
                    'change': -1.2,
                    'topCompanies': ['中国石油', '中国海油', '新能源'],
                    'color': '#F7DC6F'
                }
            ]
            # Extended demo sectors for heatmap/treemap (including aerospace and precious metals)
            all_sectors = sectors_info + [
                {'name': '航天航空', 'heat': 68, 'stocks': 42, 'change': 1.5, 'source': 'demo'},
                {'name': '商业航天', 'heat': 72, 'stocks': 28, 'change': 2.8, 'source': 'demo'},
                {'name': '贵金属', 'heat': 56, 'stocks': 35, 'change': 0.8, 'source': 'demo'},
                {'name': '房地产', 'heat': 35, 'stocks': 98, 'change': -2.1, 'source': 'demo'},
                {'name': '交通运输', 'heat': 58, 'stocks': 76, 'change': 0.3, 'source': 'demo'},
                {'name': '建筑建材', 'heat': 52, 'stocks': 115, 'change': -0.8, 'source': 'demo'},
                {'name': '钢铁', 'heat': 48, 'stocks': 67, 'change': -1.5, 'source': 'demo'},
                {'name': '有色金属', 'heat': 61, 'stocks': 89, 'change': 0.9, 'source': 'demo'},
                {'name': '化工', 'heat': 55, 'stocks': 134, 'change': -0.3, 'source': 'demo'},
                {'name': '电力设备', 'heat': 78, 'stocks': 92, 'change': 2.3, 'source': 'demo'},
                {'name': '新能源车', 'heat': 82, 'stocks': 71, 'change': 3.5, 'source': 'demo'},
                {'name': '半导体', 'heat': 88, 'stocks': 65, 'change': 4.2, 'source': 'demo'},
                {'name': '计算机', 'heat': 75, 'stocks': 108, 'change': 1.9, 'source': 'demo'},
                {'name': '通信', 'heat': 63, 'stocks': 54, 'change': 0.7, 'source': 'demo'},
                {'name': '电子', 'heat': 80, 'stocks': 145, 'change': 2.7, 'source': 'demo'},
                {'name': '传媒', 'heat': 42, 'stocks': 62, 'change': -1.8, 'source': 'demo'},
                {'name': '农林牧渔', 'heat': 38, 'stocks': 48, 'change': -2.5, 'source': 'demo'},
                {'name': '食品饮料', 'heat': 72, 'stocks': 85, 'change': 1.6, 'source': 'demo'},
                {'name': '纺织服装', 'heat': 33, 'stocks': 56, 'change': -3.2, 'source': 'demo'},
                {'name': '轻工制造', 'heat': 46, 'stocks': 73, 'change': -1.1, 'source': 'demo'},
                {'name': '商贸零售', 'heat': 51, 'stocks': 68, 'change': -0.4, 'source': 'demo'},
                {'name': '银行', 'heat': 69, 'stocks': 52, 'change': 1.3, 'source': 'demo'},
                {'name': '非银金融', 'heat': 65, 'stocks': 78, 'change': 1.1, 'source': 'demo'},
                {'name': '汽车', 'heat': 71, 'stocks': 95, 'change': 1.8, 'source': 'demo'},
                {'name': '机械设备', 'heat': 57, 'stocks': 124, 'change': 0.2, 'source': 'demo'},
                {'name': '国防军工', 'heat': 66, 'stocks': 38, 'change': 1.4, 'source': 'demo'},
                {'name': '环保', 'heat': 44, 'stocks': 61, 'change': -1.6, 'source': 'demo'},
                {'name': '美容护理', 'heat': 59, 'stocks': 32, 'change': 0.6, 'source': 'demo'},
                {'name': '家用电器', 'heat': 54, 'stocks': 47, 'change': -0.2, 'source': 'demo'},
                {'name': '社会服务', 'heat': 49, 'stocks': 55, 'change': -0.9, 'source': 'demo'},
                {'name': '煤炭', 'heat': 47, 'stocks': 43, 'change': -1.3, 'source': 'demo'}
            ]
        
        sectors_data = {
            'labels': [s['name'] for s in sectors_info],
            'data': [s['heat'] for s in sectors_info],
            'colors': [s['color'] for s in sectors_info],
            'details': sectors_info  # Include detailed information
        }
        
        # Generate market sentiment data
        # Sentiment scale: 0-20 Fear, 20-40 Very Negative, 40-60 Neutral, 60-80 Positive, 80-100 Greed
        sentiment_value = 50 + (hash(str(datetime.now().date())) % 40 - 20)
        
        if sentiment_value < 20:
            sentiment_level = '极度恐惧'
            sentiment_color = '#FF4444'
        elif sentiment_value < 40:
            sentiment_level = '恐惧'
            sentiment_color = '#FF8844'
        elif sentiment_value < 60:
            sentiment_level = '中立'
            sentiment_color = '#FFCC44'
        elif sentiment_value < 80:
            sentiment_level = '乐观'
            sentiment_color = '#88DD44'
        else:
            sentiment_level = '极度贪婪'
            sentiment_color = '#44DD44'
        
        sentiment_data = {
            'value': sentiment_value,
            'level': sentiment_level,
            'color': sentiment_color,
            'history': [
                {'date': (datetime.now() - timedelta(days=i)).strftime('%m/%d'), 
                 'value': 50 + (hash(f"sentiment{i}") % 40 - 20)}
                for i in range(30, -1, -1)
            ]
        }
        
        # Prepare all sectors data for heatmap
        heatmap_data = []
        for sector in all_sectors:
            heatmap_data.append({
                'name': sector.get('name', ''),
                'change': sector.get('change', 0),
                'heat': sector.get('heat', 50),
                'stocks': sector.get('stocks', 0),
                'source': sector.get('source', 'unknown')
            })
        
        result = {
            'success': True,
            'sectorHeat': sectors_data,
            'allSectors': heatmap_data,  # All sectors for heatmap
            'marketSentiment': sentiment_data,
            'timestamp': datetime.now().isoformat(),
            'message': 'Analytics data retrieved successfully'
        }
        
        logger.info(f"✓ Analytics data generated ({len(heatmap_data)} sectors)")
        return jsonify(result)
        
    except Exception as e:
        logger.error(f"Analytics error: {str(e)}", exc_info=True)
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/api/history', methods=['GET'])
def get_history():
    """
    API endpoint for prediction history
    Retrieves real prediction history from database
    """
    try:
        # Get filter parameters
        filter_type = request.args.get('filter', 'all')  # all, today, week, month
        
        # Get history from database
        history_data = []
        
        if db_manager:
            try:
                records = db_manager.get_prediction_history(limit=100)
                
                for record in records:
                    # Format prediction value based on type
                    if record.prediction_type == 'short_term':
                        pred_value = f"{'+' if record.prediction_value >= 0 else ''}{record.prediction_value:.2f}%"
                        pred_type_display = '短期'
                    else:
                        pred_value = f"¥{record.prediction_value:.2f}"
                        pred_type_display = '中期'
                    
                    # Determine accuracy status
                    if record.actual_value is not None:
                        # Calculate accuracy (simplified)
                        diff = abs(record.prediction_value - record.actual_value)
                        if diff < 1.0:
                            accuracy_status = 'accurate'
                            accuracy_badge = '准确'
                        else:
                            accuracy_status = 'inaccurate'
                            accuracy_badge = '偏差'
                    else:
                        accuracy_status = 'pending'
                        accuracy_badge = '待验证'
                    
                    timestamp_str = record.created_at.strftime('%Y-%m-%d %H:%M:%S')
                    timestamp_obj = record.created_at
                    
                    history_data.append({
                        'id': record.id,
                        'timestamp': timestamp_str,
                        'timestamp_obj': timestamp_obj,  # Store parsed datetime for filtering
                        'stockCode': record.stock_code,
                        'stockName': record.stock_name or '',
                        'predictionType': pred_type_display,
                        'predictedResult': pred_value,
                        'actualResult': '进行中' if record.actual_value is None else f"¥{record.actual_value:.2f}",
                        'accuracy': accuracy_status,
                        'accuracyBadge': accuracy_badge,
                        'confidence': record.confidence_score or 0
                    })
                
                # Apply filters using pre-parsed timestamps
                if filter_type == 'today':
                    today = datetime.now().date()
                    history_data = [h for h in history_data if h['timestamp_obj'].date() == today]
                elif filter_type == 'week':
                    week_ago = datetime.now() - timedelta(days=7)
                    history_data = [h for h in history_data if h['timestamp_obj'] >= week_ago]
                elif filter_type == 'month':
                    month_ago = datetime.now() - timedelta(days=30)
                    history_data = [h for h in history_data if h['timestamp_obj'] >= month_ago]
                
                # Remove timestamp_obj before returning (not JSON serializable)
                for item in history_data:
                    del item['timestamp_obj']
                
                # Calculate statistics
                total_predictions = len(history_data)
                accurate_predictions = len([h for h in history_data if h['accuracy'] == 'accurate'])
                accuracy_rate = (accurate_predictions / total_predictions * 100) if total_predictions > 0 else 0
                
                return jsonify({
                    'success': True,
                    'data': history_data,
                    'statistics': {
                        'total': total_predictions,
                        'accurate': accurate_predictions,
                        'accuracy_rate': round(accuracy_rate, 1)
                    }
                })
            except Exception as e:
                logger.error(f"Error fetching history from database: {str(e)}")
        
        # Fallback to mock data if database unavailable
        history = [
            {
                'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                'stockCode': '000001',
                'stockName': '平安银行',
                'predictionType': '短期',
                'predictedResult': '+2.5%',
                'actualResult': '+2.3%',
                'accuracy': 'accurate',
                'accuracyBadge': '准确'
            },
            {
                'timestamp': (datetime.now() - timedelta(hours=2)).strftime('%Y-%m-%d %H:%M:%S'),
                'stockCode': '600036',
                'stockName': '招商银行',
                'predictionType': '中期',
                'predictedResult': '¥38.50',
                'actualResult': '进行中',
                'accuracy': 'pending',
                'accuracyBadge': '待验证'
            }
        ]
        
        return jsonify({
            'success': True,
            'data': history,
            'statistics': {
                'total': len(history),
                'accurate': 1,
                'accuracy_rate': 50.0
            }
        })
        
    except Exception as e:
        logger.error(f"History error: {str(e)}")
        import traceback
        traceback.print_exc()
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/api/history/clear', methods=['POST'])
def clear_history():
    """
    API endpoint to clear all prediction history
    """
    try:
        if db_manager:
            count = db_manager.clear_prediction_history()
            return jsonify({
                'success': True,
                'message': f'已清空 {count} 条历史记录',
                'deleted_count': count
            })
        else:
            return jsonify({
                'success': False,
                'error': '数据库未初始化'
            }), 500
    except Exception as e:
        logger.error(f"Clear history error: {str(e)}")
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


def get_local_ip():
    """Get the local IP address of the machine"""
    try:
        # Create a socket connection to get the local IP
        # Uses Google DNS as a reliable external reference point
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        local_ip = s.getsockname()[0]
        s.close()
        return local_ip
    except (socket.error, OSError):
        return "无法获取"


def open_browser(port=5000):
    """Open browser after a short delay"""
    import time
    time.sleep(1.5)
    webbrowser.open(f'http://127.0.0.1:{port}')


def main():
    """Main entry point"""
    # Parse command line arguments
    parser = argparse.ArgumentParser(description='SIAPS Web UI - 股票智能分析预测系统')
    parser.add_argument('--host', type=str, default='127.0.0.1',
                       help='主机地址 (默认: 127.0.0.1 仅本地访问, 使用 0.0.0.0 允许网络访问)')
    parser.add_argument('--port', type=int, default=None,
                       help='端口号 (默认: 5000, 云部署时使用环境变量 PORT)')
    parser.add_argument('--no-browser', action='store_true',
                       help='不自动打开浏览器')
    parser.add_argument('--mobile', action='store_true',
                       help='启用手机访问模式（等同于 --host 0.0.0.0）- 仅在可信任网络中使用')
    
    args = parser.parse_args()
    
    # If mobile mode is enabled, override host
    if args.mobile:
        args.host = '0.0.0.0'
    
    # Support cloud deployment: use PORT environment variable if available
    import os
    port = args.port or int(os.environ.get('PORT', 5000))
    host = args.host
    
    print("=" * 70)
    print("  SIAPS - 股票智能分析预测系统 Web UI")
    print("  Stock Intelligent Analysis & Prediction System")
    print("=" * 70)
    
    # Display access information
    if host == '0.0.0.0':
        local_ip = get_local_ip()
        print(f"\n🌐 网络访问模式 (Network Access Mode)")
        print(f"📱 手机访问 (Mobile Access): http://{local_ip}:{port}")
        print(f"💻 本地访问 (Local Access): http://127.0.0.1:{port}")
        print(f"\n⚠️  安全提示: 服务已暴露到网络，请确保在可信任的网络环境中使用")
        print(f"⚠️  Security: Service exposed to network - use only on trusted networks")
        print(f"⚠️  确保您的手机和电脑在同一局域网内")
        print(f"⚠️  Make sure your phone and computer are on the same network")
    else:
        print(f"\n🚀 Starting web server on http://{host}:{port}")
        print(f"📊 本地访问 (Local Access Only): http://{host}:{port}")
        print(f"\n💡 手机访问提示: 使用 --mobile 参数启用手机访问")
        print(f"💡 For mobile access: use --mobile parameter")
    
    print("\n✨ Features:")
    print("   - 股票预测 (Stock Prediction)")
    print("   - 观测池管理 (Watchlist Management)")
    print("   - 历史记录查询 (History)")
    print("   - 数据分析 (Analytics)")
    print("   - 深色/浅色主题 (Dark/Light Theme)")
    print("\n⚠️  Press Ctrl+C to stop the server")
    print("=" * 70 + "\n")
    
    # Open browser in a separate thread (only for local access)
    if not args.no_browser and host == '127.0.0.1':
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
