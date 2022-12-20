import configparser
import requests, json

# Read the configuration file
config = configparser.ConfigParser()
config.read('config.ini')

client_id = config['DEFAULT']['client_id']
client_secret = config['DEFAULT']['client_secret']

def get_access_token(client_id, client_secret):
    # Set the URL for the Deribit API
    url = "https://test.deribit.com/api/v2/public/auth"

    # Set the query parameters
    params = {
        "client_id": client_id,
        "client_secret": client_secret,
        "grant_type": "client_credentials"
    }

    # Set the headers for the request
    headers = {
        "Content-Type": "application/json"
    }

    # Send the GET request
    response = requests.get(url, params=params, headers=headers)

    # Parse the response
    response_json = response.json()
    #print(response_json)

    # Extract the access_token field
    access_token = response_json['result']['access_token']

    # Return the access_token
    return access_token

def get_open_orders_by_instrument(instrument_name, access_token):
    # Set the API endpoint URL
    url = "https://test.deribit.com/api/v2/private/get_open_orders_by_instrument"

    # Set the request payload
    params = {
        "instrument_name": instrument_name,
        "type": all
    }

    # Set the request headers
    headers = {
        "Content-Type": "application/json",
        "Authorization": "Bearer {}".format(access_token)
    }

    # Make the request
    response = requests.get(url, params=params, headers=headers)

    # Check if the request was successful
    if response.status_code != 200:
        print("Request was not successful:")
        print(response)
        return []

    # Parse the response
    orders = response.json()
    print(orders)

    # Extract the result field
    if "result" in orders and isinstance(orders["result"], list) and orders["result"]:
        open_orders = [order for order in orders["result"] if order["state"] == "open"]
    else:
        open_orders = []

    # Return the orders
    return open_orders

def get_user_trades_by_instrument(instrument_name, access_token):
    # Set the URL for the Deribit API
    url = "https://test.deribit.com/api/v2/private/get_user_trades_by_instrument"

    # Set the query parameters
    params = {
        "instrument_name": instrument_name
    }

    # Set the headers for the request
    headers = {
        "Content-Type": "application/json",
        "Authorization": "Bearer {}".format(access_token)
    }

    # Send the GET request
    response = requests.get(url, params=params, headers=headers)

    if response.status_code != 200:
        print("Request was not successful:")
        print(response)
        return []

    #print(response.content)

    # Parse the response
    result = response.json()
    #print(result)

    # Extract the trades field
    # Extract the trades field
    trades = result.get('trades', [])

    #print(trades)

    # Filter the trades by state
    open_trades = [trade for trade in trades if trade['state'] == 'open']

    print(open_trades)
    # Return the trades
    return open_trades


def place_market_order_buy(instrument_name, amount, label, access_token):
    private_buy = "https://test.deribit.com/api/v2/private/buy"

    # Set the payload for the request
    payload = {
        "instrument_name": instrument_name,
        "amount": amount,
        "type": "market",
        "label": label
    }

    headers = {
        "Content-Type": "application/json",
        "Authorization": "Bearer {}".format(access_token)
    }

    try:
        # Send the request to the Deribit API
        response = requests.get(private_buy, params=payload, headers=headers)
        print(response)
        response_json = response.json()
    except requests.exceptions.RequestException as e:
        # Print the error message if the request fails
        print(e)

def place_market_order_sell(instrument_name, amount, label, access_token):
    private_buy = "https://test.deribit.com/api/v2/private/buy"

    # Set the payload for the request
    payload = {
        "instrument_name": instrument_name,
        "amount": amount,
        "type": "market",
        "label": label
    }

    headers = {
        "Content-Type": "application/json",
        "Authorization": "Bearer {}".format(access_token)
    }

    try:
        # Send the request to the Deribit API
        response = requests.get(private_buy, params=payload, headers=headers)
        print(response)
        response_json = response.json()
    except requests.exceptions.RequestException as e:
        # Print the error message if the request fails
        print(e)

# Example usage:
access_token = get_access_token(client_id, client_secret)
#open_trades = get_user_trades_by_instrument("ETH_USDC-PERPETUAL", access_token)
#open_orders = get_open_orders_by_instrument("ETH_USDC-PERPETUAL", access_token)

#print(open_orders)
#print(open_trades)


#place_market_order_buy("ETH_USDC-PERPETUAL", 0.01, "my_market_order", access_token)

"""
if not open_trades:
    # There are no open positions, so place a market order
    place_market_order("ETH_USDC-PERPETUAL", 0.01, "my_market_order", access_token)
    print("in here")
else:
    print("You have an EXISTING Market order running")
"""
