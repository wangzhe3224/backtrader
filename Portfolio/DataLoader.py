# Import the backtrader platform
import backtrader as bt


class DataLoader:
    """"""
    @staticmethod
    def load_last_prices(filepath: str):
        """ file contains only last prices
        date, s1, s2, s3, ...,
        2000-01-01, 100, 200, 300

        Given n columns, function return n DataFeed
        """
