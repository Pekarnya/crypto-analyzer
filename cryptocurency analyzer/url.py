"""
 Module designed to quickly create url for current API
"""

from abc import ABC, abstractmethod


URLS_API = {
    "api_vantage": "https://www.alphavantage.co/query?"
}


class URLGeter(ABC):
    """
    URLGeter Child of abstract helper class

    Parent of different classes that are used to form
    url according to the https://www.alphavantage.co/documentation/

    Args:
        ABC (Class): Helper for creating inheritance hierarchy
    """
    @abstractmethod
    def get_url(self, **kwargs: dict) -> str:
        """
        get_url Base method for forming the URL string

        Works and parameters are depends on the context

        Args:
            kwargs (dict): dictionary with aditional
            parametres of API.
            See the documentation:
            https://www.alphavantage.co/documentation/

        Returns:
            str: _description_
        """        """"""
        ...


class CurrentExchange(URLGeter):
    """
    CurrentExchange

    _extended_summary_

    Args:
        UrlGeter (ABC): Base class for various contexts.

    returns str: url of the realtime exchange
        rate for any pair of digital currency (e.g., Bitcoin)
        or physical currency (e.g., USD).
    """
    def get_url(self, **kwargs: dict) -> str:
        function_name: str = kwargs["function_name"]
        base_coin = kwargs["base_coin"]
        secondary_coin = kwargs["secondary_coin"]
        api_token = kwargs["api_token"]

        function_query: str = f"function={function_name}&"
        additional_from_arg: str = f"from_currency={base_coin}&"
        additional_to_arg: str = f"to_currency={secondary_coin}&"
        api_key: str = f"apikey={api_token}"
        list_of_params: list = [function_query, additional_from_arg,
                                additional_to_arg, api_key]
        url_api: str = URLS_API["api_vantage"]

        for param in list_of_params:
            url_api += param

        return url_api


class DailyExchange(URLGeter):
    """
    get_url Daily exchange url
    API Parameters

    ❚ Required: function
    The time series of your choice. In this case,
    function=DIGITAL_CURRENCY_DAILY

    ❚ Required: symbol
    The digital/crypto currency of your choice.
    It can be any of the currencies in the digital currency list.
    For example: symbol=BTC.

    ❚ Required: market
    The exchange market of your choice.
    It can be any of the market in the market list.
    For example: market=CNY.

    ❚ Required: apikey
    Your API key.
    """
    def get_url(self, **kwargs: dict) -> str:
        function_name: str = kwargs["function_name"]
        symbol = kwargs["symbol"]
        market = kwargs["market"]
        api_token = kwargs["api_token"]

        function_query: str = f"function={function_name}&"
        symbol_arg: str = f"symbol={symbol}&"
        market_arg: str = f"market={market}&"
        api_key: str = f"apikey={api_token}"
        list_of_params: list = [function_query, symbol_arg,
                                market_arg, api_key]
        url_api: str = URLS_API["api_vantage"]

        for param in list_of_params:
            url_api += param

        return url_api


class GetURLRequest:
    """
     Class to handle different methods depending on context
    """

    def set_strategy(self, strategy: URLGeter):
        """
        set_strategy Define strategy for future calls

        Args:
            strategy (URLGeter): inherite the parent class
        """
        self.strategy = strategy

    def form_url(self, **kwargs):
        """
        form_url Method that works on different contexts

        kwargs depends on the context you want to use API Vantage

        Returns:
            str: String representation of the url GET request
        """
        return self.strategy.get_url(**kwargs)
