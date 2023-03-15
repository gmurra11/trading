
# Use to access OTC Institutional Investors - Where are they placing their bets

import configparser
import requests
import pandas as pd
import csv
from get_strikes import get_strikes
from flask import Flask, render_template

print(__name__)

app = Flask(__name__)

# Data Directory
DIR = "/home/gmurray/REPO/trading/data"
# T-1
T1 = "/home/gmurray/REPO/trading/data/daily"
# T-7
T7 = "/home/gmurray/REPO/trading/data/weekly"

# They'll should only be x2 Expries, as weekly are closer to the current day.  I'm inetrested in 30-80 days out, or more specifically 45 - 60 days.
LESS_THAN_50_DAYS = "28APR23"
LESS_THAN_80_DAYS = "26MAY23"

# Files
LESS_THAN_50_DAYS_WEEKLY_CSV_FILE = f"{DIR}/LVT-WEEKLY-{LESS_THAN_50_DAYS}.csv"
LESS_THAN_50_DAYS_MONTHLY_CSV_FILE = f"{DIR}/LVT-MONTHLY-{LESS_THAN_50_DAYS}.csv"

LESS_THAN_80_DAYS_WEEKLY_CSV_FILE = f"{DIR}/LVT-WEEKLY-{LESS_THAN_80_DAYS}.csv"
LESS_THAN_80_DAYS_MONTHLY_CSV_FILE = f"{DIR}/LVT-MONTHLY-{LESS_THAN_80_DAYS}.csv"

# T-1 Files (From Daily)
LESS_THAN_50_DAYS_WEEKLY_CSV_FILE_T1 = f"{T1}/LVT-WEEKLY-{LESS_THAN_50_DAYS}.csv"
LESS_THAN_50_DAYS_MONTHLY_CSV_FILE_T1 = f"{T1}/LVT-MONTHLY-{LESS_THAN_50_DAYS}.csv"

LESS_THAN_80_DAYS_WEEKLY_CSV_FILE_T1 = f"{T1}/LVT-WEEKLY-{LESS_THAN_80_DAYS}.csv"
LESS_THAN_80_DAYS_MONTHLY_CSV_FILE_T1 = f"{T1}/LVT-MONTHLY-{LESS_THAN_80_DAYS}.csv"

# T-7 Files (From Weekly)
LESS_THAN_50_DAYS_WEEKLY_CSV_FILE_T7 = f"{T7}/LVT-WEEKLY-{LESS_THAN_50_DAYS}.csv"
LESS_THAN_50_DAYS_MONTHLY_CSV_FILE_T7 = f"{T7}/LVT-MONTHLY-{LESS_THAN_50_DAYS}.csv"

LESS_THAN_80_DAYS_WEEKLY_CSV_FILE_T7 = f"{T7}/LVT-WEEKLY-{LESS_THAN_80_DAYS}.csv"
LESS_THAN_80_DAYS_MONTHLY_CSV_FILE_T7 = f"{T7}/LVT-MONTHLY-{LESS_THAN_80_DAYS}.csv"

# Read the configuration file
config = configparser.ConfigParser()
config.read('/home/gmurray/REPO/trading/config.ini')

client_id = config['DEFAULT']['client_id']
client_secret = config['DEFAULT']['client_secret']

def get_diff(current, new_value):
    current_value = current
    diff = current_value - new_value
    if diff > 0:
        return '+' + str(round(diff, 2))
    elif diff < 0:
        return str(round(diff, 2))
    else:
        return '0'

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
                non_blocked_calls_buy = abs(int(row["Calls Buy"]))
                non_blocked_calls_sell = abs(int(row["Calls Sell"]))
                blocked_calls_buy = abs(int(row["Call Buy Blocked"]))
                blocked_calls_sell = abs(int(row["Call Sell Blocked"]))
                calls_total = non_blocked_calls_buy + non_blocked_calls_sell + blocked_calls_buy + blocked_calls_sell
                return calls_total


def extract_put_totals(instrument_name, csv_file):

    strike = instrument_name.split('-')[2]

    # Read the csv file and find the corresponding strike
    with open(csv_file, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            if row["Strike"] == strike:
                non_blocked_puts_buy = 0
                if row["Puts Buy"] and row["Puts Buy"] != "":
                    non_blocked_puts_buy = abs(int(row["Puts Buy"]))

                non_blocked_puts_sell = 0
                if row["Puts Sell"] and row["Puts Sell"] != "":
                    non_blocked_puts_sell = abs(int(row["Puts Sell"]))

                non_blocked_puts_buy = 0
                if row["Put Buy Blocked"] and row["Put Buy Blocked"] != "":
                    blocked_puts_buy = abs(int(row["Put Buy Blocked"]))

                blocked_puts_sell = 0
                if row["Put Sell Blocked"] and row["Put Sell Blocked"] != "":
                    blocked_puts_sell = abs(int(row["Put Sell Blocked"]))

                puts_total = non_blocked_puts_buy + non_blocked_puts_sell + blocked_puts_buy + blocked_puts_sell

                return puts_total

def get_options_table(call_or_put, btc_or_eth, min_days, max_days, min_strike, max_strike, weekly_csv_file, monthly_csv_file, weekly_csv_file_t1, monthly_csv_file_t1, weekly_csv_file_t7, monthly_csv_file_t7):
    options = []
    options_t1 = []
    options_t7 = []

    eth_strikes = get_strikes(btc_or_eth, min_days, max_days, min_strike, max_strike)

    for instrument_name in eth_strikes:

        option_type = instrument_name[-1]

        if option_type == call_or_put:
            weekly_totals = extract_call_totals(instrument_name, weekly_csv_file) if option_type == "C" else extract_put_totals(instrument_name, weekly_csv_file)
            monthly_totals = extract_call_totals(instrument_name, monthly_csv_file) if option_type == "C" else extract_put_totals(instrument_name, monthly_csv_file)
            weekly_totals_t1 = extract_call_totals(instrument_name, weekly_csv_file_t1) if option_type == "C" else extract_put_totals(instrument_name, weekly_csv_file_t1)
            monthly_totals_t1 = extract_call_totals(instrument_name, monthly_csv_file_t1) if option_type == "C" else extract_put_totals(instrument_name, monthly_csv_file_t1)
            weekly_totals_t7 = extract_call_totals(instrument_name, weekly_csv_file_t7) if option_type == "C" else extract_put_totals(instrument_name, weekly_csv_file_t7)
            monthly_totals_t7 = extract_call_totals(instrument_name, monthly_csv_file_t7) if option_type == "C" else extract_put_totals(instrument_name, monthly_csv_file_t7)

            options.append((instrument_name, weekly_totals, monthly_totals))
            options_t1.append((instrument_name, weekly_totals_t1, monthly_totals_t1))
            options_t7.append((instrument_name, weekly_totals_t7, monthly_totals_t7))

    options_diff = []
    for opt, opt_t1, opt_t7 in zip(options, options_t1, options_t7):
        #setting the current or live directory ./ files to 0 if a None value is found, otherwise it breaks the caulcation
        opt_1 = opt[1] if opt[1] else 0
        opt_2 = opt[2] if opt[2] else 0
        weekly_diff_t1 = 0 if opt_t1[1] is None or opt_t1[1] == 0 else get_diff(opt_1, opt_t1[1])
        monthly_diff_t1 = 0 if opt_t1[2] is None or opt_t1[2] == 0 else get_diff(opt_2, opt_t1[2])
        weekly_diff_t7 = 0 if opt_t7[1] is None or opt_t7[1] == 0 else get_diff(opt_1, opt_t7[1])
        monthly_diff_t7 = 0 if opt_t7[2] is None or opt_t7[2] == 0 else get_diff(opt_2, opt_t7[2])
        options_diff.append((opt[0], opt_1, opt_2, weekly_diff_t1, monthly_diff_t1, weekly_diff_t7, monthly_diff_t7))

    sorted_options = sorted(options_diff, key=lambda x: (x[2], x[1]), reverse=True)
    return sorted_options[:10]

less_than_50_days_call_table = get_options_table("C", "ETH", 30, 50, 1000, 2500, LESS_THAN_50_DAYS_WEEKLY_CSV_FILE, LESS_THAN_50_DAYS_MONTHLY_CSV_FILE, LESS_THAN_50_DAYS_WEEKLY_CSV_FILE_T1, LESS_THAN_50_DAYS_MONTHLY_CSV_FILE_T1, LESS_THAN_50_DAYS_WEEKLY_CSV_FILE_T7, LESS_THAN_50_DAYS_MONTHLY_CSV_FILE_T7)
less_than_50_days_put_table = get_options_table("P", "ETH", 30, 50, 1000, 2500, LESS_THAN_50_DAYS_WEEKLY_CSV_FILE, LESS_THAN_50_DAYS_MONTHLY_CSV_FILE, LESS_THAN_50_DAYS_WEEKLY_CSV_FILE_T1, LESS_THAN_50_DAYS_MONTHLY_CSV_FILE_T1, LESS_THAN_50_DAYS_WEEKLY_CSV_FILE_T7, LESS_THAN_50_DAYS_MONTHLY_CSV_FILE_T7)
less_than_80_days_call_table = get_options_table("C", "ETH", 30, 50, 1000, 2500, LESS_THAN_80_DAYS_WEEKLY_CSV_FILE, LESS_THAN_80_DAYS_MONTHLY_CSV_FILE, LESS_THAN_80_DAYS_WEEKLY_CSV_FILE_T1, LESS_THAN_80_DAYS_MONTHLY_CSV_FILE_T1, LESS_THAN_80_DAYS_WEEKLY_CSV_FILE_T7, LESS_THAN_80_DAYS_MONTHLY_CSV_FILE_T7)
less_than_80_days_put_table = get_options_table("P", "ETH", 30, 50, 1000, 2500, LESS_THAN_80_DAYS_WEEKLY_CSV_FILE, LESS_THAN_80_DAYS_MONTHLY_CSV_FILE, LESS_THAN_80_DAYS_WEEKLY_CSV_FILE_T1, LESS_THAN_80_DAYS_MONTHLY_CSV_FILE_T1, LESS_THAN_80_DAYS_WEEKLY_CSV_FILE_T7, LESS_THAN_80_DAYS_MONTHLY_CSV_FILE_T7)


#print(less_than_50_days_put_table)

@app.route('/liquidity')
def push_web():
    less_than_50_days_calls = less_than_50_days_call_table
    less_than_50_days_puts = less_than_50_days_put_table
    less_than_50_days_pc_ratio = put_call_ratio(less_than_50_days_calls, less_than_50_days_puts)
    less_than_80_days_calls = less_than_80_days_call_table
    less_than_80_days_puts = less_than_80_days_put_table
    less_than_80_days_pc_ratio = put_call_ratio(less_than_80_days_calls, less_than_80_days_puts)
    return render_template('table.html', data_less_than_50_days_call=less_than_50_days_calls, data_less_than_50_days_puts=less_than_50_days_puts, data_less_than_50_days_pc_ratio=less_than_50_days_pc_ratio, data_less_than_80_days_calls=less_than_80_days_calls, data_less_than_80_days_puts=less_than_80_days_puts, data_less_than_80_days_pc_ratio=less_than_80_days_pc_ratio)

if __name__ == '__main__':
    app.run(debug=True, port=5010)
