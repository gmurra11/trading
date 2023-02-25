import pandas as pd
import csv
from flask import Flask, render_template

app = Flask(__name__)

# Data Directory
DIR = "/home/gmurray/REPO/trading/data-skew"
# T-1
T1 = "/home/gmurray/REPO/trading/data-skew/daily"
# T-7
#T7 = "/home/gmurray/REPO/trading/data-skew/weekly"

SKEW25_CURRENT = f"{DIR}/LVT-SKEW25-1D.csv"
SKEW25_T1 = f"{T1}/LVT-SKEW25-1D.csv" #Note using 1D from yesterday as a comparison.  Ie: from an older file found in daily
SKEW25_T7 = f"{DIR}/LVT-SKEW25-1W.csv"
SKEW25_T30 = f"{DIR}/LVT-SKEW25-1M.csv"
MULTI_EXPIRY_SKEW = f"{DIR}/MULTI-EXPIRY-SKEW.csv"

# Quarterly Expiries
Q1_EXPIRY = "31st March"
Q2_EXPIRY = "30th June"
Q3_EXPIRY = "29th September"

# ETH Delta 25 SKEW ##############################################

def get_average_skew(CSV_FILE):
    # Read the csv file into a pandas dataframe
    df = pd.read_csv(CSV_FILE)
    # Calculate the average of the "Skew 30 Days" column
    avg_skew = df['Skew 30 Days'].mean()
    return round(avg_skew, 1)

def get_skew_diff(avg_skew, skew_to_diff):
    current_skew = avg_skew
    # Calculate the percentage difference between the current value and T-?
    diff = (skew_to_diff - current_skew) / current_skew * 100
    return round(diff, 1)
    # Round the average skew value to one decimal place

avg_skew = get_average_skew(SKEW25_CURRENT)
avg_skew_t1 = get_average_skew(SKEW25_T1)
avg_skew_t7 = get_average_skew(SKEW25_T7)
avg_skew_t30 = get_average_skew(SKEW25_T30)

diff_t1 = get_skew_diff(avg_skew, avg_skew_t1)
diff_t7 = get_skew_diff(avg_skew, avg_skew_t7)
diff_t30 = get_skew_diff(avg_skew, avg_skew_t30)

# IV 25 DELTA CHANGES #####################################################################

# In Laevitas it's called "ETH Time Lapse Skew" under https://app.laevitas.ch/eth/deribit/options/volatility/iv
ETH_IV_CHANGE_SKEW_CSV = f"{DIR}/LVT-ETH-25DELTA-IV-CHANGE.csv"
BTC_IV_CHANGE_SKEW_CSV = f"{DIR}/LVT-BTC-25DELTA-IV-CHANGE.csv"

def get_data(file_path):
    with open(file_path, 'r') as file:
        reader = csv.reader(file)
        headers = next(reader) # skip the header row
        for row in reader:
            if row[0] == '0.25':
                return row[1:]
        # If the desired row is not found, return a default value
        return [0, 0, 0, 0]

def add_iv_percentages_diff(data):
    today = float(data[0])
    yesterday = float(data[1])
    one_week_ago = float(data[2])
    one_month_ago = float(data[3])
    today_percent = 0
    yesterday_percent = round((today - yesterday) / yesterday * 100, 1)
    one_week_ago_percent = round((today - one_week_ago) / one_week_ago * 100, 1)
    one_month_ago_percent = round((today - one_month_ago) / one_month_ago * 100, 1)
    return [yesterday_percent, one_week_ago_percent, one_month_ago_percent]

def add_multi_expiry_percentages_diff(data):
    q1_iv = float(data[0])
    q2_iv = float(data[1])
    q3_iv = float(data[2])
    diff_with_q1_vs_q2 = round((q1_iv - q2_iv) / q2_iv * 100, 1)
    diff_with_q1_vs_q3 = round((q1_iv - q3_iv) / q3_iv * 100, 1)
    return [diff_with_q1_vs_q2, diff_with_q1_vs_q3]

eth_get_delta25_row = get_data(ETH_IV_CHANGE_SKEW_CSV)
eth_percentage_diff_changes = add_iv_percentages_diff(eth_get_delta25_row)

btc_get_delta25_row = get_data(BTC_IV_CHANGE_SKEW_CSV)
btc_percentage_diff_changes = add_iv_percentages_diff(btc_get_delta25_row)

if eth_percentage_diff_changes:
    eth_iv_change_delta25_list = eth_get_delta25_row + eth_percentage_diff_changes
    print(eth_iv_change_delta25_list)
else:
    print("Desired row not found")

if btc_percentage_diff_changes:
    btc_iv_change_delta25_list = btc_get_delta25_row + btc_percentage_diff_changes
    print(btc_iv_change_delta25_list)
else:
    print("Desired row not found")

##############################################################################################

# MLTI-EXPIRY SKEW

eth_multi_expiry_delta25_row = get_data(MULTI_EXPIRY_SKEW)
eth_multi_expiry_percentage_diff_changes = add_multi_expiry_percentages_diff(eth_multi_expiry_delta25_row)


@app.route('/skew-dashboard')
def push_web():
    return render_template('table.html', data_avg_skew=avg_skew,
                                        data_avg_skew_t1=avg_skew_t1,
                                        data_avg_skew_t7=avg_skew_t7,
                                        data_avg_skew_t30=avg_skew_t30,
                                        data_diff_t1=diff_t1,
                                        data_diff_t7=diff_t7,
                                        data_diff_t30=diff_t30,
                                        data_eth_iv_today=eth_iv_change_delta25_list[0],
                                        data_eth_iv_yesterday=eth_iv_change_delta25_list[1],
                                        data_eth_iv_yesterday_chg=eth_iv_change_delta25_list[4],
                                        data_eth_iv_last_week=eth_iv_change_delta25_list[2],
                                        data_eth_iv_last_week_chg=eth_iv_change_delta25_list[5],
                                        data_eth_iv_last_month=eth_iv_change_delta25_list[3],
                                        data_eth_iv_last_month_chg=eth_iv_change_delta25_list[6],
                                        data_btc_iv_today=btc_iv_change_delta25_list[0],
                                        data_btc_iv_yesterday=btc_iv_change_delta25_list[1],
                                        data_btc_iv_yesterday_chg=btc_iv_change_delta25_list[4],
                                        data_btc_iv_last_week=btc_iv_change_delta25_list[2],
                                        data_btc_iv_last_week_chg=btc_iv_change_delta25_list[5],
                                        data_btc_iv_last_month=btc_iv_change_delta25_list[3],
                                        data_btc_iv_last_month_chg=btc_iv_change_delta25_list[6],
                                        data_multi_expiry_q1_iv=eth_multi_expiry_delta25_row[0],
                                        data_multi_expiry_q2_iv=eth_multi_expiry_delta25_row[1],
                                        data_multi_expiry_q3_iv=eth_multi_expiry_delta25_row[2],
                                        data_multi_expiry_q2_iv_diff=eth_multi_expiry_percentage_diff_changes[0],
                                        data_multi_expiry_q3_iv_diff=eth_multi_expiry_percentage_diff_changes[1],
                                        data_q1_label=Q1_EXPIRY,
                                        data_q2_label=Q2_EXPIRY,
                                        data_q3_label=Q3_EXPIRY
                                        )

if __name__ == '__main__':
    app.run(debug=True, port=5005)
