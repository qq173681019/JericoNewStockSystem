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
            'eastmoney': self._init_eastmoney(),
            'sina': self._init_sina()
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
        except (ImportError, TypeError) as e:
            logger.warning(f"✗ Yahoo Finance not available: {str(e)}")
            return None
    
    def _init_eastmoney(self):
        """Initialize EastMoney (via requests with no proxy)"""
        try:
            import requests
            # Create a session that ignores proxies
            session = requests.Session()
            session.trust_env = False  # Don't use environment proxy settings
            session.proxies = {'http': None, 'https': None}
            logger.info("✓ EastMoney initialized")
            return session
        except ImportError:
            logger.warning("✗ EastMoney not available")
            return None
    
    def _init_sina(self):
        """Initialize Sina Finance (via requests)"""
        try:
            import requests
            # Create a session for Sina
            session = requests.Session()
            session.headers.update({
                'Referer': 'https://finance.sina.com.cn',
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            })
            logger.info("✓ Sina Finance initialized")
            return session
        except ImportError:
            logger.warning("✗ Sina Finance not available")
            return None
    
    def fetch_from_sina(self, stock_code: str) -> Optional[Dict[str, Any]]:
        """Fetch real-time data from Sina Finance API"""
        if 'sina' not in self.available_sources:
            return None
        
        try:
            session = self.available_sources['sina']
            
            # Determine market prefix: sh for Shanghai, sz for Shenzhen
            if stock_code.startswith('6'):
                symbol = f'sh{stock_code}'
            else:
                symbol = f'sz{stock_code}'
            
            url = f'https://hq.sinajs.cn/list={symbol}'
            response = session.get(url, timeout=10)
            
            if response.status_code == 200:
                text = response.text
                # Parse: var hq_str_sh601606="长城军工,45.510,45.360,45.710,..."
                if '="' in text and text.strip().endswith('";'):
                    data_str = text.split('="')[1].rstrip('";')
                    parts = data_str.split(',')
                    
                    if len(parts) >= 32:
                        name = parts[0]
                        open_price = float(parts[1]) if parts[1] else 0
                        yesterday_close = float(parts[2]) if parts[2] else 0
                        current_price = float(parts[3]) if parts[3] else 0
                        high = float(parts[4]) if parts[4] else 0
                        low = float(parts[5]) if parts[5] else 0
                        volume = float(parts[8]) if parts[8] else 0
                        
                        # Calculate change percentage
                        change_pct = 0
                        if yesterday_close > 0:
                            change_pct = round((current_price - yesterday_close) / yesterday_close * 100, 2)
                        
                        return {
                            'source': 'sina',
                            'code': stock_code,
                            'name': name,
                            'price': current_price,
                            'change_pct': change_pct,
                            'volume': volume,
                            'high': high,
                            'low': low,
                            'open': open_price,
                            'yesterday_close': yesterday_close,
                            'timestamp': datetime.now().isoformat()
                        }
        except Exception as e:
            logger.error(f"Sina fetch error for {stock_code}: {str(e)}")
        
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
            requests_lib = self.available_sources['eastmoney']
            
            # Determine market code: 1=Shanghai, 0=Shenzhen
            if stock_code.startswith('6'):
                market_code = '1'
            elif stock_code.startswith(('0', '3')):
                market_code = '0'
            else:
                market_code = '0'
            
            secid = f"{market_code}.{stock_code}"
            
            # Use the stock quote API
            url = "http://push2.eastmoney.com/api/qt/stock/get"
            params = {
                'secid': secid,
                'ut': 'bd1d9ddb04089700cf9c27f6f7426281',
                'fields': 'f43,f44,f45,f46,f47,f48,f49,f50,f51,f52,f57,f58,f59,f60,f169,f170,f171'
            }
            
            response = requests_lib.get(url, params=params, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                if data.get('data'):
                    stock_info = data['data']
                    # f43=current price (in fen), f58=name, f170=change percent
                    price_raw = stock_info.get('f43', 0)
                    change_raw = stock_info.get('f170', 0)
                    
                    # Handle the price (stored in fen, need to convert to yuan)
                    if price_raw and price_raw != '-':
                        price = float(price_raw) / 100
                    else:
                        price = 0
                    
                    # Change percent
                    if change_raw and change_raw != '-':
                        change_pct = float(change_raw) / 100
                    else:
                        change_pct = 0
                    
                    return {
                        'source': 'eastmoney',
                        'code': stock_code,
                        'name': stock_info.get('f58', ''),
                        'price': price,
                        'change_pct': change_pct,
                        'volume': float(stock_info.get('f47', 0) or 0),
                        'high': float(stock_info.get('f44', 0) or 0) / 100,
                        'low': float(stock_info.get('f45', 0) or 0) / 100,
                        'open': float(stock_info.get('f46', 0) or 0) / 100,
                        'timestamp': datetime.now().isoformat()
                    }
        except Exception as e:
            logger.error(f"EastMoney fetch error for {stock_code}: {str(e)}")
        
        return None
    
    def fetch_stock_realtime(self, stock_code: str) -> Optional[Dict[str, Any]]:
        """
        Fetch real-time stock data using multiple sources with fallback
        This is the preferred method for getting single stock data
        """
        # Try Sina first (most reliable, no proxy issues)
        result = self.fetch_from_sina(stock_code)
        if result and result.get('price', 0) > 0:
            return result
        
        # Fallback to EastMoney
        result = self.fetch_from_eastmoney(stock_code)
        if result and result.get('price', 0) > 0:
            return result
        
        # Fallback to AKShare
        result = self.fetch_from_akshare(stock_code)
        if result and result.get('price', 0) > 0:
            return result
        
        # Fallback to Yahoo Finance (for international)
        result = self.fetch_from_yahoo(stock_code)
        if result and result.get('price', 0) > 0:
            return result
        
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
    
    def fetch_sector_data(self, limit: int = 6) -> List[Dict[str, Any]]:
        """
        Fetch real-time sector data from TongHuaShun (同花顺) via AKShare
        Falls back to EastMoney if TongHuaShun is unavailable
        
        Args:
            limit: Number of top sectors to return
            
        Returns:
            List of sector dictionaries sorted by change percentage
        """
        # Try TongHuaShun first (more accurate real-time data)
        result = self._fetch_sector_from_ths(limit)
        if result:
            # Ensure AI-related sectors are included
            result = self._ensure_ai_sectors(result, limit)
            return result
            
        # Fallback to EastMoney
        logger.warning("TongHuaShun data unavailable, falling back to EastMoney")
        result = self._fetch_sector_from_eastmoney(limit)
        if result:
            result = self._ensure_ai_sectors(result, limit)
        return result
    
    def _fetch_sector_from_ths(self, limit: int) -> List[Dict[str, Any]]:
        """Fetch sector data from TongHuaShun via AKShare with retry"""
        if 'akshare' not in self.available_sources:
            return []
        
        import time
        max_retries = 3
        
        for attempt in range(max_retries):
            try:
                ak = self.available_sources['akshare']
                # Use stock_board_industry_summary_ths for real-time data
                df = ak.stock_board_industry_summary_ths()
                
                if df is None or df.empty:
                    if attempt < max_retries - 1:
                        time.sleep(0.5)
                        continue
                    return []
                
                result = []
                for idx, row in df.head(limit).iterrows():
                    try:
                        # Get change percentage
                        change = float(row.get('涨跌幅', 0))
                        
                        # Calculate heat (0-100)
                        heat = min(100, max(0, 50 + change * 5))
                        
                        # Get stock counts
                        rising = int(row.get('上涨家数', 0) or 0)
                        falling = int(row.get('下跌家数', 0) or 0)
                        
                        # Get leading stock
                        leading_stock = row.get('领涨股', '')
                        
                        result.append({
                            'name': row.get('板块', '未知板块'),
                            'heat': int(heat),
                            'stocks': rising + falling,
                            'change': round(change, 2),
                            'topCompanies': [leading_stock] if leading_stock else [],
                            'code': '',  # THS doesn't return code in summary
                            'source': 'tonghuashun'
                        })
                    except (ValueError, TypeError) as e:
                        continue
                
                if result:
                    logger.info(f"✓ Fetched {len(result)} industry sectors from TongHuaShun")
                    return result
                    
            except Exception as e:
                if attempt < max_retries - 1:
                    time.sleep(0.5)
                    continue
                logger.warning(f"TongHuaShun sector fetch failed after {max_retries} attempts: {str(e)}")
            return []
    
    def _fetch_sector_from_eastmoney(self, limit: int) -> List[Dict[str, Any]]:
        """Fetch sector data from EastMoney API (fallback)"""
        try:
            url = "http://push2.eastmoney.com/api/qt/clist/get"
            params = {
                'pn': 1,
                'pz': limit,
                'po': 1,  # Descending sort (highest change first)
                'np': 1,
                'ut': 'bd1d9ddb04089700cf9c27f6f7426281',
                'fltt': 2,
                'invt': 2,
                'fid': 'f3',  # Sort by f3 (Change Percent)
                'fs': 'm:90 t:2',  # Market 90, Type 2 (Industry Board)
                'fields': 'f12,f13,f14,f2,f3,f4,f104,f105,f128,f140,f136'
            }
            
            if 'eastmoney' in self.available_sources:
                requests_lib = self.available_sources['eastmoney']
            else:
                import requests
                requests_lib = requests
                
            response = requests_lib.get(url, params=params, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                if data and data.get('data') and data['data'].get('diff'):
                    result = []
                    for item in data['data']['diff']:
                        change = float(item.get('f3', 0))
                        heat = min(100, max(0, 50 + change * 5))
                        rising = int(item.get('f104', 0) or 0)
                        falling = int(item.get('f105', 0) or 0)
                        
                        result.append({
                            'name': item.get('f14', '未知板块'),
                            'heat': int(heat),
                            'stocks': rising + falling,
                            'change': round(change, 2),
                            'topCompanies': [item.get('f128', '')] if item.get('f128') else [],
                            'code': item.get('f12', ''),
                            'source': 'eastmoney'
                        })
                    
                    logger.info(f"✓ Fetched {len(result)} industry sectors from EastMoney")
                    return result
                    
        except Exception as e:
            logger.error(f"EastMoney sector fetch error: {str(e)}")
            
        return []
    
    def _ensure_ai_sectors(self, sectors: List[Dict[str, Any]], limit: int) -> List[Dict[str, Any]]:
        """
        Ensure AI-related sectors are included in the sector list
        If AI sectors are missing from top performers, add them with fetched or estimated data
        
        Args:
            sectors: List of sector dictionaries
            limit: Target number of sectors
            
        Returns:
            Updated list with AI sectors included (AI sectors prioritized to appear near top)
        """
        # Define important AI-related sector keywords
        ai_keywords = ['AI', '人工智能', 'AI应用', '机器人', 'ChatGPT', 'AIGC', '算力']
        
        # Check if any AI sectors are already present
        sector_names = [s['name'] for s in sectors]
        has_ai_sector = any(
            any(keyword in name for keyword in ai_keywords) 
            for name in sector_names
        )
        
        # If AI sectors are present or we've reached limit, return as is
        if has_ai_sector:
            logger.info("AI-related sectors already present in sector list")
            return sectors[:limit]
        
        # Try to fetch AI sector data from the full dataset
        # Allow up to 2 AI sectors to be added without overwhelming the list
        max_ai_sectors = min(2, max(1, limit // 3))  # Dynamic limit: 1-2 sectors based on total limit
        ai_sectors = self._fetch_ai_sectors_from_full_data(max_count=max_ai_sectors)
        
        if ai_sectors:
            # Insert AI sectors after the top 2 performers to ensure visibility
            # while still respecting top performing sectors
            if len(sectors) >= 2:
                # Insert after position 2
                combined = sectors[:2] + ai_sectors + sectors[2:]
            else:
                # Add to the end if we have fewer than 2 sectors
                combined = sectors + ai_sectors
            
            logger.info(f"Added {len(ai_sectors)} AI-related sectors to the list")
            return combined[:limit]
        
        return sectors[:limit]
    
    def _fetch_ai_sectors_from_full_data(self, max_count: int = 2) -> List[Dict[str, Any]]:
        """
        Fetch AI-related sectors from the full dataset
        
        Args:
            max_count: Maximum number of AI sectors to return (default: 2)
            
        Returns:
            List of AI-related sectors (up to max_count)
        """
        if 'akshare' not in self.available_sources:
            return []
        
        try:
            ak = self.available_sources['akshare']
            # Fetch full sector data (not limited)
            df = ak.stock_board_industry_summary_ths()
            
            if df is None or df.empty:
                return []
            
            ai_keywords = ['AI', '人工智能', 'AI应用', '机器人', 'ChatGPT', 'AIGC', '算力']
            ai_sectors = []
            
            for idx, row in df.iterrows():
                sector_name = row.get('板块', '')
                # Check if this sector contains AI-related keywords
                if any(keyword in sector_name for keyword in ai_keywords):
                    try:
                        change = float(row.get('涨跌幅', 0))
                        # Calculate heat score (0-100 scale)
                        # Formula: base 50 (neutral) + (change% * 5) to amplify small movements
                        # E.g., +2% change → 60 heat, -2% change → 40 heat
                        # Clamped to [0, 100] range for consistency
                        heat = min(100, max(0, 50 + change * 5))
                        rising = int(row.get('上涨家数', 0) or 0)
                        falling = int(row.get('下跌家数', 0) or 0)
                        leading_stock = row.get('领涨股', '')
                        
                        ai_sectors.append({
                            'name': sector_name,
                            'heat': int(heat),
                            'stocks': rising + falling,
                            'change': round(change, 2),
                            'topCompanies': [leading_stock] if leading_stock else [],
                            'code': '',
                            'source': 'tonghuashun'
                        })
                        
                        # Limit to max_count AI sectors
                        if len(ai_sectors) >= max_count:
                            break
                    except (ValueError, TypeError):
                        continue
            
            if ai_sectors:
                logger.info(f"✓ Found {len(ai_sectors)} AI-related sectors in full dataset")
            
            return ai_sectors
            
        except Exception as e:
            logger.warning(f"Failed to fetch AI sectors from full data: {str(e)}")
            return []

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
