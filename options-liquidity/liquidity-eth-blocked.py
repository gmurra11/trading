# Use to access OTC Institutional Investors - Where are they placing their bets

import configparser
import requests
import pandas as pd
import csv
from get_strikes import get_strikes
from liquidity_functions import get_options_table, put_call_ratio
from flask import Flask, render_template

# Data Directory
DIR = "/home/gmurray/REPO/trading/data"
# T-1
T1 = "/home/gmurray/REPO/trading/data/daily"
# T-7
T7 = "/home/gmurray/REPO/trading/data/weekly"

# They'll should only be x2 Expries, as weekly are closer to the current day.  I'm inetrested in 30-80 days out, or more specifically 45 - 60 days.
LESS_THAN_50_DAYS = "28APR23"
LESS_THAN_80_DAYS = "26MAY23"
CURRENCY = "ETH"
MIN_STRIKE = 1000
MAX_STRIKE = 2500
is_blocked = True

# Files
LESS_THAN_50_DAYS_WEEKLY_CSV_FILE = f"{DIR}/LVT-WEEKLY-{LESS_THAN_50_DAYS}-{CURRENCY}.csv"
LESS_THAN_50_DAYS_MONTHLY_CSV_FILE = f"{DIR}/LVT-MONTHLY-{LESS_THAN_50_DAYS}-{CURRENCY}.csv"

LESS_THAN_80_DAYS_WEEKLY_CSV_FILE = f"{DIR}/LVT-WEEKLY-{LESS_THAN_80_DAYS}-{CURRENCY}.csv"
LESS_THAN_80_DAYS_MONTHLY_CSV_FILE = f"{DIR}/LVT-MONTHLY-{LESS_THAN_80_DAYS}-{CURRENCY}.csv"

# T-1 Files (From Daily)
LESS_THAN_50_DAYS_WEEKLY_CSV_FILE_T1 = f"{T1}/LVT-WEEKLY-{LESS_THAN_50_DAYS}-{CURRENCY}.csv"
LESS_THAN_50_DAYS_MONTHLY_CSV_FILE_T1 = f"{T1}/LVT-MONTHLY-{LESS_THAN_50_DAYS}-{CURRENCY}.csv"

LESS_THAN_80_DAYS_WEEKLY_CSV_FILE_T1 = f"{T1}/LVT-WEEKLY-{LESS_THAN_80_DAYS}-{CURRENCY}.csv"
LESS_THAN_80_DAYS_MONTHLY_CSV_FILE_T1 = f"{T1}/LVT-MONTHLY-{LESS_THAN_80_DAYS}-{CURRENCY}.csv"

# T-7 Files (From Weekly)
LESS_THAN_50_DAYS_WEEKLY_CSV_FILE_T7 = f"{T7}/LVT-WEEKLY-{LESS_THAN_50_DAYS}-{CURRENCY}.csv"
LESS_THAN_50_DAYS_MONTHLY_CSV_FILE_T7 = f"{T7}/LVT-MONTHLY-{LESS_THAN_50_DAYS}-{CURRENCY}.csv"

LESS_THAN_80_DAYS_WEEKLY_CSV_FILE_T7 = f"{T7}/LVT-WEEKLY-{LESS_THAN_80_DAYS}-{CURRENCY}.csv"
LESS_THAN_80_DAYS_MONTHLY_CSV_FILE_T7 = f"{T7}/LVT-MONTHLY-{LESS_THAN_80_DAYS}-{CURRENCY}.csv"

app = Flask(__name__)

less_than_50_days_call_table = get_options_table("C", CURRENCY, 30, 50, MIN_STRIKE, MAX_STRIKE, LESS_THAN_50_DAYS_WEEKLY_CSV_FILE, LESS_THAN_50_DAYS_MONTHLY_CSV_FILE, LESS_THAN_50_DAYS_WEEKLY_CSV_FILE_T1, LESS_THAN_50_DAYS_MONTHLY_CSV_FILE_T1, LESS_THAN_50_DAYS_WEEKLY_CSV_FILE_T7, LESS_THAN_50_DAYS_MONTHLY_CSV_FILE_T7, is_blocked)
less_than_50_days_put_table = get_options_table("P", CURRENCY, 30, 50, MIN_STRIKE, MAX_STRIKE, LESS_THAN_50_DAYS_WEEKLY_CSV_FILE, LESS_THAN_50_DAYS_MONTHLY_CSV_FILE, LESS_THAN_50_DAYS_WEEKLY_CSV_FILE_T1, LESS_THAN_50_DAYS_MONTHLY_CSV_FILE_T1, LESS_THAN_50_DAYS_WEEKLY_CSV_FILE_T7, LESS_THAN_50_DAYS_MONTHLY_CSV_FILE_T7, is_blocked)
less_than_80_days_call_table = get_options_table("C", CURRENCY, 50, 80, MIN_STRIKE, MAX_STRIKE, LESS_THAN_80_DAYS_WEEKLY_CSV_FILE, LESS_THAN_80_DAYS_MONTHLY_CSV_FILE, LESS_THAN_80_DAYS_WEEKLY_CSV_FILE_T1, LESS_THAN_80_DAYS_MONTHLY_CSV_FILE_T1, LESS_THAN_80_DAYS_WEEKLY_CSV_FILE_T7, LESS_THAN_80_DAYS_MONTHLY_CSV_FILE_T7, is_blocked)
less_than_80_days_put_table = get_options_table("P", CURRENCY, 50, 80, MIN_STRIKE, MAX_STRIKE, LESS_THAN_80_DAYS_WEEKLY_CSV_FILE, LESS_THAN_80_DAYS_MONTHLY_CSV_FILE, LESS_THAN_80_DAYS_WEEKLY_CSV_FILE_T1, LESS_THAN_80_DAYS_MONTHLY_CSV_FILE_T1, LESS_THAN_80_DAYS_WEEKLY_CSV_FILE_T7, LESS_THAN_80_DAYS_MONTHLY_CSV_FILE_T7, is_blocked)

#print(less_than_50_days_put_table)

@app.route('/liquidity-eth-blocked')
def push_web():
    less_than_50_days_calls = less_than_50_days_call_table
    less_than_50_days_puts = less_than_50_days_put_table
    less_than_50_days_pc_ratio = put_call_ratio(less_than_50_days_calls, less_than_50_days_puts)
    less_than_80_days_calls = less_than_80_days_call_table
    less_than_80_days_puts = less_than_80_days_put_table
    less_than_80_days_pc_ratio = put_call_ratio(less_than_80_days_calls, less_than_80_days_puts)
    return render_template('table.html', data_less_than_50_days_call=less_than_50_days_calls, data_less_than_50_days_puts=less_than_50_days_puts, data_less_than_50_days_pc_ratio=less_than_50_days_pc_ratio, data_less_than_80_days_calls=less_than_80_days_calls, data_less_than_80_days_puts=less_than_80_days_puts, data_less_than_80_days_pc_ratio=less_than_80_days_pc_ratio, data_currency=CURRENCY)

if __name__ == '__main__':
    app.run(debug=True, port=5014)
