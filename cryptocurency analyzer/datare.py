"""
 Alternate way to collect statistical data
"""

import pandas as pd
import numpy as np

ETH_USD_PATH = "cryptocurency analyzer/reserve_data/ETH-USD.csv"
BTC_USD_PATH = "cryptocurency analyzer/reserve_data/BTC-USD.csv"


def reserve_data() -> np.ndarray:
    """
    reserve_data Loading reserve data
    if AlphaVantage returns wrong json

    Returns:
        np.array: Using the np array representation
        allows us to calc Pearson coefficient
    """
    etherium = pd.read_csv(ETH_USD_PATH, nrows=7, usecols=[2, 3, 4, 5])
    bitcoin = pd.read_csv(BTC_USD_PATH, nrows=7, usecols=[2, 3, 4, 5])
    eth_prices = np.array(etherium.values)
    btc_prices = np.array(bitcoin.values)
    return btc_prices, eth_prices
