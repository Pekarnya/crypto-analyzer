"""
 Collecting the data from the AlphaVantage API
"""

import aiohttp


class DataCollector():
    """
    DataCollector collects the data from exchange API

    Actual prices of crypto coins
    """    """"""

    def __init__(self) -> None:
        """Constructor of the DataCollector object
        Args: coin - is the actual coin name"""
        ...

    async def get_coin_price(self, url: str) -> dict:
        """
        get_coin_price Asyncio method

        use it only with asyncio.run()

        Args:
            url (str): url of the api you have chosen

        Returns:
            dict: {response: response_status,
                   output: text_formated_output}
        """
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                status_code = response.status
                output_api = await response.json()
        return {"status": status_code, "output": output_api}
