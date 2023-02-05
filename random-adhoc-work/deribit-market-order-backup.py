import configparser
import requests

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

def place_market_order(instrument_name, amount, label, access_token):
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
place_market_order("ETH_USDC-PERPETUAL", 0.01, "my_market_order", access_token)
