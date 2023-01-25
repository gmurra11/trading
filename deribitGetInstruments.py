import configparser
import requests, json

# Read the configuration file
config = configparser.ConfigParser()
config.read('config.ini')

client_id = config['DEFAULT']['client_id']
client_secret = config['DEFAULT']['client_secret']

url = "https://test.deribit.com/api/v2/public/get_instruments"

querystring = {"currency":"ETH","kind":"option"}

response = requests.request("GET", url, params=querystring)

instruments = response.json()

print(instruments)
