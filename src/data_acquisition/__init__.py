"""
SIAPS Data Acquisition Package
"""
from .fetcher import DataFetcher, AKShareFetcher, get_data_fetcher

__all__ = ['DataFetcher', 'AKShareFetcher', 'get_data_fetcher']
