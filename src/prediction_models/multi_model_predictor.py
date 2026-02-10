#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
多模型集成预测模块
基于 Kronos-custom 算法改进
版本: v1.0.0

实现技术指标、机器学习、支撑阻力位三种方法的多时间框架预测

算法架构:
1. 技术指标预测 (30%权重): MACD, RSI, 移动平均线, 布林带
2. 机器学习预测 (40%权重): Random Forest + 动态特征窗口
3. 支撑阻力位预测 (30%权重): 关键价位识别与趋势分析

支持的时间框架:
- 1小时预测: 基于分钟级数据
- 3天预测: 基于日线数据
- 30天预测: 基于日线数据（实际为中期3个月目标）
"""

import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import StandardScaler
import warnings
warnings.filterwarnings('ignore')


class MultiModelPredictor:
    """多模型集成预测器"""
    
    def __init__(self, weights=None):
        """
        初始化预测器
        weights: dict, 各模型权重 {'technical': 0.3, 'ml': 0.4, 'support_resistance': 0.3}
        """
        self.weights = weights or {'technical': 0.3, 'ml': 0.4, 'support_resistance': 0.3}
        self.scaler = StandardScaler()
        
    def predict_multi_timeframe(self, stock_data, timeframe='3day'):
        """
        多时间框架预测主函数
        stock_data: DataFrame, 股票历史数据，需包含 'close', 'high', 'low', 'volume' 列
        timeframe: str, 时间框架 ('1hour', '3day', '30day')
        返回: dict, 包含各模型预测结果和集成结果
        """
        # 根据时间框架确定预测点数
        if timeframe == '30min':
            pred_points = 6   # 30分钟，假设5分钟一个点
            window_size = 60  # 使用5小时历史数据
        elif timeframe == '1day':
            pred_points = 1   # 1天
            window_size = 10  # 使用10天历史数据
        else:
            # 默认1天预测
            pred_points = 1
            window_size = 10
            
        results = {}
        
        try:
            # 确保有足够的数据
            if len(stock_data) < window_size:
                return self._fallback_prediction(stock_data, pred_points, timeframe)
            
            # 方法1: 技术指标预测
            tech_pred = self._technical_indicator_prediction(stock_data, pred_points, timeframe)
            results['technical'] = tech_pred
            
            # 方法2: 机器学习预测
            ml_pred = self._machine_learning_prediction(stock_data, pred_points, window_size)
            results['machine_learning'] = ml_pred
            
            # 方法3: 支撑阻力位预测
            sr_pred = self._support_resistance_prediction(stock_data, pred_points)
            results['support_resistance'] = sr_pred
            
            # 集成预测
            ensemble_pred = self._ensemble_prediction(tech_pred, ml_pred, sr_pred)
            results['ensemble'] = ensemble_pred
            
            # 计算预测信心度
            confidence = self._calculate_confidence(tech_pred, ml_pred, sr_pred)
            results['confidence'] = confidence
            
            # 计算变化百分比
            current_price = stock_data['close'].iloc[-1]
            predicted_prices = ensemble_pred['prices']
            price_changes = [(p - current_price) / current_price * 100 for p in predicted_prices]
            results['price_change_pcts'] = price_changes
            
            # 生成交易建议
            results['trading_signal'] = self._generate_trading_signal(
                current_price, predicted_prices, confidence
            )
            
            return results
            
        except Exception as e:
            print(f"多模型预测失败: {str(e)}")
            import traceback
            traceback.print_exc()
            return self._fallback_prediction(stock_data, pred_points, timeframe)
    
    def _technical_indicator_prediction(self, data, pred_points, timeframe):
        """方法1: 基于技术指标的预测 - 增强量化算法"""
        try:
            data = data.copy()
            
            # === 计算核心技术指标 ===
            
            # MACD (趋势指标)
            exp1 = data['close'].ewm(span=12, adjust=False).mean()
            exp2 = data['close'].ewm(span=26, adjust=False).mean()
            macd = exp1 - exp2
            signal = macd.ewm(span=9, adjust=False).mean()
            macd_histogram = macd - signal
            
            # RSI (超买超卖指标)
            delta = data['close'].diff()
            gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
            loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
            rs = gain / loss
            rsi = 100 - (100 / (1 + rs))
            
            # 布林带 (波动率指标)
            ma20 = data['close'].rolling(window=20).mean()
            std20 = data['close'].rolling(window=20).std()
            upper_band = ma20 + (std20 * 2)
            lower_band = ma20 - (std20 * 2)
            
            # KDJ (随机指标)
            low_14 = data['low'].rolling(window=14).min()
            high_14 = data['high'].rolling(window=14).max()
            rsv = (data['close'] - low_14) / (high_14 - low_14) * 100
            k = rsv.ewm(com=2, adjust=False).mean()
            d = k.ewm(com=2, adjust=False).mean()
            j = 3 * k - 2 * d
            
            # 成交量趋势
            volume_ma5 = data['volume'].rolling(window=5).mean()
            volume_trend = data['volume'].iloc[-1] / volume_ma5.iloc[-1] if volume_ma5.iloc[-1] > 0 else 1
            
            # === 生成交易信号 ===
            current_price = data['close'].iloc[-1]
            
            # 1. MACD信号 (-1到1)
            macd_signal = np.tanh(macd_histogram.iloc[-1] / current_price * 100)
            
            # 2. RSI信号 (-1到1)
            rsi_value = rsi.iloc[-1]
            if rsi_value > 70:
                rsi_signal = -0.5  # 超买，看跌
            elif rsi_value < 30:
                rsi_signal = 0.5   # 超卖，看涨
            else:
                rsi_signal = (rsi_value - 50) / 50 * 0.3
            
            # 3. 布林带信号 (-1到1)
            bb_position = (current_price - lower_band.iloc[-1]) / (upper_band.iloc[-1] - lower_band.iloc[-1])
            bb_signal = (bb_position - 0.5) * 2  # 转换为-1到1
            
            # 4. KDJ信号 (-1到1)
            kdj_signal = (j.iloc[-1] - 50) / 50
            kdj_signal = max(min(kdj_signal, 1), -1)
            
            # 5. 成交量信号
            volume_signal = (volume_trend - 1) * 0.5
            volume_signal = max(min(volume_signal, 0.5), -0.5)
            
            # === 根据时间框架调整权重和波动率 ===
            if timeframe == '30min':
                # 30分钟：高频交易，注重短期动量
                signal_weights = {
                    'macd': 0.15,
                    'rsi': 0.25,
                    'bollinger': 0.30,
                    'kdj': 0.20,
                    'volume': 0.10
                }
                base_volatility = 0.003  # 0.3% 基础波动
                momentum_factor = 1.5    # 动量放大系数
                
            elif timeframe == '1day':
                # 1天：日内交易，平衡趋势和动量
                signal_weights = {
                    'macd': 0.30,
                    'rsi': 0.20,
                    'bollinger': 0.20,
                    'kdj': 0.20,
                    'volume': 0.10
                }
                base_volatility = 0.015  # 1.5% 基础波动
                momentum_factor = 1.2
            
            elif timeframe == '1hour':
                # 1小时
                signal_weights = {
                    'macd': 0.20,
                    'rsi': 0.25,
                    'bollinger': 0.25,
                    'kdj': 0.20,
                    'volume': 0.10
                }
                base_volatility = 0.005
                momentum_factor = 1.3
            
            elif timeframe == '3day':
                # 3天
                signal_weights = {
                    'macd': 0.30,
                    'rsi': 0.20,
                    'bollinger': 0.20,
                    'kdj': 0.20,
                    'volume': 0.10
                }
                base_volatility = 0.02
                momentum_factor = 1.0
                
            else:
                # 默认设置 (30day)
                signal_weights = {
                    'macd': 0.35,
                    'rsi': 0.20,
                    'bollinger': 0.20,
                    'kdj': 0.15,
                    'volume': 0.10
                }
                base_volatility = 0.03
                momentum_factor = 1.0
            
            # === 生成预测价格序列 ===
            predictions = []
            current = current_price
            
            for i in range(pred_points):
                # 计算综合信号
                total_signal = (
                    macd_signal * signal_weights['macd'] +
                    rsi_signal * signal_weights['rsi'] +
                    bb_signal * signal_weights['bollinger'] +
                    kdj_signal * signal_weights['kdj'] +
                    volume_signal * signal_weights['volume']
                )
                
                # 应用动量和波动率
                price_change_pct = total_signal * base_volatility * momentum_factor
                
                # 添加微小随机波动(模拟市场噪音)
                noise = np.random.normal(0, base_volatility * 0.2)
                price_change_pct += noise
                
                # 限制单步最大变化
                max_change = base_volatility * 2
                price_change_pct = max(min(price_change_pct, max_change), -max_change)
                
                # 计算新价格
                current = current * (1 + price_change_pct)
                predictions.append(current)
                
                # 信号衰减(模拟市场动态调整)
                macd_signal *= 0.9
                rsi_signal *= 0.9
                bb_signal *= 0.95
                kdj_signal *= 0.9
            
            return {
                'prices': predictions,
                'method': 'technical_indicators_enhanced',
                'indicators': {
                    'MACD': float(macd.iloc[-1]),
                    'MACD_Signal': float(signal.iloc[-1]),
                    'RSI': float(rsi.iloc[-1]),
                    'Bollinger_Upper': float(upper_band.iloc[-1]),
                    'Bollinger_Lower': float(lower_band.iloc[-1]),
                    'KDJ_K': float(k.iloc[-1]),
                    'KDJ_D': float(d.iloc[-1]),
                    'KDJ_J': float(j.iloc[-1]),
                    'Volume_Trend': float(volume_trend),
                    '综合信号': float(total_signal)
                }
            }
            
        except Exception as e:
            print(f"技术指标预测失败: {str(e)}")
            import traceback
            traceback.print_exc()
            return self._simple_trend_prediction(data, pred_points)
    
    def _machine_learning_prediction(self, data, pred_points, window_size):
        """方法2: 基于机器学习的预测"""
        try:
            data = data.copy()
            
            # 创建特征
            features = []
            targets = []
            
            # 使用滑动窗口创建训练数据
            for i in range(window_size, len(data)):
                # 特征: 过去window_size天的价格、成交量等
                window_data = data.iloc[i-window_size:i]
                
                feature_vector = [
                    window_data['close'].mean(),
                    window_data['close'].std(),
                    window_data['high'].max(),
                    window_data['low'].min(),
                    window_data['volume'].mean() if 'volume' in window_data.columns else 0,
                    (window_data['close'].iloc[-1] - window_data['close'].iloc[0]) / window_data['close'].iloc[0]
                ]
                
                features.append(feature_vector)
                targets.append(data['close'].iloc[i])
            
            if len(features) < 5:
                # 数据不足，使用简单预测
                return self._simple_trend_prediction(data, pred_points)
            
            # 训练随机森林模型
            X = np.array(features)
            y = np.array(targets)
            
            # 标准化特征
            X_scaled = self.scaler.fit_transform(X)
            
            # 训练模型
            model = RandomForestRegressor(n_estimators=50, max_depth=10, random_state=42)
            model.fit(X_scaled, y)
            
            # 预测
            predictions = []
            current_data = data.copy()
            
            for i in range(pred_points):
                # 使用最近的数据作为特征
                window_data = current_data.iloc[-window_size:]
                
                feature_vector = [
                    window_data['close'].mean(),
                    window_data['close'].std(),
                    window_data['high'].max(),
                    window_data['low'].min(),
                    window_data['volume'].mean() if 'volume' in window_data.columns else 0,
                    (window_data['close'].iloc[-1] - window_data['close'].iloc[0]) / window_data['close'].iloc[0]
                ]
                
                X_pred = np.array([feature_vector])
                X_pred_scaled = self.scaler.transform(X_pred)
                
                pred_price = model.predict(X_pred_scaled)[0]
                predictions.append(pred_price)
                
                # 添加预测结果到数据中，用于下一次预测
                new_row = current_data.iloc[-1:].copy()
                new_row['close'] = pred_price
                current_data = pd.concat([current_data, new_row], ignore_index=True)
            
            return {
                'prices': predictions,
                'method': 'machine_learning',
                'model': 'RandomForest'
            }
        except Exception as e:
            print(f"机器学习预测失败: {str(e)}")
            import traceback
            traceback.print_exc()
            return self._simple_trend_prediction(data, pred_points)
    
    def _support_resistance_prediction(self, data, pred_points):
        """方法3: 基于支撑阻力位的预测"""
        try:
            data = data.copy()
            
            # 识别支撑位和阻力位
            high_prices = data['high'].values
            low_prices = data['low'].values
            close_prices = data['close'].values
            
            # 找到局部最高点和最低点
            resistance_levels = []
            support_levels = []
            
            for i in range(2, len(high_prices) - 2):
                # 阻力位: 局部最高点
                if high_prices[i] == max(high_prices[i-2:i+3]):
                    resistance_levels.append(high_prices[i])
                
                # 支撑位: 局部最低点
                if low_prices[i] == min(low_prices[i-2:i+3]):
                    support_levels.append(low_prices[i])
            
            # 如果没有找到支撑阻力位，使用简单方法
            if not resistance_levels:
                resistance_levels = [max(high_prices)]
            if not support_levels:
                support_levels = [min(low_prices)]
            
            # 最近的支撑和阻力位
            current_price = close_prices[-1]
            next_resistance = min([r for r in resistance_levels if r > current_price], default=max(resistance_levels))
            next_support = max([s for s in support_levels if s < current_price], default=min(support_levels))
            
            # 计算趋势
            recent_prices = close_prices[-10:]
            trend = (recent_prices[-1] - recent_prices[0]) / recent_prices[0]
            
            # 预测
            predictions = []
            current = current_price
            
            for i in range(pred_points):
                # 根据趋势和支撑阻力位预测
                if trend > 0:
                    # 上升趋势，向阻力位移动
                    predicted = current + (next_resistance - current) * 0.3
                elif trend < 0:
                    # 下降趋势，向支撑位移动
                    predicted = current + (next_support - current) * 0.3
                else:
                    # 横盘，小幅随机波动（-0.5% to +0.5%）
                    fluctuation = (hash(f"{current}{i}") % 100 - 50) / 10000
                    predicted = current * (1 + fluctuation)
                
                predictions.append(predicted)
                current = predicted
            
            return {
                'prices': predictions,
                'method': 'support_resistance',
                'levels': {
                    'resistance': next_resistance,
                    'support': next_support
                }
            }
        except Exception as e:
            print(f"支撑阻力位预测失败: {str(e)}")
            return self._simple_trend_prediction(data, pred_points)
    
    def _ensemble_prediction(self, tech_pred, ml_pred, sr_pred):
        """集成多个模型的预测结果"""
        try:
            # 获取各模型的预测价格
            tech_prices = np.array(tech_pred['prices'])
            ml_prices = np.array(ml_pred['prices'])
            sr_prices = np.array(sr_pred['prices'])
            
            # 加权平均
            ensemble_prices = (
                tech_prices * self.weights['technical'] +
                ml_prices * self.weights['ml'] +
                sr_prices * self.weights['support_resistance']
            )
            
            return {
                'prices': ensemble_prices.tolist(),
                'method': 'ensemble',
                'weights': self.weights
            }
        except Exception as e:
            print(f"集成预测失败: {str(e)}")
            # 如果集成失败，返回技术指标预测
            return tech_pred
    
    def _calculate_confidence(self, tech_pred, ml_pred, sr_pred):
        """计算预测信心度"""
        try:
            # 计算三个模型预测的一致性
            tech_prices = np.array(tech_pred['prices'])
            ml_prices = np.array(ml_pred['prices'])
            sr_prices = np.array(sr_pred['prices'])
            
            # 计算标准差，标准差越小说明一致性越高
            all_predictions = np.array([tech_prices, ml_prices, sr_prices])
            std_dev = np.std(all_predictions, axis=0).mean()
            mean_price = np.mean(all_predictions)
            
            # 归一化标准差
            normalized_std = std_dev / mean_price
            
            # 信心度: 1 - normalized_std * 10
            # 乘以10是为了将标准差放大到合适的范围，使信心度在0.5-0.95之间
            # 当三个模型预测差异大时，normalized_std会增大，信心度降低
            confidence = max(0.5, min(0.95, 1 - normalized_std * 10))
            
            return confidence
        except Exception as e:
            print(f"信心度计算失败: {str(e)}")
            return 0.70
    
    def _generate_trading_signal(self, current_price, predicted_prices, confidence):
        """生成交易建议"""
        try:
            # 计算平均预测变化
            avg_change = (predicted_prices[-1] - current_price) / current_price * 100
            
            # 根据变化幅度和信心度给出建议
            if avg_change > 5 and confidence > 0.7:
                recommendation = '强烈买入'
                action = 'strong_buy'
            elif avg_change > 2 and confidence > 0.6:
                recommendation = '买入'
                action = 'buy'
            elif avg_change > -2 and avg_change <= 2:
                recommendation = '持有'
                action = 'hold'
            elif avg_change > -5 and confidence > 0.6:
                recommendation = '卖出'
                action = 'sell'
            else:
                recommendation = '强烈卖出'
                action = 'strong_sell'
            
            return {
                'recommendation': recommendation,
                'action': action,
                'confidence': confidence,
                'expected_change': avg_change
            }
        except Exception as e:
            print(f"交易信号生成失败: {str(e)}")
            return {
                'recommendation': '持有',
                'action': 'hold',
                'confidence': 0.5,
                'expected_change': 0
            }
    
    def _simple_trend_prediction(self, data, pred_points):
        """简单的趋势预测（备用方法）"""
        try:
            close_prices = data['close'].values
            # 使用线性趋势
            recent_prices = close_prices[-min(10, len(close_prices)):]
            trend = (recent_prices[-1] - recent_prices[0]) / recent_prices[0] / len(recent_prices)
            
            predictions = []
            current = close_prices[-1]
            for i in range(pred_points):
                current = current * (1 + trend)
                predictions.append(current)
            
            return {
                'prices': predictions,
                'method': 'simple_trend'
            }
        except Exception as e:
            print(f"简单趋势预测失败: {str(e)}")
            last_price = data['close'].iloc[-1]
            return {
                'prices': [last_price] * pred_points,
                'method': 'fallback'
            }
    
    def _fallback_prediction(self, data, pred_points, timeframe):
        """备用预测方法（当其他方法都失败时）"""
        try:
            last_price = data['close'].iloc[-1]
            return {
                'technical': {'prices': [last_price] * pred_points, 'method': 'fallback'},
                'machine_learning': {'prices': [last_price] * pred_points, 'method': 'fallback'},
                'support_resistance': {'prices': [last_price] * pred_points, 'method': 'fallback'},
                'ensemble': {'prices': [last_price] * pred_points, 'method': 'fallback'},
                'confidence': 0.5,
                'price_change_pcts': [0] * pred_points,
                'trading_signal': {
                    'recommendation': '持有',
                    'action': 'hold',
                    'confidence': 0.5,
                    'expected_change': 0
                }
            }
        except Exception as e:
            print(f"备用预测也失败: {str(e)}")
            return {
                'error': str(e),
                'timeframe': timeframe
            }
