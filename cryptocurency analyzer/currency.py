"""
 Provides class for working with the statistics
 in cryptocurency market
"""

import asyncio
import itertools
import numpy as np
from coins import DataCollector
from tokencolector import TokenColector
import url


class CurrencyStatistics:
    """
     Provides statistical methods for currency exchange markets
    """
    def __init__(self, token_name: str, file_name: str, base_coin: str,
                 second_coin: str) -> None:

        self.api = TokenColector(token_name=token_name,
                                 file_name=file_name)
        self.token = self.api.get_api_key()

        # f.e BTC
        self.base_coin = base_coin
        kwargs_base_coin = {
            "function_name": "DIGITAL_CURRENCY_DAILY",
            "symbol": self.base_coin,
            "market": "USD",
            "api_token": self.token
        }
        # f.e ETH
        self.second_coin = second_coin
        kwargs_second_coin = {
            "function_name": "DIGITAL_CURRENCY_DAILY",
            "symbol": self.second_coin,
            "market": "USD",
            "api_token": self.token
        }

        self.base_coin = DataCollector()
        self.second_coin = DataCollector()
        self.url_instance = url.GetURLRequest()
        self.curr_url_instance = self.url_instance
        self.url_instance.set_strategy(url.DailyExchange())
        self._base_coin_url = self.__url_getter(self.url_instance,
                                                **kwargs_base_coin)
        self._second_coin_url = self.__url_getter(self.url_instance,
                                                  **kwargs_second_coin)

    @classmethod
    def __url_getter(cls, url_instance, **kwargs):
        url_adress = url_instance.form_url(**kwargs)
        return url_adress

    @staticmethod
    def __dict_collection(coin_data: dict, period_keys: list) -> dict:
        period_data_coin = {}
        for key in period_keys:
            period_data_coin[key] = coin_data[key]
        return period_data_coin

    @staticmethod
    def __single_day_keys(period_data_coin: dict,
                          last_period_keys: list) -> list:

        period_coin_keys: list = list(itertools.islice(period_data_coin[last_period_keys[0]].keys(), 0, 8, 2))
        return period_coin_keys

    @staticmethod
    def __wraper_price(week_data_coin, last_week_keys, week_coin_keys):
        daily_coin_data = np.array([])
        for day in last_week_keys:
            for coin in week_coin_keys:
                daily_coin_data = np.append(daily_coin_data,
                                            [week_data_coin[day][coin]])

        return daily_coin_data

    @staticmethod
    def roc_method(curr_price: float, prev_price: float) -> float:
        """
        roc_method Calculate the percentage of price action

        ((curr_price/prev_price)-1) * 100

        Args:
            curr_price (float): current price on the market
            prev_price (float): last price on the market

        Returns:
            float: percentage of price action
        """
        percente_action = ((curr_price / prev_price) - 1) * 100
        return percente_action

    @staticmethod
    def decoupling(coin_price_action: float | int,
                   pirson_corr: float) -> float:
        """
        decoupling is a process of finding self driven price action

        Static method.

        Args:
            coin_price_action (float | int): coin price action in percent
            pirson_corr (float): Pearson correlation coefficient

        Returns:
            float: decoupled coin price action in percent
        """        """"""
        decoupled_price = (coin_price_action -
                           (coin_price_action * pirson_corr))
        return decoupled_price

    @staticmethod
    def pirson_coef(base_coin_prices: np.ndarray,
                    second_coin_prices: np.ndarray) -> float:
        """
        pirson_coef implementation of Pearson coefficient

        Calculates Pearson correlation using return rate
        between two types of crypto-currencies namely base_coin_prices
        and second_coin_prices.

        Static method.

        Args:
            base_coin_prices (np.ndarray): array of historical data
            second_coin_prices (np.ndarray): array of historical data

        Returns:
            float: Pearson`s correlation coefficient from -1 to 1.
        """
        my_rho = np.corrcoef(base_coin_prices, second_coin_prices, dtype=float)
        pirson_corr = my_rho[0][1]
        return pirson_corr

    def historic_data(self, days: int) -> np.ndarray:
        """
        historic_data Collects historic data from the AlphaVantage API

        Args:
            days (int): Number of the days to retrieve historical data

        Returns:
            np.ndarray: Two array that contain historical data of
            prices for the past periods
        """        """"""
        base_coin_weakly_data = asyncio.run(self.base_coin.get_coin_price(self._base_coin_url))
        second_coin_weakly_data = asyncio.run(self.second_coin.get_coin_price(self._second_coin_url))

        if "output" not in base_coin_weakly_data.keys() or "output" not in second_coin_weakly_data.keys():
            return None

        base_coin_stats = base_coin_weakly_data.get("output")
        second_coin_stats = second_coin_weakly_data.get("output")

        if "Time Series (Digital Currency Daily)" not in base_coin_stats.keys() or "Time Series (Digital Currency Daily)" not in second_coin_stats.keys():
            return None

        base_coin_data: dict = base_coin_stats["Time Series (Digital Currency Daily)"]
        second_coin_data: dict = second_coin_stats["Time Series (Digital Currency Daily)"]
        base_coin_period_keys: list = list(itertools.islice(base_coin_data.keys(), days))
        second_coin_period_keys: list = list(itertools.islice
                                             (second_coin_data.keys(), days))

        base_coin_data_from_period = self.__dict_collection(base_coin_data,
                                                            base_coin_period_keys)

        second_coin_data_from_period = self.__dict_collection(second_coin_data,
                                                              second_coin_period_keys)

        base_coin_keys = self.__single_day_keys(base_coin_data_from_period,
                                                base_coin_period_keys)

        second_coin_keys = self.__single_day_keys(second_coin_data_from_period,
                                                  second_coin_period_keys)

        daily_base_coin_data = self.__wraper_price(base_coin_data_from_period,
                                                   base_coin_period_keys,
                                                   base_coin_keys)

        daily_second_coin_data = self.__wraper_price(second_coin_data_from_period,
                                                     second_coin_period_keys,
                                                     second_coin_keys)

        return daily_base_coin_data, daily_second_coin_data

    def __current_price_metadata(self, coin: str) -> dict:
        """
        __current_price_metadata method for recieving json data from
        AlphaVantage API.

        Private method.

        Args:
            coin (str): coin name acronym f.e ETH or USD

        Returns:
            dict: Metadata dictionary
        """
        kwargs = {
            "function_name": "CURRENCY_EXCHANGE_RATE",
            "base_coin": coin,
            "secondary_coin": "USD",
            "api_token": self.token
        }
        current_price_coin = DataCollector()
        self.curr_url_instance.set_strategy(url.CurrentExchange())
        curr_url = self.__url_getter(self.curr_url_instance, **kwargs)
        curr_price = asyncio.run(current_price_coin.get_coin_price(curr_url))

        if "output" not in curr_price.keys():
            return None

        curr_price: dict = curr_price["output"]
        meta_data: dict = curr_price.get("Realtime Currency Exchange Rate")
        return meta_data

    def current_price(self, coin: str) -> float:
        """
        current_price _summary_

        _extended_summary_

        Args:
            coin (str): coin acronym f.e ETH

        Returns:
            float: current_price on the market
        """
        meta_data = self.__current_price_metadata(coin)
        if meta_data is None:
            return None

        price = meta_data["5. Exchange Rate"]
        return float(price)
