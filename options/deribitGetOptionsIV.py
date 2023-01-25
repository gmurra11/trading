import configparser
import requests
import pandas as pd
from flask import Flask, render_template

app = Flask(__name__)

@app.route('/table')
def table():
    # Constants
    HISTORICAL_LOW_IV = 15.55
    HISTORICAL_HIGH_IV = 185.90

    # Read the configuration file
    config = configparser.ConfigParser()
    config.read('../config.ini')

    client_id = config['DEFAULT']['client_id']
    client_secret = config['DEFAULT']['client_secret']

    url_instrument_id = "https://www.deribit.com/api/v2/public/get_instrument"
    url_order_book = "https://www.deribit.com/api/v2/public/get_order_book_by_instrument_id"

    def calculate_ivr(mark_iv):
        return (mark_iv - HISTORICAL_LOW_IV) / (HISTORICAL_HIGH_IV - HISTORICAL_LOW_IV) * 100

    def calculate_ivp(mark_iv):
        df = pd.read_csv("historical_eth_iv.csv", encoding="utf-8", sep=',')
        ivp = df.query("HV < @mark_iv").count()[0]/365*100
        return ivp

    options = []
    with open("optionInstrumentList.txt", "r") as file:
        for line in file:
            instrument_name = line.strip()
            query_instrument_name = {"instrument_name": instrument_name}

            response_instrument_name = requests.request("GET", url_instrument_id, params=query_instrument_name)

            #I need the instrument ID from get_instrument api call
            instrument_details = response_instrument_name.json()

            #I pass this to get_order_book_by_instrument_id to get the mark_iv
            query_for_mark_iv = {"instrument_id": instrument_details['result']['instrument_id']}

            response_mark_iv = requests.request("GET", url_order_book, params=query_for_mark_iv)

            iv_details = response_mark_iv.json()

            if 'result' in iv_details and 'mark_iv' in iv_details['result'] and iv_details['result']['mark_iv'] is not None:
                mark_iv = iv_details['result']['mark_iv']
                ivr = calculate_ivr(mark_iv)
                ivp = calculate_ivp(mark_iv)
                options.append((instrument_name, mark_iv, ivr, ivp))

    sorted_options = sorted(options, key=lambda x: (x[3], x[2]))

    for option in sorted_options:
        print(f"Instrument Name: {option[0]}")
        print(f"IV: {option[1]:.2f}%")
        print(f"IVR: {option[2]:.2f}%")
        print(f"IVP: {option[3]:.2f}%")

    return render_template('table.html', data=sorted_options)

if __name__ == '__main__':
    app.run(debug=True)
