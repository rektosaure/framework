# src/downloaders/__init__.py

from .fred_downloader import FredDownloader
from .yfinance_downloader import YFinanceDownloader
from .sec_downloader import SecDownloader
from .investing_downloader import InvestingDownloader
from .ycharts_downloader import YChartsDownloader
from .cftc_downloader import CftcDownloader
from .empty_downloader import EmptyDownloader

__all__ = [
    'FredDownloader',
    'YFinanceDownloader',
    'SecDownloader',
    'InvestingDownloader',
    'YChartsDownloader',
    'CftcDownloader',
    'EmptyDownloader'
]