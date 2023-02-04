import configparser
import requests, json

# Read the configuration file
config = configparser.ConfigParser()
config.read('config.ini')

client_id = config['DEFAULT']['client_id']
client_secret = config['DEFAULT']['client_secret']

url = "https://www.deribit.com/api/v2/public/get_order_book_by_instrument_id"

querystring = {"instrument_id":"216550","depth":10}

response = requests.request("GET", url, params=querystring)

print(response.text)
