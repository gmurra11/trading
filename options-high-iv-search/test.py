import requests
import time

# Set the API endpoint and parameters
endpoint = "https://www.deribit.com/api/v2/public/get_instruments"
params = {
    "currency": "BTC",
    "kind": "option",
    "expired": "false"
}

# Make the API request and get the response
response = requests.get(endpoint, params=params)
data = response.json()

#Format to extract expiration
#print(data['result'][0]['expiration_timestamp'])

# Filter the expiries based on open interest between 30 and 60 days
now = int(time.time() * 1000)
expiries = [d["expiration_timestamp"] for d in data['result']
            if d["expiration_timestamp"] > now
            and d["expiration_timestamp"] - now >= 30*86400*1000
            and d["expiration_timestamp"] - now <= 60*86400*1000]
print(expiries)
