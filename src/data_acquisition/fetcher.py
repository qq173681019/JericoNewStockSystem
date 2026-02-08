"""
SIAPS - Data Acquisition Module
Fetches stock data from various sources
"""
import pandas as pd
from typing import Optional, Dict, Any
from datetime import datetime, timedelta
import sys
from pathlib import Path

# Add project root to Python path
ROOT_DIR = Path(__file__).parent.parent.parent.parent
sys.path.insert(0, str(ROOT_DIR))

from src.utils import setup_logger

logger = setup_logger(__name__)


class DataFetcher:
    """Base class for data fetchers"""
    
    def __init__(self):
        self.cache_enabled = True
    
    def fetch_daily_data(self, stock_code: str, start_date: str, end_date: str) -> pd.DataFrame:
        """
        Fetch daily stock data
        
        Args:
            stock_code: Stock code (e.g., '000001')
            start_date: Start date in format 'YYYY-MM-DD'
            end_date: End date in format 'YYYY-MM-DD'
        
        Returns:
            pd.DataFrame: Daily stock data
        """
        raise NotImplementedError
    
    def fetch_realtime_data(self, stock_code: str) -> Dict[str, Any]:
        """
        Fetch real-time stock data
        
        Args:
            stock_code: Stock code
        
        Returns:
            dict: Real-time stock data
        """
        raise NotImplementedError


class AKShareFetcher(DataFetcher):
    """AKShare data fetcher implementation"""
    
    def __init__(self):
        super().__init__()
        try:
            import akshare as ak
            self.ak = ak
            logger.info("AKShare initialized successfully")
        except ImportError:
            logger.error("AKShare not installed. Please install: pip install akshare")
            self.ak = None
    
    def fetch_daily_data(self, stock_code: str, start_date: str, end_date: str) -> pd.DataFrame:
        """
        Fetch daily stock data from AKShare
        
        Args:
            stock_code: Stock code (e.g., '000001')
            start_date: Start date in format 'YYYYMMDD'
            end_date: End date in format 'YYYYMMDD'
        
        Returns:
            pd.DataFrame: Daily stock data with columns [date, open, high, low, close, volume]
        """
        if self.ak is None:
            logger.error("AKShare not available")
            return pd.DataFrame()
        
        try:
            # Determine market (sh: Shanghai, sz: Shenzhen)
            if stock_code.startswith('6'):
                symbol = f'sh{stock_code}'
            else:
                symbol = f'sz{stock_code}'
            
            logger.info(f"Fetching daily data for {symbol} from {start_date} to {end_date}")
            
            # Fetch historical data
            df = self.ak.stock_zh_a_hist(
                symbol=symbol,
                period="daily",
                start_date=start_date,
                end_date=end_date,
                adjust="qfq"  # Forward adjusted
            )
            
            if df is not None and not df.empty:
                logger.info(f"Successfully fetched {len(df)} records for {stock_code}")
                return df
            else:
                logger.warning(f"No data found for {stock_code}")
                return pd.DataFrame()
        
        except Exception as e:
            logger.error(f"Error fetching data for {stock_code}: {str(e)}")
            return pd.DataFrame()
    
    def fetch_realtime_data(self, stock_code: str) -> Dict[str, Any]:
        """
        Fetch real-time stock data from AKShare
        
        Args:
            stock_code: Stock code
        
        Returns:
            dict: Real-time stock data
        """
        if self.ak is None:
            logger.error("AKShare not available")
            return {}
        
        try:
            # Fetch real-time quotes
            df = self.ak.stock_zh_a_spot_em()
            
            # Find the stock
            stock_data = df[df['代码'] == stock_code]
            
            if not stock_data.empty:
                result = stock_data.iloc[0].to_dict()
                logger.info(f"Successfully fetched real-time data for {stock_code}")
                return result
            else:
                logger.warning(f"No real-time data found for {stock_code}")
                return {}
        
        except Exception as e:
            logger.error(f"Error fetching real-time data for {stock_code}: {str(e)}")
            return {}


def get_data_fetcher(source: str = "akshare") -> Optional[DataFetcher]:
    """
    Get data fetcher instance based on source
    
    Args:
        source: Data source name ('akshare', 'tushare', etc.)
    
    Returns:
        DataFetcher: Data fetcher instance
    """
    if source.lower() == "akshare":
        return AKShareFetcher()
    else:
        logger.error(f"Unsupported data source: {source}")
        return None


def get_multi_source_fetcher():
    """
    Get multi-source data fetcher with automatic fallback
    
    Returns:
        MultiSourceDataFetcher: Multi-source fetcher instance
    """
    try:
        from src.data_acquisition.multi_source_fetcher import MultiSourceDataFetcher
        return MultiSourceDataFetcher()
    except ImportError as e:
        logger.error(f"Failed to import MultiSourceDataFetcher: {str(e)}")
        return None
