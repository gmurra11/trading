import requests
import time
import pandas as pd

# Set the API endpoint and parameters for BTC options
btc_endpoint = "https://www.deribit.com/api/v2/public/get_instruments"
btc_params = {
    "currency": "BTC",
    "kind": "option",
    "expired": "false"
}

# Make the BTC options API request and get the response
btc_response = requests.get(btc_endpoint, params=btc_params)
btc_data = btc_response.json()

# Set the API endpoint and parameters for ETH options
eth_endpoint = "https://www.deribit.com/api/v2/public/get_instruments"
eth_params = {
    "currency": "ETH",
    "kind": "option",
    "expired": "false"
}

# Make the ETH options API request and get the response
eth_response = requests.get(eth_endpoint, params=eth_params)
eth_data = eth_response.json()

# Combine the BTC and ETH data
data = btc_data["result"] + eth_data["result"]

# Filter the expiries based on open interest between 30 and 60 days
now = int(time.time() * 1000)
expiries = [d for d in data
            if d["expiration_timestamp"] > now
            and d["expiration_timestamp"] - now >= 30*86400*1000
            and d["expiration_timestamp"] - now <= 60*86400*1000]

# Create a pandas DataFrame from the filtered expiries data
df = pd.DataFrame(expiries, columns=["instrument_name", "tick_size", "expiration_timestamp", "creation_timestamp", "contract_size", "underlying_index", "underlying_price", "settlement_period", "option_type", "strike", "base_currency", "quote_currency"])

# Print the DataFrame
print(df)
