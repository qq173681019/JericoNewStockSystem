"""
Multi-Source Data Fetcher
Fetches stock data from multiple sources and compares reliability
Supports: AKShare, TuShare, Yahoo Finance, EastMoney
"""
import pandas as pd
from typing import Dict, List, Optional, Any
from datetime import datetime, timedelta
import sys
from pathlib import Path

# Add project root to Python path
ROOT_DIR = Path(__file__).parent.parent.parent
sys.path.insert(0, str(ROOT_DIR))

from src.utils import setup_logger

logger = setup_logger(__name__)


class MultiSourceDataFetcher:
    """Fetches data from multiple sources and provides reliability comparison"""
    
    def __init__(self):
        self.sources = {
            'akshare': self._init_akshare(),
            'tushare': self._init_tushare(),
            'yahoo': self._init_yahoo(),
            'eastmoney': self._init_eastmoney()
        }
        self.available_sources = {k: v for k, v in self.sources.items() if v is not None}
        logger.info(f"Initialized with sources: {list(self.available_sources.keys())}")
    
    def _init_akshare(self):
        """Initialize AKShare"""
        try:
            import akshare as ak
            logger.info("✓ AKShare initialized")
            return ak
        except ImportError:
            logger.warning("✗ AKShare not available")
            return None
    
    def _init_tushare(self):
        """Initialize TuShare"""
        try:
            import tushare as ts
            # TuShare requires token, using default for testing
            logger.info("✓ TuShare initialized")
            return ts
        except ImportError:
            logger.warning("✗ TuShare not available")
            return None
    
    def _init_yahoo(self):
        """Initialize Yahoo Finance"""
        try:
            import yfinance as yf
            logger.info("✓ Yahoo Finance initialized")
            return yf
        except ImportError:
            logger.warning("✗ Yahoo Finance not available")
            return None
    
    def _init_eastmoney(self):
        """Initialize EastMoney (via requests)"""
        try:
            import requests
            logger.info("✓ EastMoney initialized")
            return requests
        except ImportError:
            logger.warning("✗ EastMoney not available")
            return None
    
    def fetch_from_akshare(self, stock_code: str) -> Optional[Dict[str, Any]]:
        """Fetch real-time data from AKShare"""
        if 'akshare' not in self.available_sources:
            return None
        
        try:
            ak = self.available_sources['akshare']
            
            # Determine market
            if stock_code.startswith('6'):
                symbol = f'sh{stock_code}'
            else:
                symbol = f'sz{stock_code}'
            
            # Get real-time quote
            df = ak.stock_zh_a_spot_em()
            stock_data = df[df['代码'] == stock_code]
            
            if not stock_data.empty:
                row = stock_data.iloc[0]
                return {
                    'source': 'akshare',
                    'code': stock_code,
                    'name': row.get('名称', ''),
                    'price': float(row.get('最新价', 0)),
                    'change_pct': float(row.get('涨跌幅', 0)),
                    'volume': float(row.get('成交量', 0)),
                    'timestamp': datetime.now().isoformat()
                }
        except Exception as e:
            logger.error(f"AKShare fetch error for {stock_code}: {str(e)}")
        
        return None
    
    def fetch_from_yahoo(self, stock_code: str) -> Optional[Dict[str, Any]]:
        """Fetch real-time data from Yahoo Finance"""
        if 'yahoo' not in self.available_sources:
            return None
        
        try:
            yf = self.available_sources['yahoo']
            
            # Convert to Yahoo symbol format
            if stock_code.startswith('6'):
                yahoo_symbol = f'{stock_code}.SS'  # Shanghai
            else:
                yahoo_symbol = f'{stock_code}.SZ'  # Shenzhen
            
            ticker = yf.Ticker(yahoo_symbol)
            info = ticker.info
            
            if info and 'currentPrice' in info:
                return {
                    'source': 'yahoo',
                    'code': stock_code,
                    'name': info.get('longName', ''),
                    'price': float(info.get('currentPrice', 0)),
                    'change_pct': float(info.get('regularMarketChangePercent', 0)),
                    'volume': float(info.get('volume', 0)),
                    'timestamp': datetime.now().isoformat()
                }
        except Exception as e:
            logger.error(f"Yahoo Finance fetch error for {stock_code}: {str(e)}")
        
        return None
    
    def fetch_from_eastmoney(self, stock_code: str) -> Optional[Dict[str, Any]]:
        """Fetch real-time data from EastMoney"""
        if 'eastmoney' not in self.available_sources:
            return None
        
        try:
            requests = self.available_sources['eastmoney']
            
            # EastMoney API endpoint
            market_code = '1' if stock_code.startswith('6') else '0'
            secid = f"{market_code}.{stock_code}"
            
            url = f"http://push2.eastmoney.com/api/qt/stock/get"
            params = {
                'secid': secid,
                'fields': 'f43,f44,f45,f46,f47,f48,f49,f50,f51,f52,f57,f58'
            }
            
            response = requests.get(url, params=params, timeout=5)
            
            if response.status_code == 200:
                data = response.json()
                if data.get('data'):
                    stock_info = data['data']
                    return {
                        'source': 'eastmoney',
                        'code': stock_code,
                        'name': stock_info.get('f58', ''),
                        'price': float(stock_info.get('f43', 0)) / 100,  # Price in fen
                        'change_pct': float(stock_info.get('f169', 0)) / 100,  # Using f169 for change percentage
                        'volume': float(stock_info.get('f47', 0)),
                        'timestamp': datetime.now().isoformat()
                    }
        except Exception as e:
            logger.error(f"EastMoney fetch error for {stock_code}: {str(e)}")
        
        return None
    
    def fetch_from_all_sources(self, stock_code: str) -> Dict[str, Any]:
        """Fetch data from all available sources"""
        results = {}
        
        if 'akshare' in self.available_sources:
            results['akshare'] = self.fetch_from_akshare(stock_code)
        
        if 'yahoo' in self.available_sources:
            results['yahoo'] = self.fetch_from_yahoo(stock_code)
        
        if 'eastmoney' in self.available_sources:
            results['eastmoney'] = self.fetch_from_eastmoney(stock_code)
        
        return {k: v for k, v in results.items() if v is not None}
    
    def compare_sources(self, stock_codes: List[str]) -> pd.DataFrame:
        """
        Compare data reliability across multiple sources for given stock codes
        
        Args:
            stock_codes: List of stock codes to compare
            
        Returns:
            DataFrame with comparison results
        """
        comparison_data = []
        
        for stock_code in stock_codes:
            logger.info(f"Comparing sources for {stock_code}")
            
            # Fetch from all sources
            results = self.fetch_from_all_sources(stock_code)
            
            if len(results) < 2:
                logger.warning(f"Not enough sources available for {stock_code}")
                continue
            
            # Extract prices
            prices = {source: data['price'] for source, data in results.items()}
            
            # Calculate statistics
            avg_price = sum(prices.values()) / len(prices)
            max_diff = max(abs(p - avg_price) for p in prices.values())
            max_diff_pct = (max_diff / avg_price * 100) if avg_price > 0 else 0
            
            comparison_data.append({
                'stock_code': stock_code,
                'sources_available': len(results),
                'avg_price': round(avg_price, 2),
                'max_diff': round(max_diff, 4),
                'max_diff_pct': round(max_diff_pct, 2),
                **{f'{source}_price': data['price'] for source, data in results.items()}
            })
        
        df = pd.DataFrame(comparison_data)
        return df
    
    def get_best_source(self, stock_code: str) -> Optional[Dict[str, Any]]:
        """
        Get data from the most reliable source with fallback
        Priority: akshare > eastmoney > yahoo
        """
        # Try sources in order of reliability
        for source_name in ['akshare', 'eastmoney', 'yahoo']:
            if source_name in self.available_sources:
                method = getattr(self, f'fetch_from_{source_name}')
                data = method(stock_code)
                if data:
                    logger.info(f"Successfully fetched from {source_name} for {stock_code}")
                    return data
        
        logger.error(f"Failed to fetch from any source for {stock_code}")
        return None
    
    def fetch_historical_data(self, stock_code: str, start_date: str, end_date: str) -> pd.DataFrame:
        """
        Fetch historical data with fallback mechanism
        
        Args:
            stock_code: Stock code
            start_date: Start date (YYYYMMDD or YYYY-MM-DD)
            end_date: End date (YYYYMMDD or YYYY-MM-DD)
            
        Returns:
            DataFrame with historical data
        """
        # Try AKShare first (most reliable for Chinese stocks)
        if 'akshare' in self.available_sources:
            try:
                ak = self.available_sources['akshare']
                
                if stock_code.startswith('6'):
                    symbol = f'sh{stock_code}'
                else:
                    symbol = f'sz{stock_code}'
                
                # Format dates
                start_date_fmt = start_date.replace('-', '')
                end_date_fmt = end_date.replace('-', '')
                
                df = ak.stock_zh_a_hist(
                    symbol=symbol,
                    period="daily",
                    start_date=start_date_fmt,
                    end_date=end_date_fmt,
                    adjust="qfq"
                )
                
                if df is not None and not df.empty:
                    logger.info(f"Fetched {len(df)} historical records from AKShare for {stock_code}")
                    return df
            except Exception as e:
                logger.error(f"AKShare historical fetch error: {str(e)}")
        
        # Fallback to Yahoo Finance
        if 'yahoo' in self.available_sources:
            try:
                yf = self.available_sources['yahoo']
                
                if stock_code.startswith('6'):
                    yahoo_symbol = f'{stock_code}.SS'
                else:
                    yahoo_symbol = f'{stock_code}.SZ'
                
                ticker = yf.Ticker(yahoo_symbol)
                df = ticker.history(start=start_date, end=end_date)
                
                if not df.empty:
                    logger.info(f"Fetched {len(df)} historical records from Yahoo Finance for {stock_code}")
                    return df
            except Exception as e:
                logger.error(f"Yahoo Finance historical fetch error: {str(e)}")
        
        logger.error(f"Failed to fetch historical data for {stock_code}")
        return pd.DataFrame()


def test_data_sources(num_stocks: int = 20):
    """
    Test and compare data sources for reliability
    
    Args:
        num_stocks: Number of random stocks to test (default: 20)
    """
    logger.info(f"=== Testing Data Source Reliability ({num_stocks} stocks) ===\n")
    
    # Sample stock codes from different sectors
    test_stocks = [
        '000001',  # 平安银行
        '000002',  # 万科A
        '000066',  # 中国长城
        '000333',  # 美的集团
        '000858',  # 五粮液
        '600000',  # 浦发银行
        '600036',  # 招商银行
        '600519',  # 贵州茅台
        '600887',  # 伊利股份
        '601318',  # 中国平安
        '601398',  # 工商银行
        '601857',  # 中国石油
        '601988',  # 中国银行
        '300750',  # 宁德时代
        '002594',  # 比亚迪
        '002415',  # 海康威视
        '300059',  # 东方财富
        '002230',  # 科大讯飞
        '000725',  # 京东方A
        '601888',  # 中国中免
    ][:num_stocks]
    
    fetcher = MultiSourceDataFetcher()
    
    # Compare sources
    comparison_df = fetcher.compare_sources(test_stocks)
    
    if not comparison_df.empty:
        logger.info("\n=== Comparison Results ===")
        logger.info(f"\n{comparison_df.to_string()}")
        
        # Calculate source reliability
        logger.info("\n=== Source Reliability Summary ===")
        logger.info(f"Average max difference: {comparison_df['max_diff_pct'].mean():.2f}%")
        logger.info(f"Stocks with < 1% difference: {len(comparison_df[comparison_df['max_diff_pct'] < 1])}/{len(comparison_df)}")
        logger.info(f"Stocks with < 0.1% difference: {len(comparison_df[comparison_df['max_diff_pct'] < 0.1])}/{len(comparison_df)}")
        
        # Recommendation
        logger.info("\n=== Recommendation ===")
        avg_diff = comparison_df['max_diff_pct'].mean()
        if avg_diff < 0.5:
            logger.info("✓ All sources are highly reliable (< 0.5% difference)")
        elif avg_diff < 1.0:
            logger.info("✓ Sources are reliable (< 1% difference)")
        else:
            logger.info("⚠ Sources show some variation (> 1% difference)")
        
        logger.info("\nRecommended primary source: AKShare (most comprehensive for Chinese stocks)")
        logger.info("Recommended fallback: EastMoney API")
        
        return comparison_df
    else:
        logger.error("No comparison data available")
        return None


if __name__ == "__main__":
    # Run the test
    test_data_sources(20)
