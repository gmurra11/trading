# Use to access OTC Institutional Investors - Where are they placing their bets

import configparser
import requests
import pandas as pd
import csv
from flask import Flask, render_template

app = Flask(__name__)

# Data Directory
DIR = "/home/gmurray/REPO/trading/data-weekly"
# T-1
T1 = "/home/gmurray/REPO/trading/data-weekly/daily"
# T-7
T7 = "/home/gmurray/REPO/trading/data-weekly/weekly"

# Files
NEXT_FRIDAY_STRIKES_FILE = f"{DIR}/Next-Fri-Options.txt"
NEXT_FRIDAY_LVT_WEEKLY_CSV_FILE = f"{DIR}/LVT-WEEKLY-24FEB23.csv"
NEXT_FRIDAY_LVT_MONTHLY_CSV_FILE = f"{DIR}/LVT-MONTHLY-24FEB23.csv"
FOLLOWING_FRIDAY_STRIKES_FILE = f"{DIR}/Following-Fri-Options.txt"
FOLLOWING_FRIDAY_LVT_WEEKLY_CSV_FILE = f"{DIR}/LVT-WEEKLY-03MAR23.csv"
FOLLOWING_FRIDAY_LVT_MONTHLY_CSV_FILE = f"{DIR}/LVT-MONTHLY-03MAR23.csv"
THIRD_FRIDAY_STRIKES_FILE = f"{DIR}/Next-Fri-Options.txt"
THIRD_FRIDAY_LVT_WEEKLY_CSV_FILE = f"{DIR}/LVT-WEEKLY-10MAR23.csv"
THIRD_FRIDAY_LVT_MONTHLY_CSV_FILE = f"{DIR}/LVT-MONTHLY-10MAR23.csv"

# T-1 Files (From Daily)
NEXT_FRIDAY_STRIKES_FILE_T1 = f"{T1}/Next-Fri-Options.txt"
NEXT_FRIDAY_LVT_WEEKLY_CSV_FILE_T1 = f"{T1}/LVT-WEEKLY-24FEB23.csv"
NEXT_FRIDAY_LVT_MONTHLY_CSV_FILE_T1 = f"{T1}/LVT-MONTHLY-24FEB23.csv"
FOLLOWING_FRIDAY_STRIKES_FILE_T1 = f"{T1}/Following-Fri-Options.txt"
FOLLOWING_FRIDAY_LVT_WEEKLY_CSV_FILE_T1 = f"{T1}/LVT-WEEKLY-03MAR23.csv"
FOLLOWING_FRIDAY_LVT_MONTHLY_CSV_FILE_T1 = f"{T1}/LVT-MONTHLY-03MAR23.csv"
THIRD_FRIDAY_STRIKES_FILE_T1 = f"{T1}/Next-Fri-Options.txt"
THIRD_FRIDAY_LVT_WEEKLY_CSV_FILE_T1 = f"{T1}/LVT-WEEKLY-10MAR23.csv"
THIRD_FRIDAY_LVT_MONTHLY_CSV_FILE_T1 = f"{T1}/LVT-MONTHLY-10MAR23.csv"

# T-7 Files (From Weekly)
NEXT_FRIDAY_STRIKES_FILE_T7 = f"{T7}/Next-Fri-Options.txt"
NEXT_FRIDAY_LVT_WEEKLY_CSV_FILE_T7 = f"{T7}/LVT-WEEKLY-24FEB23.csv"
NEXT_FRIDAY_LVT_MONTHLY_CSV_FILE_T7 = f"{T7}/LVT-MONTHLY-24FEB23.csv"
FOLLOWING_FRIDAY_STRIKES_FILE_T7 = f"{T7}/Following-Fri-Options.txt"
FOLLOWING_FRIDAY_LVT_WEEKLY_CSV_FILE_T7 = f"{T7}/LVT-WEEKLY-03MAR23.csv"
FOLLOWING_FRIDAY_LVT_MONTHLY_CSV_FILE_T7 = f"{T7}/LVT-MONTHLY-03MAR23.csv"
THIRD_FRIDAY_STRIKES_FILE_T7 = f"{T7}/Next-Fri-Options.txt"
THIRD_FRIDAY_LVT_WEEKLY_CSV_FILE_T7 = f"{T7}/LVT-WEEKLY-10MAR23.csv"
THIRD_FRIDAY_LVT_MONTHLY_CSV_FILE_T7 = f"{T7}/LVT-MONTHLY-10MAR23.csv"

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

def get_options_table(expiry, option_type, strikes_file, weekly_csv_file, monthly_csv_file, weekly_csv_file_t1, monthly_csv_file_t1, weekly_csv_file_t7, monthly_csv_file_t7):
    options = []
    options_t1 = []
    options_t7 = []
    with open(strikes_file, "r") as file:
        for line in file:
            instrument_name = line.strip() + option_type  #appending option type to the name
            query_instrument_name = {"instrument_name": instrument_name}

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
        weekly_diff_t1 = 0 if opt_t1[1] is None or opt_t1[1] == 0 else round((abs(opt_1 - opt_t1[1]) / opt_t1[1]) * 100, 2)
        monthly_diff_t1 = 0 if opt_t1[2] is None or opt_t1[2] == 0 else round((abs(opt_2 - opt_t1[2]) / opt_t1[2]) * 100, 2)
        weekly_diff_t7 = 0 if opt_t7[1] is None or opt_t7[1] == 0 else round((abs(opt_1 - opt_t7[1]) / opt_t7[1]) * 100, 2)
        monthly_diff_t7 = 0 if opt_t7[2] is None or opt_t7[2] == 0 else round((abs(opt_2 - opt_t7[2]) / opt_t7[2]) * 100, 2)
        options_diff.append((opt[0], opt_1, opt_2, weekly_diff_t1, monthly_diff_t1, weekly_diff_t7, monthly_diff_t7))

    sorted_options = sorted(options_diff, key=lambda x: (x[2], x[1]), reverse=True)

    for option in sorted_options:
        print(f"Instrument Name: {option[0]}")
        print(f"WEEKLY CALL TOTALS: {int(option[1])}")
        print(f"T1 WEEKLY % DIFFERENCE: {round(float(option[3]), 2)}")
        print(f"T7 WEEKLY % DIFFERENCE: {round(float(option[5]), 2)}")
        print(f"MONTHLY CALL TOTALS: {int(option[2])}")
        print(f"T1 MONTHLY % DIFFERENCE: {round(float(option[4]), 2)}")
        print(f"T7 MONTHLY % DIFFERENCE: {round(float(option[6]), 2)}")
    return sorted_options

next_friday_call_table = get_options_table("NEXT_FRIDAY", "C", NEXT_FRIDAY_STRIKES_FILE, NEXT_FRIDAY_LVT_WEEKLY_CSV_FILE, NEXT_FRIDAY_LVT_MONTHLY_CSV_FILE, NEXT_FRIDAY_LVT_WEEKLY_CSV_FILE_T1, NEXT_FRIDAY_LVT_MONTHLY_CSV_FILE_T1, NEXT_FRIDAY_LVT_WEEKLY_CSV_FILE_T7, NEXT_FRIDAY_LVT_MONTHLY_CSV_FILE_T7)
next_friday_put_table = get_options_table("NEXT_FRIDAY", "P", NEXT_FRIDAY_STRIKES_FILE, NEXT_FRIDAY_LVT_WEEKLY_CSV_FILE, NEXT_FRIDAY_LVT_MONTHLY_CSV_FILE, NEXT_FRIDAY_LVT_WEEKLY_CSV_FILE_T1, NEXT_FRIDAY_LVT_MONTHLY_CSV_FILE_T1, NEXT_FRIDAY_LVT_WEEKLY_CSV_FILE_T7, NEXT_FRIDAY_LVT_MONTHLY_CSV_FILE_T7)
following_friday_call_table = get_options_table("FOLLOWING_FRIDAY", "C", FOLLOWING_FRIDAY_STRIKES_FILE, FOLLOWING_FRIDAY_LVT_WEEKLY_CSV_FILE, FOLLOWING_FRIDAY_LVT_MONTHLY_CSV_FILE, FOLLOWING_FRIDAY_LVT_WEEKLY_CSV_FILE_T1, FOLLOWING_FRIDAY_LVT_MONTHLY_CSV_FILE_T1, FOLLOWING_FRIDAY_LVT_WEEKLY_CSV_FILE_T7, FOLLOWING_FRIDAY_LVT_MONTHLY_CSV_FILE_T7)
following_friday_put_table = get_options_table("FOLLOWING_FRIDAY", "P", FOLLOWING_FRIDAY_STRIKES_FILE, FOLLOWING_FRIDAY_LVT_WEEKLY_CSV_FILE, FOLLOWING_FRIDAY_LVT_MONTHLY_CSV_FILE, FOLLOWING_FRIDAY_LVT_WEEKLY_CSV_FILE_T1, FOLLOWING_FRIDAY_LVT_MONTHLY_CSV_FILE_T1, FOLLOWING_FRIDAY_LVT_WEEKLY_CSV_FILE_T7, FOLLOWING_FRIDAY_LVT_MONTHLY_CSV_FILE_T7)
third_friday_call_table = get_options_table("THIRD_FRIDAY", "C", THIRD_FRIDAY_STRIKES_FILE, THIRD_FRIDAY_LVT_WEEKLY_CSV_FILE, THIRD_FRIDAY_LVT_MONTHLY_CSV_FILE, THIRD_FRIDAY_LVT_WEEKLY_CSV_FILE_T1, THIRD_FRIDAY_LVT_MONTHLY_CSV_FILE_T1, THIRD_FRIDAY_LVT_WEEKLY_CSV_FILE_T7, THIRD_FRIDAY_LVT_MONTHLY_CSV_FILE_T7)
third_friday_put_table = get_options_table("THIRD_FRIDAY", "P", THIRD_FRIDAY_STRIKES_FILE, THIRD_FRIDAY_LVT_WEEKLY_CSV_FILE, THIRD_FRIDAY_LVT_MONTHLY_CSV_FILE, THIRD_FRIDAY_LVT_WEEKLY_CSV_FILE_T1, THIRD_FRIDAY_LVT_MONTHLY_CSV_FILE_T1, THIRD_FRIDAY_LVT_WEEKLY_CSV_FILE_T7, THIRD_FRIDAY_LVT_MONTHLY_CSV_FILE_T7)

@app.route('/blocked-bets-weekly-options')
def push_web():
    next_friday_calls = next_friday_call_table
    next_friday_puts = next_friday_put_table
    next_friday_pc_ratio = put_call_ratio(next_friday_calls, next_friday_puts)
    following_friday_calls = following_friday_call_table
    following_friday_puts = following_friday_put_table
    following_friday_pc_ratio = put_call_ratio(following_friday_calls, following_friday_puts)
    third_friday_calls = third_friday_call_table
    third_friday_puts = third_friday_put_table
    third_friday_pc_ratio = put_call_ratio(third_friday_calls, third_friday_puts)
    return render_template('table.html', data_call_next_friday=next_friday_calls, data_put_next_friday=next_friday_puts, data_next_friday_pc_ratio=next_friday_pc_ratio, data_call_following_friday=following_friday_calls, data_put_following_friday=following_friday_puts, data_following_friday_pc_ratio=following_friday_pc_ratio, data_call_third_friday=third_friday_calls, data_put_third_friday=third_friday_puts, data_third_friday_pc_ratio=third_friday_pc_ratio)

if __name__ == '__main__':
    app.run(debug=True, port=5002)
