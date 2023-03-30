import configparser
import requests
import time
import pandas as pd
from flask import Flask, render_template

app = Flask(__name__)

# Constants
HISTORICAL_IV = {
    "ETH": {"LOW": 15.55, "HIGH": 185.90},
    "BTC": {"LOW": 9.28, "HIGH": 127.08}
}

# Data Directory
DIR = "/home/gmurray/REPO/trading/data"

# Read the configuration file
config = configparser.ConfigParser()
config.read('/home/gmurray/REPO/trading/config.ini')

client_id = config['DEFAULT']['client_id']
client_secret = config['DEFAULT']['client_secret']

def calculate_ivr(currency, mark_iv):
    historical_low_iv = HISTORICAL_IV[currency]["LOW"]
    historical_high_iv = HISTORICAL_IV[currency]["HIGH"]
    return (mark_iv - historical_low_iv) / (historical_high_iv - historical_low_iv) * 100

def calculate_ivp(currency, mark_iv):
    historical_low_iv = HISTORICAL_IV[currency]["LOW"]
    df = pd.read_csv(f"{DIR}/historical_{currency.lower()}_iv.csv", encoding="utf-8", sep=',')
    ivp = df.query("HV < @mark_iv").count()[0]/365*100
    return ivp

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

# Filter the expiries based on open interest between 25 and 60 days
now = int(time.time() * 1000)
expiries = [d for d in data
            if d["expiration_timestamp"] > now
            and d["expiration_timestamp"] - now >= 25*86400*1000
            and d["expiration_timestamp"] - now <= 80*86400*1000]

# Filter the expiries based on strikes less than 0.30 delta
filtered_exp_lt_50 = []
filtered_exp_lt_80 = []

for exp in expiries:
    endpoint = f"https://www.deribit.com/api/v2/public/get_order_book_by_instrument_id?instrument_id={exp['instrument_id']}"
    response = requests.get(endpoint)
    order_book = response.json()
    currency = exp["base_currency"]
    if "result" in order_book and order_book['result'] and order_book['result']['open_interest']:
        delta = order_book['result']['greeks']['delta']
        if 0.15 < abs(delta) < 0.32:
            index_price = btc_index_price if exp["base_currency"] == "BTC" else eth_index_price
            mark_iv = order_book['result']['mark_iv']
            range_min, range_max = calculate_range(index_price, mark_iv)
            filtered_exp_dict = {
                "instrument_name": exp["instrument_name"],
                "mark_iv": mark_iv,
                "option_type": exp["option_type"],
                "strike": exp["strike"],
                "delta": delta,
                "volume": order_book["result"]['stats']["volume"],
                "open_interest": order_book["result"]["open_interest"],
                "range": f"{range_min:.0f} - {range_max:.0f}",
                "days_to_expiry": (pd.to_datetime(exp['expiration_timestamp'], unit='ms') - pd.Timestamp.now()).days,
                "ivr": calculate_ivr(currency, mark_iv),
                "ivp": calculate_ivp(currency, mark_iv),
            }
            if filtered_exp_dict["days_to_expiry"] < 50:
                filtered_exp_lt_50.append(filtered_exp_dict)
            elif filtered_exp_dict["days_to_expiry"] < 80:
                filtered_exp_lt_80.append(filtered_exp_dict)

df_lt_50 = pd.DataFrame(filtered_exp_lt_50, columns=["instrument_name", "mark_iv", "ivr", "ivp", "option_type", "strike", "delta", "volume", "open_interest", "range", "days_to_expiry"])
df_lt_80 = pd.DataFrame(filtered_exp_lt_80, columns=["instrument_name", "mark_iv", "ivr", "ivp", "option_type", "strike", "delta", "volume", "open_interest", "range", "days_to_expiry"])

df_lt_50_sorted = df_lt_50.sort_values(by=['ivp', 'ivr'], ascending=[False, False])
df_lt_80_sorted = df_lt_80.sort_values(by=['ivp', 'ivr'], ascending=[False, False])

data_lt_50 = df_lt_50_sorted.to_dict('records')
data_lt_80 = df_lt_80_sorted.to_dict('records')


# Print the DataFrame
#print(df_sorted)

@app.route('/ivp')
def ivp():
    return render_template('table.html', data_less_than_50=data_lt_50, data_less_than_80=data_lt_80)

if __name__ == '__main__':
    app.run(debug=True, port=5008)
