# Use to access OTC Institutional Investors - Where are they placing their bets

import configparser
import requests
import pandas as pd
import csv
from flask import Flask, render_template

app = Flask(__name__)

# Data Directory
DIR = "/home/gmurray/REPO/trading/data"
# T-1
T1 = "/home/gmurray/REPO/trading/data/daily"

# Files
MARCH_STRIKES_FILE = f"{DIR}/March-Q1-Options.txt"
MARCH_LVT_WEEKLY_CSV_FILE = f"{DIR}/LVT-WEEKLY-31MAR23.csv"
MARCH_LVT_MONTHLY_CSV_FILE = f"{DIR}/LVT-MONTHLY-31MAR23.csv"
JUNE_STRIKES_FILE = f"{DIR}/June-Q2-Options.txt"
JUNE_LVT_WEEKLY_CSV_FILE = f"{DIR}/LVT-WEEKLY-30JUN23.csv"
JUNE_LVT_MONTHLY_CSV_FILE = f"{DIR}/LVT-MONTHLY-30JUN23.csv"
SEPTEMBER_STRIKES_FILE = f"{DIR}/September-Q3-Options.txt"
SEPTEMBER_LVT_WEEKLY_CSV_FILE = f"{DIR}/LVT-WEEKLY-29SEP23.csv"
SEPTEMBER_LVT_MONTHLY_CSV_FILE = f"{DIR}/LVT-MONTHLY-29SEP23.csv"

# T-1 Files (From Daily)
MARCH_STRIKES_FILE_T1 = f"{T1}/March-Q1-Options.txt"
MARCH_LVT_WEEKLY_CSV_FILE_T1 = f"{T1}/LVT-WEEKLY-31MAR23.csv"
MARCH_LVT_MONTHLY_CSV_FILE_T1 = f"{T1}/LVT-MONTHLY-31MAR23.csv"
JUNE_STRIKES_FILE_T1 = f"{T1}/June-Q2-Options.txt"
JUNE_LVT_WEEKLY_CSV_FILE_T1 = f"{T1}/LVT-WEEKLY-30JUN23.csv"
JUNE_LVT_MONTHLY_CSV_FILE_T1 = f"{T1}/LVT-MONTHLY-30JUN23.csv"
SEPTEMBER_STRIKES_FILE_T1 = f"{T1}/September-Q3-Options.txt"
SEPTEMBER_LVT_WEEKLY_CSV_FILE_T1 = f"{T1}/LVT-WEEKLY-29SEP23.csv"
SEPTEMBER_LVT_MONTHLY_CSV_FILE_T1 = f"{T1}/LVT-MONTHLY-29SEP23.csv"

# Read the configuration file
config = configparser.ConfigParser()
config.read('/home/gmurray/REPO/trading/config.ini')

client_id = config['DEFAULT']['client_id']
client_secret = config['DEFAULT']['client_secret']

def put_call_ratio(calls, puts):
    pc_ratio = 0

    call_total = 0
    # option[2] is based off monthly data
    for option in calls:
        call_total = call_total + int(option[2])

    put_total = 0
    # option[2] is based off monthly data
    for option in puts:
        put_total = put_total + int(option[2])

    pc_ratio = put_total / call_total

    return pc_ratio

def extract_call_totals(instrument_name, csv_file):

    strike = instrument_name.split('-')[2]

    # Read the csv file and find the corresponding strike
    with open(csv_file, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            if row["Strike"] == strike:
                blocked_calls_buy = abs(int(row["Call Buy Blocked"]))
                blocked_calls_sell = abs(int(row["Call Sell Blocked"]))
                blocked_calls_total = blocked_calls_buy + blocked_calls_sell
                return blocked_calls_total


def extract_put_totals(instrument_name, csv_file):

    strike = instrument_name.split('-')[2]

    # Read the csv file and find the corresponding strike
    with open(csv_file, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            if row["Strike"] == strike:
                blocked_puts_buy = 0
                if row["Put Buy Blocked"] and row["Put Buy Blocked"] != "":
                    blocked_puts_buy = abs(int(row["Put Buy Blocked"]))

                blocked_puts_sell = 0
                if row["Put Sell Blocked"] and row["Put Sell Blocked"] != "":
                    blocked_puts_sell = abs(int(row["Put Sell Blocked"]))
                blocked_puts_total = blocked_puts_buy + blocked_puts_sell

                return blocked_puts_total

def march_call_table():
    call_options = []
    call_options_t1 = []
    with open(MARCH_STRIKES_FILE, "r") as file:
        for line in file:
            instrument_name = line.strip() + "C"  #appending C for Call to the name
            query_instrument_name = {"instrument_name": instrument_name}

            weekly_call_totals = extract_call_totals(instrument_name, MARCH_LVT_WEEKLY_CSV_FILE)
            monthly_call_totals = extract_call_totals(instrument_name, MARCH_LVT_MONTHLY_CSV_FILE)
            weekly_call_totals_t1 = extract_call_totals(instrument_name, MARCH_LVT_WEEKLY_CSV_FILE_T1)
            monthly_call_totals_t1 = extract_call_totals(instrument_name, MARCH_LVT_MONTHLY_CSV_FILE_T1)

            call_options.append((instrument_name, weekly_call_totals, monthly_call_totals))
            call_options_t1.append((instrument_name, weekly_call_totals_t1, monthly_call_totals_t1))

    call_options_diff = []
    for option, option_t1 in zip(call_options, call_options_t1):
        weekly_diff = 0 if option_t1[1] == 0 else  round((abs(option[1] - option_t1[1]) / option_t1[1]) * 100, 2)
        monthly_diff = 0 if option_t1[2] == 0 else round((abs(option[2] - option_t1[2]) / option_t1[2]) * 100, 2)
        call_options_diff.append((option[0], option[1], option[2], weekly_diff, monthly_diff))

    march_sorted_call_options = sorted(call_options_diff, key=lambda x: (x[2], x[1]), reverse=True)

    for option in march_sorted_call_options:
        print(f"Instrument Name: {option[0]}")
        print(f"WEEKLY CALL TOTALS: {int(option[1])}")
        print(f"WEEKLY % DIFFERENCE: {round(float(option[3]), 2)}")
        print(f"MONTHLY CALL TOTALS: {int(option[2])}")
        print(f"MONTHLY % DIFFERENCE: {round(float(option[4]), 2)}")
    return march_sorted_call_options

def march_put_table():
    put_options = []
    with open(MARCH_STRIKES_FILE, "r") as file:
        for line in file:
            instrument_name = line.strip() + "P"  #appending P for Call to the name
            query_instrument_name = {"instrument_name": instrument_name}

            weekly_put_totals = extract_put_totals(instrument_name, MARCH_LVT_WEEKLY_CSV_FILE)
            monthly_put_totals = extract_put_totals(instrument_name, MARCH_LVT_MONTHLY_CSV_FILE)

            put_options.append((instrument_name, weekly_put_totals, monthly_put_totals))

    march_sorted_put_options = sorted(put_options, key=lambda x: (x[2], x[1]), reverse=True)

    for option in march_sorted_put_options:
        print(f"Instrument Name: {option[0]}")
        print(f"WEEKLY PUT TOTALS: {int(option[1])}")
        print(f"MONTHLY PUT TOTALS: {int(option[2])}")
    return march_sorted_put_options

def june_call_table():
    call_options = []
    with open(JUNE_STRIKES_FILE, "r") as file:
        for line in file:
            instrument_name = line.strip() + "C"  #appending P for Call to the name
            query_instrument_name = {"instrument_name": instrument_name}

            weekly_call_totals = extract_call_totals(instrument_name, JUNE_LVT_WEEKLY_CSV_FILE)
            monthly_call_totals = extract_call_totals(instrument_name, JUNE_LVT_MONTHLY_CSV_FILE)
            call_options.append((instrument_name, weekly_call_totals, monthly_call_totals))

    june_sorted_call_options = sorted(call_options, key=lambda x: (x[2], x[1]), reverse=True)

    for option in june_sorted_call_options:
        print(f"Instrument Name: {option[0]}")
        print(f"WEEKLY CALL TOTALS: {int(option[1])}")
        print(f"MONTHLY CALL TOTALS: {int(option[2])}")
    return june_sorted_call_options

def june_put_table():
    put_options = []
    with open(JUNE_STRIKES_FILE, "r") as file:
        for line in file:
            instrument_name = line.strip() + "P"  #appending P for Call to the name
            query_instrument_name = {"instrument_name": instrument_name}

            weekly_put_totals = extract_put_totals(instrument_name, JUNE_LVT_WEEKLY_CSV_FILE)
            monthly_put_totals = extract_put_totals(instrument_name, JUNE_LVT_MONTHLY_CSV_FILE)
            put_options.append((instrument_name, weekly_put_totals, monthly_put_totals))

    june_sorted_put_options = sorted(put_options, key=lambda x: (x[2], x[1]), reverse=True)

    for option in june_sorted_put_options:
        print(f"Instrument Name: {option[0]}")
        print(f"WEEKLY PUT TOTALS: {int(option[1])}")
        print(f"MONTHLY PUT TOTALS: {int(option[2])}")
    return june_sorted_put_options

def september_call_table():
    call_options = []
    with open(SEPTEMBER_STRIKES_FILE, "r") as file:
        for line in file:
            instrument_name = line.strip() + "C"  #appending P for Call to the name
            query_instrument_name = {"instrument_name": instrument_name}

            weekly_call_totals = extract_call_totals(instrument_name, SEPTEMBER_LVT_WEEKLY_CSV_FILE)
            monthly_call_totals = extract_call_totals(instrument_name, SEPTEMBER_LVT_MONTHLY_CSV_FILE)
            call_options.append((instrument_name, weekly_call_totals, monthly_call_totals))

    september_sorted_call_options = sorted(call_options, key=lambda x: (x[2], x[1]), reverse=True)

    for option in september_sorted_call_options:
        print(f"Instrument Name: {option[0]}")
        print(f"WEEKLY CALL TOTALS: {int(option[1])}")
        print(f"MONTHLY CALL TOTALS: {int(option[2])}")
    return september_sorted_call_options

def september_put_table():
    put_options = []
    with open(SEPTEMBER_STRIKES_FILE, "r") as file:
        for line in file:
            instrument_name = line.strip()
            query_instrument_name = {"instrument_name": instrument_name}

            weekly_put_totals = extract_put_totals(instrument_name, SEPTEMBER_LVT_WEEKLY_CSV_FILE)
            monthly_put_totals = extract_put_totals(instrument_name, SEPTEMBER_LVT_MONTHLY_CSV_FILE)
            put_options.append((instrument_name, weekly_put_totals, monthly_put_totals))

    september_sorted_put_options = sorted(put_options, key=lambda x: (x[2], x[1]), reverse=True)

    for option in september_sorted_put_options:
        print(f"Instrument Name: {option[0]}")
        print(f"WEEKLY PUT TOTALS: {int(option[1])}")
        print(f"MONTHLY PUT TOTALS: {int(option[2])}")
    return september_sorted_put_options

@app.route('/blocked-bets')
def push_web():
    march_calls = march_call_table()
    march_puts = march_put_table()
    march_pc_ratio = put_call_ratio(march_calls, march_puts)
    june_calls = june_call_table()
    june_puts = june_put_table()
    june_pc_ratio = put_call_ratio(june_calls, june_puts)
    sep_calls = september_call_table()
    sep_puts = september_put_table()
    sep_pc_ratio = put_call_ratio(sep_calls, sep_puts)
    return render_template('table.html', data_call_march=march_calls, data_put_march=march_puts, data_march_pc_ratio=march_pc_ratio, data_call_june=june_calls, data_put_june=june_puts, data_june_pc_ratio=june_pc_ratio, data_call_sep=sep_calls, data_put_sep=sep_puts, data_sep_pc_ratio=sep_pc_ratio)

if __name__ == '__main__':
    app.run(debug=True)
