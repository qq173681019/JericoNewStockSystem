#!/usr/bin/env python3
"""测试多时间框架预测API"""
import sys
import json
from datetime import datetime, timedelta
import pandas as pd
import numpy as np

# 测试导入
try:
    from src.prediction_models.multi_model_predictor import MultiModelPredictor
    print("✅ MultiModelPredictor导入成功")
except Exception as e:
    print(f"❌ 导入失败: {e}")
    sys.exit(1)

# 创建测试数据
print("\n创建测试股票数据...")
np.random.seed(42)
dates = pd.date_range('2024-01-01', periods=60, freq='D')
base_price = 100.0
noise = np.random.randn(60) * 2
trend = np.linspace(0, 10, 60)
prices = base_price + trend + noise

data = pd.DataFrame({
    'close': prices,
    'high': prices + abs(np.random.randn(60) * 1),
    'low': prices - abs(np.random.randn(60) * 1),
    'volume': np.random.randint(1000000, 5000000, 60)
}, index=dates)

print(f"✅ 数据准备完成: {len(data)}天历史数据")
print(f"   最新价格: ¥{data['close'].iloc[-1]:.2f}")
print(f"   价格区间: ¥{data['close'].min():.2f} - ¥{data['close'].max():.2f}")

# 测试预测器
print("\n" + "="*60)
print("测试多时间框架预测")
print("="*60)

predictor = MultiModelPredictor()

for timeframe in ['1hour', '3day', '30day']:
    print(f"\n{'='*60}")
    print(f"⏱️  {timeframe.upper()} 预测测试")
    print(f"{'='*60}")
    
    # Expected number of predictions for each timeframe
    expected_points = {'1hour': 12, '3day': 3, '30day': 90}
    
    try:
        result = predictor.predict_multi_timeframe(data, timeframe=timeframe)
        
        if 'error' in result:
            print(f"❌ 预测失败: {result['error']}")
            continue
        
        # Validate result structure
        assert 'ensemble' in result, "缺少ensemble预测结果"
        assert 'prices' in result['ensemble'], "缺少价格预测数据"
        assert 'confidence' in result, "缺少信心度数据"
        assert 'price_change_pcts' in result, "缺少价格变化百分比"
        assert 'trading_signal' in result, "缺少交易信号"
        
        # Validate prediction length
        ensemble_prices = result['ensemble']['prices']
        assert len(ensemble_prices) == expected_points[timeframe], \
            f"预测点数不匹配: 期望{expected_points[timeframe]}, 实际{len(ensemble_prices)}"
        
        # Validate confidence range
        confidence = result['confidence']
        assert 0 <= confidence <= 1, f"信心度超出范围: {confidence}"
            
        # 提取结果
        ensemble_prices = result['ensemble']['prices']
        confidence = result['confidence']
        price_changes = result['price_change_pcts']
        signal = result['trading_signal']
        
        # 显示结果
        print(f"\n📊 预测结果:")
        print(f"   预测点数: {len(ensemble_prices)}个")
        print(f"   当前价格: ¥{data['close'].iloc[-1]:.2f}")
        print(f"   预测价格: ¥{ensemble_prices[0]:.2f} → ¥{ensemble_prices[-1]:.2f}")
        print(f"   预期变化: {price_changes[-1]:+.2f}%")
        print(f"   信心度: {confidence:.1%}")
        print(f"\n💡 交易信号:")
        print(f"   建议: {signal['recommendation']}")
        print(f"   动作: {signal['action']}")
        print(f"   理由: 预期变化 {signal['expected_change']:+.2f}%")
        
        # 模型细节
        print(f"\n🔧 模型详情:")
        for model_name in ['technical', 'machine_learning', 'support_resistance']:
            if model_name in result and 'prices' in result[model_name]:
                model_prices = result[model_name]['prices']
                model_change = (model_prices[-1] - data['close'].iloc[-1]) / data['close'].iloc[-1] * 100
                print(f"   {model_name}: ¥{model_prices[-1]:.2f} ({model_change:+.2f}%)")
        
        # 判断预测质量
        print(f"\n✅ 预测成功")
        if confidence > 0.8:
            print(f"   质量评级: ⭐⭐⭐ 高信心度")
        elif confidence > 0.6:
            print(f"   质量评级: ⭐⭐ 中等信心度")
        else:
            print(f"   质量评级: ⭐ 低信心度")
            
    except Exception as e:
        print(f"❌ 预测过程出错: {e}")
        import traceback
        traceback.print_exc()

print("\n" + "="*60)
print("✅ 所有测试完成")
print("="*60)
print("\n📋 总结:")
print("   - 1小时预测: 短期波动预测，适合日内交易")
print("   - 3天预测: 短期趋势预测，适合波段交易")
print("   - 30天预测: 中期目标预测，适合趋势投资")
print("\n⚠️  注意: 预测仅供参考，投资有风险，决策需谨慎！")
