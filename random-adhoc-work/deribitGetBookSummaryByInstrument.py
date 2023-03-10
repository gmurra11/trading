import configparser
import requests, json

# Read the configuration file
config = configparser.ConfigParser()
config.read('config.ini')

client_id = config['DEFAULT']['client_id']
client_secret = config['DEFAULT']['client_secret']

url = "https://test.deribit.com/api/v2/public/get_book_summary_by_instrument"

querystring = {"instrument_name":"ETH-31MAR23-2000-C"}

response = requests.request("GET", url, params=querystring)

print(response.text)
