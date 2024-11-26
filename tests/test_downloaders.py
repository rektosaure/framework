# tests/test_downloaders.py

import unittest
from unittest.mock import patch
from src.downloaders.fred_downloader import FredDownloader
from src.downloaders.yfinance_downloader import YFinanceDownloader

class TestDownloaders(unittest.TestCase):
    def test_fred_downloader_success(self):
        downloader = FredDownloader()
        with patch('pandas_datareader.data.DataReader') as mock_datareader:
            mock_data = pd.DataFrame({
                'DATE': pd.date_range(start='2020-01-01', periods=5, freq='D'),
                'DGS10': [1.5, 1.6, 1.7, 1.8, 1.9]
            })
            mock_datareader.return_value = mock_data
            df = downloader.download('10Y', 'DGS10')
            self.assertFalse(df.empty)
            self.assertIn('Date', df.columns)
            self.assertIn('10Y', df.columns)

    def test_yfinance_downloader_success(self):
        downloader = YFinanceDownloader()
        with patch('yfinance.download') as mock_yfinance_download:
            mock_data = pd.DataFrame({
                'Date': pd.date_range(start='2020-01-01', periods=5, freq='D'),
                'Close': [100, 101, 102, 103, 104]
            }).set_index('Date')
            mock_yfinance_download.return_value = mock_data
            df = downloader.download('TLT', 'TLT')
            self.assertFalse(df.empty)
            self.assertIn('Date', df.columns)
            self.assertIn('TLT', df.columns)

if __name__ == '__main__':
    unittest.main()