#!/usr/bin/env python3
"""
Unit tests for technical indicator signal calculation
"""
import sys
from pathlib import Path

# Add project root to Python path
ROOT_DIR = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT_DIR))


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


class TestIndicatorSignals:
    """Test cases for indicator signal calculation"""
    
    def test_rsi_bullish(self):
        """Test RSI in oversold range (20-40) returns bullish"""
        indicators = {'RSI': 35.0}
        signals = calculate_indicator_signals(15.0, indicators)
        assert signals['RSI'] == 'bullish', f"Expected RSI to be bullish but got {signals['RSI']}"
        print("✓ RSI bullish test passed")
    
    def test_rsi_bearish(self):
        """Test RSI in overbought range (60-80) returns bearish"""
        indicators = {'RSI': 70.0}
        signals = calculate_indicator_signals(15.0, indicators)
        assert signals['RSI'] == 'bearish', f"Expected RSI to be bearish but got {signals['RSI']}"
        print("✓ RSI bearish test passed")
    
    def test_rsi_neutral(self):
        """Test RSI in neutral range (40-60) returns neutral"""
        indicators = {'RSI': 50.0}
        signals = calculate_indicator_signals(15.0, indicators)
        assert signals['RSI'] == 'neutral', f"Expected RSI to be neutral but got {signals['RSI']}"
        print("✓ RSI neutral test passed")
    
    def test_rsi_boundaries(self):
        """Test RSI boundary values"""
        # RSI = 20 should be bullish
        signals = calculate_indicator_signals(15.0, {'RSI': 20.0})
        assert signals['RSI'] == 'bullish', "RSI 20 should be bullish"
        
        # RSI = 40 should be bullish
        signals = calculate_indicator_signals(15.0, {'RSI': 40.0})
        assert signals['RSI'] == 'bullish', "RSI 40 should be bullish"
        
        # RSI = 60 should be bearish
        signals = calculate_indicator_signals(15.0, {'RSI': 60.0})
        assert signals['RSI'] == 'bearish', "RSI 60 should be bearish"
        
        # RSI = 80 should be bearish
        signals = calculate_indicator_signals(15.0, {'RSI': 80.0})
        assert signals['RSI'] == 'bearish', "RSI 80 should be bearish"
        
        print("✓ RSI boundary test passed")
    
    def test_macd_positive(self):
        """Test MACD > 0 returns bullish"""
        indicators = {'MACD': 0.5}
        signals = calculate_indicator_signals(15.0, indicators)
        assert signals['MACD'] == 'bullish', f"Expected MACD to be bullish but got {signals['MACD']}"
        print("✓ MACD positive test passed")
    
    def test_macd_negative(self):
        """Test MACD < 0 returns bearish"""
        indicators = {'MACD': -0.2}
        signals = calculate_indicator_signals(15.0, indicators)
        assert signals['MACD'] == 'bearish', f"Expected MACD to be bearish but got {signals['MACD']}"
        print("✓ MACD negative test passed")
    
    def test_macd_zero(self):
        """Test MACD = 0 returns bearish"""
        indicators = {'MACD': 0.0}
        signals = calculate_indicator_signals(15.0, indicators)
        assert signals['MACD'] == 'bearish', f"Expected MACD to be bearish but got {signals['MACD']}"
        print("✓ MACD zero test passed")
    
    def test_kdj_oversold(self):
        """Test KDJ < 20 returns bullish"""
        indicators = {'KDJ': 15.0}
        signals = calculate_indicator_signals(15.0, indicators)
        assert signals['KDJ'] == 'bullish', f"Expected KDJ to be bullish but got {signals['KDJ']}"
        print("✓ KDJ oversold test passed")
    
    def test_kdj_overbought(self):
        """Test KDJ > 80 returns bearish"""
        indicators = {'KDJ': 85.0}
        signals = calculate_indicator_signals(15.0, indicators)
        assert signals['KDJ'] == 'bearish', f"Expected KDJ to be bearish but got {signals['KDJ']}"
        print("✓ KDJ overbought test passed")
    
    def test_kdj_neutral(self):
        """Test KDJ between 20-80 returns neutral"""
        indicators = {'KDJ': 50.0}
        signals = calculate_indicator_signals(15.0, indicators)
        assert signals['KDJ'] == 'neutral', f"Expected KDJ to be neutral but got {signals['KDJ']}"
        print("✓ KDJ neutral test passed")
    
    def test_ma_bullish(self):
        """Test MA5 > MA20 returns bullish for both"""
        indicators = {'MA5': 15.2, 'MA20': 14.8}
        signals = calculate_indicator_signals(15.0, indicators)
        assert signals['MA5'] == 'bullish', f"Expected MA5 to be bullish but got {signals['MA5']}"
        assert signals['MA20'] == 'bullish', f"Expected MA20 to be bullish but got {signals['MA20']}"
        print("✓ MA bullish test passed")
    
    def test_ma_bearish(self):
        """Test MA5 < MA20 returns bearish for both"""
        indicators = {'MA5': 14.5, 'MA20': 15.0}
        signals = calculate_indicator_signals(15.0, indicators)
        assert signals['MA5'] == 'bearish', f"Expected MA5 to be bearish but got {signals['MA5']}"
        assert signals['MA20'] == 'bearish', f"Expected MA20 to be bearish but got {signals['MA20']}"
        print("✓ MA bearish test passed")
    
    def test_boll_near_lower(self):
        """Test price near lower band returns bullish"""
        indicators = {'BOLL': '10.0-20.0'}  # lower=10, upper=20, threshold_lower=13
        current_price = 12.0  # Below threshold_lower
        signals = calculate_indicator_signals(current_price, indicators)
        assert signals['BOLL'] == 'bullish', f"Expected BOLL to be bullish but got {signals['BOLL']}"
        print("✓ BOLL near lower band test passed")
    
    def test_boll_near_upper(self):
        """Test price near upper band returns bearish"""
        indicators = {'BOLL': '10.0-20.0'}  # lower=10, upper=20, threshold_upper=17
        current_price = 18.0  # Above threshold_upper
        signals = calculate_indicator_signals(current_price, indicators)
        assert signals['BOLL'] == 'bearish', f"Expected BOLL to be bearish but got {signals['BOLL']}"
        print("✓ BOLL near upper band test passed")
    
    def test_boll_neutral(self):
        """Test price in middle range returns neutral"""
        indicators = {'BOLL': '14.0-16.0'}  # lower=14, upper=16
        current_price = 15.0  # In the middle
        signals = calculate_indicator_signals(current_price, indicators)
        assert signals['BOLL'] == 'neutral', f"Expected BOLL to be neutral but got {signals['BOLL']}"
        print("✓ BOLL neutral test passed")
    
    def test_all_indicators_combined(self):
        """Test all indicators together"""
        indicators = {
            'RSI': 35.0,      # Bullish
            'MACD': -0.2,     # Bearish
            'KDJ': 15.0,      # Bullish
            'MA5': 15.2,      # Bullish
            'MA20': 14.85,    # Bullish
            'BOLL': '12.5-16.8'  # Should be neutral at 14.5
        }
        current_price = 14.5
        signals = calculate_indicator_signals(current_price, indicators)
        
        assert signals['RSI'] == 'bullish'
        assert signals['MACD'] == 'bearish'
        assert signals['KDJ'] == 'bullish'
        assert signals['MA5'] == 'bullish'
        assert signals['MA20'] == 'bullish'
        assert signals['BOLL'] == 'neutral'
        print("✓ All indicators combined test passed")
    
    def run_all_tests(self):
        """Run all test methods"""
        print("\nRunning indicator signal tests...\n")
        test_methods = [
            self.test_rsi_bullish,
            self.test_rsi_bearish,
            self.test_rsi_neutral,
            self.test_rsi_boundaries,
            self.test_macd_positive,
            self.test_macd_negative,
            self.test_macd_zero,
            self.test_kdj_oversold,
            self.test_kdj_overbought,
            self.test_kdj_neutral,
            self.test_ma_bullish,
            self.test_ma_bearish,
            self.test_boll_near_lower,
            self.test_boll_near_upper,
            self.test_boll_neutral,
            self.test_all_indicators_combined,
        ]
        
        passed = 0
        failed = 0
        
        for test_method in test_methods:
            try:
                test_method()
                passed += 1
            except AssertionError as e:
                print(f"✗ {test_method.__name__} failed: {e}")
                failed += 1
            except Exception as e:
                print(f"✗ {test_method.__name__} error: {e}")
                failed += 1
        
        print(f"\n{'='*60}")
        print(f"Test Results: {passed} passed, {failed} failed")
        print(f"{'='*60}\n")
        
        return failed == 0


if __name__ == '__main__':
    tester = TestIndicatorSignals()
    success = tester.run_all_tests()
    sys.exit(0 if success else 1)
