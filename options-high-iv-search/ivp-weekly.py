import configparser
import requests
import pandas as pd
import csv
from flask import Flask, render_template

app = Flask(__name__)

NEAREST_FRI_STRIKES_FILE = f"{DIR}/Nearest-Fri-Options.txt"

# Data Directory
DIR = "/home/gmurray/REPO/trading/data-weekly"

# Constants
HISTORICAL_LOW_IV = 15.55
HISTORICAL_HIGH_IV = 185.90


# Read the configuration file
config = configparser.ConfigParser()
config.read('/home/gmurray/REPO/trading/config.ini')

client_id = config['DEFAULT']['client_id']
client_secret = config['DEFAULT']['client_secret']

url_instrument_id = "https://www.deribit.com/api/v2/public/get_instrument"
url_order_book = "https://www.deribit.com/api/v2/public/get_order_book_by_instrument_id"

def calculate_ivr(mark_iv):
    return (mark_iv - HISTORICAL_LOW_IV) / (HISTORICAL_HIGH_IV - HISTORICAL_LOW_IV) * 100

def calculate_ivp(mark_iv):
    df = pd.read_csv(f"{DIR}/historical_eth_iv.csv", encoding="utf-8", sep=',')
    ivp = df.query("HV < @mark_iv").count()[0]/365*100
    return ivp

def extract_call_totals(instrument_name, csv_file):

    strike = instrument_name.split('-')[2]

    # Read the csv file and find the corresponding strike
    with open(csv_file, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            if row["Strike"] == strike:
                calls_buy = abs(int(row["Calls Buy"]))
                calls_sell = abs(int(row["Calls Sell"]))
                calls_total = calls_buy + calls_sell
                return calls_total

def extract_put_totals(instrument_name, csv_file):

    strike = instrument_name.split('-')[2]

    # Read the csv file and find the corresponding strike
    with open(csv_file, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            if row["Strike"] == strike:
                puts_buy = abs(int(row["Puts Buy"]))
                puts_sell = abs(int(row["Puts Sell"]))
                puts_total = puts_buy + puts_sell
                return puts_total

def nearest_friday_call_table():
    options = []
    with open(NEAREST_FRI_STRIKES_FILE, "r") as file:
        for line in file:
            instrument_name = line.strip() + "C"  #appending C for Call to the name
            query_instrument_name = {"instrument_name": instrument_name}
            #print(instrument_name)

            response_instrument_name = requests.request("GET", url_instrument_id, params=query_instrument_name)
            #print(response_instrument_name)

            #I need the instrument ID from get_instrument api call
            instrument_details = response_instrument_name.json()
            #print(instrument_details)

            #I pass this to get_order_book_by_instrument_id to get the mark_iv
            query_for_mark_iv = {"instrument_id": instrument_details['result']['instrument_id']}
            #print(query_for_mark_iv)

            response_mark_iv = requests.request("GET", url_order_book, params=query_for_mark_iv)

            iv_details = response_mark_iv.json()

            if 'result' in iv_details and 'mark_iv' in iv_details['result'] and iv_details['result']['mark_iv'] is not None:
                mark_iv = iv_details['result']['mark_iv']
                ivr = calculate_ivr(mark_iv)
                ivp = calculate_ivp(mark_iv)
                oi = iv_details['result']['open_interest']
                vol = iv_details['result']['stats']['volume']
                options.append((instrument_name, mark_iv, ivr, ivp, oi, vol))

    nearest_friday_sorted_options = sorted(options, key=lambda x: (x[3], x[2]))

    for option in nearest_friday_sorted_options:
        print(f"Instrument Name: {option[0]}")
        print(f"IV: {option[1]:.2f}%")
        print(f"IVR: {option[2]:.2f}%")
        print(f"IVP: {option[3]:.2f}%")
        print(f"OI: {int(option[4])}")
    return nearest_friday_sorted_options[:15]

@app.route('/ivp-high-iv-search')
def push_web():
    nearest_friday_call = nearest_friday_call_table()
    return render_template('table.html', data_nearest_friday_call=nearest_friday_call)

if __name__ == '__main__':
    app.run(debug=True, port=5003)
