import configparser
import requests, json

# Read the configuration file
config = configparser.ConfigParser()
config.read('config.ini')

client_id = config['DEFAULT']['client_id']
client_secret = config['DEFAULT']['client_secret']
import requests

url = "https://www.deribit.com/api/v2/public/get_instrument"

querystring = {"instrument_name":"ETH-31MAR23-1600-C"}

response = requests.request("GET", url, params=querystring)

instrument_details = response.json()

print(instrument_details)
