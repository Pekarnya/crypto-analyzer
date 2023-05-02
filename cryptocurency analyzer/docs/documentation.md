# url module documentation
================================================================

This module use strategy aproach due the various options of the
Alphavantage API. Here is an example of using DailyExchange function
of the API:
----------------------------------------------------------------

<# Create an instance of GetURLRequest
url_request = GetURLRequest()

# Set the strategy to CurrentExchange
url_request.set_strategy(DailyExchange())

# Create a dictionary of keyword arguments
kwargs = {
    "function_name": "DIGITAL_CURRENCY_DAILY",
    "symbol": "BTC",
    "market": "USD",
    "api_token": "Your_token"
}

# Call form_url on the GetURLRequest instance with the keyword arguments
url = url_request.form_url(**kwargs)
print(url)>


## Example of using CurentExchange:

<# Create an instance of GetURLRequest
url_request = GetURLRequest()

# Set the strategy to CurrentExchange
url_request.set_strategy(CurrentExchange())

# Create a dictionary of keyword arguments
kwargs = {
    "function_name": "CURRENCY_EXCHANGE_RATE",
    "base_coin": "BTC",
    "secondary_coin": "USD",
    "api_token": "Your token"
}

# Call form_url on the GetURLRequest instance with the keyword arguments
url = url_request.form_url(**kwargs)
print(url)>

You have to provide parametres in the kwargs dict with the
valid parameters that a mentioned at https://www.alphavantage.co/documentation/