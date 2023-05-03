"""
 contains functions for tracking the price action

If you want to track the price action you have to
run this module
"""
import time
import schedule
from currency import CurrencyStatistics


def price_tracker(pirson_corr: float, coins: CurrencyStatistics,
                  crypto_coin: str, is_premium: bool):
    """
    Tracks price changes on the market via AlphaVantage api.

    This function uses the AlphaVantage API to track changes in the price of a
    cryptocurrency over time. It calculates the decoupled price action of the
    cryptocurrency and logs it to provide visibility into how the price is changing.

    Args:
        pirson_corr (float): Pearson Product Moment Correlation
        coins (CurrencyStatistics): object of CurrencyStatistics class
        crypto_coin (str): string acronym f.e ETH
        is_premium (bool): AlphaVantage API premium option provide more
        information, allow for user make more requests.
    """
    def pause():
        start_time = time.time()
        while time.time() - start_time < 12:
            pass

    def price_action_cummulative(coin_price_action,
                                 decoupled_coin_price_action):
        """
        Calculates the cumulative price action of a cryptocurrency.

        This function calculates the cumulative price action of
        a cryptocurrency based on its current and previous prices.
        It returns a dictionary that contains the cumulative price
        action for both coupled and decoupled prices.

        Args:
            coin_price_action (float): The current price action
            of the cryptocurrency.
            decoupled_coin_price_action (float): The decoupled price action
            of the cryptocurrency.

        Returns:
            counter_dict (dict): A dictionary that contains the cumulative
            price action for both coupled and decoupled prices.

        """

        global price_action_counter
        price_action_counter += coin_price_action
        global decoupled_price_action_counter
        decoupled_price_action_counter += decoupled_coin_price_action
        counter_dict = {"coupled": price_action_counter,
                        "decoupled": decoupled_price_action_counter}
        return counter_dict

    def update_prices():
        global price_action_counter
        price_action_counter = 0.0
        global decoupled_price_action_counter
        decoupled_price_action_counter = 0.0
        print("updated")

    schedule.every().hour.do(update_prices)

    i = 0
    while True:
        if i > 5:
            i = 0
        schedule.run_pending()
        i += 1
        prev_coin_price = coins.current_price(crypto_coin)
        if i == 1:
            print(f"current price is {prev_coin_price}")
        if is_premium is False and i == 1:
            print(f"using premium is {is_premium}, only 5 requests per minute")
            pause()
        curr_coin_price = coins.current_price(crypto_coin)

        if prev_coin_price is not None and curr_coin_price is not None:
            coin_price_action = CurrencyStatistics.roc_method(curr_coin_price,
                                                              prev_coin_price)

            decoupled_coin_price_action = coins.decoupling(coin_price_action,
                                                           pirson_corr)
            print(f"Decoupled price action:{decoupled_coin_price_action}")

            counter_dict: dict = price_action_cummulative(coin_price_action,
                                                          decoupled_coin_price_action)

            decoupling_price_action_hour = counter_dict["decoupled"]

            print(f"current {crypto_coin} price decoupling change last \
                      hour: {decoupling_price_action_hour}")

            if decoupling_price_action_hour >= 1:
                print(f"{crypto_coin} decoupled price action had changed")
                print(f"current {crypto_coin} price decoupling change last \
                      hour: {decoupling_price_action_hour}")
            else:
                continue
        else:
            # print("Bad response from the server")
            continue


def main():
    """
    main(): Set the parameters to initialize
    price_tracker()
    """
    btc_prices, eth_prices = None, None
    while btc_prices is None or eth_prices is None:
        btc = "BTC"
        eth = "ETH"
        coins = CurrencyStatistics("VANTAGE", "./API.env", btc, eth)
        btc_prices, eth_prices = coins.historic_data(7)
        if btc_prices is None or eth_prices is None:
            print("Bad response from API")

    pirson_corr = coins.pirson_coef(btc_prices, eth_prices)
    print(f"correlation last period is: {pirson_corr}")
    price_tracker(pirson_corr, coins, eth, is_premium=False)


price_action_counter = 0.0
decoupled_price_action_counter = 0.0


if __name__ == "__main__":
    main()
