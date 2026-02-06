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
        if timeframe == '1hour':
            pred_points = 12  # 1小时内，假设5分钟一个点
            window_size = 60  # 使用5小时历史数据
        elif timeframe == '3day':
            pred_points = 3   # 3天
            window_size = 10  # 使用10天历史数据
        elif timeframe == '30day':
            pred_points = 90  # 3个月（实际为中期目标）
            window_size = 30  # 使用30天历史数据
        else:
            # 默认3天预测
            pred_points = 3
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
        """方法1: 基于技术指标的预测"""
        try:
            # 计算技术指标
            data = data.copy()
            
            # MACD
            ema12 = data['close'].ewm(span=12, adjust=False).mean()
            ema26 = data['close'].ewm(span=26, adjust=False).mean()
            macd = ema12 - ema26
            signal = macd.ewm(span=9, adjust=False).mean()
            macd_hist = macd - signal
            
            # RSI
            delta = data['close'].diff()
            gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
            loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
            rs = gain / loss
            rsi = 100 - (100 / (1 + rs))
            
            # 移动平均线
            ma5 = data['close'].rolling(window=min(5, len(data))).mean()
            ma20 = data['close'].rolling(window=min(20, len(data))).mean()
            
            # 布林带
            bb_window = min(20, len(data))
            bb_middle = data['close'].rolling(window=bb_window).mean()
            bb_std = data['close'].rolling(window=bb_window).std()
            bb_upper = bb_middle + (bb_std * 2)
            bb_lower = bb_middle - (bb_std * 2)
            
            # 获取最新指标值
            latest_close = data['close'].iloc[-1]
            latest_macd = macd.iloc[-1] if not pd.isna(macd.iloc[-1]) else 0
            latest_signal = signal.iloc[-1] if not pd.isna(signal.iloc[-1]) else 0
            latest_rsi = rsi.iloc[-1] if not pd.isna(rsi.iloc[-1]) else 50
            latest_ma5 = ma5.iloc[-1] if not pd.isna(ma5.iloc[-1]) else latest_close
            latest_ma20 = ma20.iloc[-1] if not pd.isna(ma20.iloc[-1]) else latest_close
            latest_bb_upper = bb_upper.iloc[-1] if not pd.isna(bb_upper.iloc[-1]) else latest_close * 1.05
            latest_bb_lower = bb_lower.iloc[-1] if not pd.isna(bb_lower.iloc[-1]) else latest_close * 0.95
            
            # 预测逻辑
            predictions = []
            current_price = latest_close
            
            for i in range(pred_points):
                # MACD信号
                macd_signal = 1 if latest_macd > latest_signal else -1
                
                # RSI信号
                if latest_rsi > 70:
                    rsi_signal = -1  # 超买
                elif latest_rsi < 30:
                    rsi_signal = 1   # 超卖
                else:
                    rsi_signal = 0   # 中性
                
                # 均线信号
                ma_signal = 1 if latest_ma5 > latest_ma20 else -1
                
                # 布林带信号
                if current_price > latest_bb_upper:
                    bb_signal = -1  # 接近上轨，可能回调
                elif current_price < latest_bb_lower:
                    bb_signal = 1   # 接近下轨，可能反弹
                else:
                    bb_signal = 0   # 在带内
                
                # 综合信号
                total_signal = (macd_signal * 0.3 + rsi_signal * 0.2 + 
                               ma_signal * 0.3 + bb_signal * 0.2)
                
                # 根据时间框架调整变化幅度
                if timeframe == '1hour':
                    change_factor = 0.002  # 1小时内变化较小
                elif timeframe == '3day':
                    change_factor = 0.01   # 3天中等变化
                else:  # 30day
                    change_factor = 0.03   # 30天较大变化
                
                # 计算预测价格
                price_change = total_signal * change_factor * current_price
                current_price = current_price + price_change
                predictions.append(current_price)
            
            return {
                'prices': predictions,
                'method': 'technical_indicators',
                'indicators': {
                    'MACD': latest_macd,
                    'RSI': latest_rsi,
                    'MA5': latest_ma5,
                    'MA20': latest_ma20
                }
            }
        except Exception as e:
            print(f"技术指标预测失败: {str(e)}")
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
                    # 横盘，小幅波动
                    trend_price = current * (1 + trend * 0.5)
                    predicted = trend_price
                
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
            
            # 信心度: 1 - normalized_std，范围在0到1之间
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
