import requests
import time
import pandas as pd

# Set the API endpoint for BTC and ETH index prices
btc_get_index_endpoint = "https://www.deribit.com/api/v2/public/get_index?currency=BTC"
eth_get_index_endpoint = "https://www.deribit.com/api/v2/public/get_index?currency=ETH"

# Make the API requests and get the responses
btc_get_index_response = requests.get(btc_get_index_endpoint)
eth_get_index_response = requests.get(eth_get_index_endpoint)

# Get the BTC and ETH index prices from the responses
btc_index_price = btc_get_index_response.json()["result"]['BTC']
eth_index_price = eth_get_index_response.json()["result"]['ETH']

def calculate_range(price, mark_iv):
    range_pct = mark_iv / 100
    min_range = price - (price * range_pct)
    max_range = price + (price * range_pct)
    return min_range, max_range

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
            and d["expiration_timestamp"] - now <= 80*86400*1000]

# Filter the expiries based on strikes less than 0.30 delta
filtered_exp = []
for exp in expiries:
    endpoint = f"https://www.deribit.com/api/v2/public/get_order_book_by_instrument_id?instrument_id={exp['instrument_id']}"
    response = requests.get(endpoint)
    order_book = response.json()
    if "result" in order_book and order_book['result'] and order_book['result']['open_interest']:
        delta = order_book['result']['greeks']['delta']
        if 0.15 < abs(delta) < 0.30:
            #print(exp["base_currency"])
            index_price = btc_index_price if exp["base_currency"] == "BTC" else eth_index_price
            #print(index_price)
            range_min, range_max = calculate_range(index_price, order_book['result']['mark_iv'])
            filtered_exp.append({
                "instrument_name": exp["instrument_name"],
                "mark_iv": order_book['result']['mark_iv'],
                "option_type": exp["option_type"],
                "strike": exp["strike"],
                "delta": delta,
                "volume": order_book["result"]['stats']["volume"],
                "open_interest": order_book["result"]["open_interest"],
                "range": f"{range_min:.0f} - {range_max:.0f}"
            })

# Convert the filtered data to a pandas DataFrame
df = pd.DataFrame(filtered_exp, columns=["instrument_name", "mark_iv", "option_type", "strike", "delta", "volume", "open_interest", "range"])

# Print the DataFrame
print(df)
