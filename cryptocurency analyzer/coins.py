import asyncio
import requests
from tokencolector import TokenColector


class DataCollector():
    """
    DataCollector collects the data from exchange API

    Actual prices of crypto coins
    """    """"""

    def __init__(self, coin, api) -> None:
        """Constructor of the DataCollector object
        Args: coin - is the actual coin name"""

        self.coin = coin
        self.api = api

    
    def get_coin_price(self):
        ...

api_key = TokenColector(token_name="VANTAGE", file_name="./API.env")