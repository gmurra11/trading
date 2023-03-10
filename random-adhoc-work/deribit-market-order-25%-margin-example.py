import requests

# Replace YOUR_API_KEY and YOUR_API_SECRET with your actual API key and secret
api_key = "YOUR_API_KEY"
api_secret = "YOUR_API_SECRET"

# Set the URL for the Deribit API
url = "https://test.deribit.com/api/v2/private/buy"

# Set the payload for the request
payload = {
    "instrument_name": "ETH-PERPETUAL",
    "amount": 25000,
    "type": "market",
    "label": "my_market_order",
    "options": [{"option_type": "call", "strike_price": 0, "amount": 0.25}],
}

# Set the headers for the request
headers = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {api_key}:{api_secret}",
}

# Send the request to the Deribit API
response = requests.post(url, json=payload, headers=headers)

# Print the response from the API
print(response.json())
