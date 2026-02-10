"""
Technical indicator signal calculation utilities
"""


def calculate_indicator_signals(current_price, indicators):
    """
    Calculate technical indicator signals
    
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
