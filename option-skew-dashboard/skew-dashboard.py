import pandas as pd
from datetime import datetime, timedelta
import csv
from flask import Flask, render_template

app = Flask(__name__)

# Data Directory
DIR = "/home/gmurray/REPO/trading/data-skew"
# T-1
T1 = "/home/gmurray/REPO/trading/data-skew/daily"
# T-7
#T7 = "/home/gmurray/REPO/trading/data-skew/weekly"

SKEW25_CURRENT_ETH = f"{DIR}/LVT-SKEW25-1D-ETH.csv"
SKEW25_T1_ETH = f"{T1}/LVT-SKEW25-1D-ETH.csv" #Note using 1D from yesterday as a comparison.  Ie: from an older file found in daily
SKEW25_T7_ETH = f"{DIR}/LVT-SKEW25-1W-ETH.csv"
SKEW25_T30_ETH = f"{DIR}/LVT-SKEW25-1M-ETH.csv"
SKEW25_CURRENT_BTC = f"{DIR}/LVT-SKEW25-1D-BTC.csv"
SKEW25_T1_BTC = f"{T1}/LVT-SKEW25-1D-BTC.csv" #Note using 1D from yesterday as a comparison.  Ie: from an older file found in daily
SKEW25_T7_BTC = f"{DIR}/LVT-SKEW25-1W-BTC.csv"
SKEW25_T30_BTC = f"{DIR}/LVT-SKEW25-1M-BTC.csv"
MULTI_EXPIRY_SKEW_ETH = f"{DIR}/LVT-MULTI-EXPIRY-SKEW-ETH.csv"
MULTI_EXPIRY_SKEW_BTC = f"{DIR}/LVT-MULTI-EXPIRY-SKEW-BTC.csv"
# In Laevitas it's called "ETH Time Lapse Skew" under https://app.laevitas.ch/eth/deribit/options/volatility/iv
ETH_IV_CHANGE_SKEW_CSV = f"{DIR}/LVT-ETH-25DELTA-IV-CHANGE.csv"
BTC_IV_CHANGE_SKEW_CSV = f"{DIR}/LVT-BTC-25DELTA-IV-CHANGE.csv"
#Used for Volatility Carry Spread
ETH_VOL_CARRY_SPREAD = f"{DIR}/LVT-ETH-VOLATILITY-CARRY-SPREAD.csv"
BTC_VOL_CARRY_SPREAD = f"{DIR}/LVT-BTC-VOLATILITY-CARRY-SPREAD.csv"

# Quarterly Expiries
EXPIRY_1 = "30th June"
EXPIRY_2 = "29th September"
EXPIRY_3 = "29th December"
EXPIRY_4 = "29th March 2024"


#################### Shared function ###########################

def get_diff(current, new_value):
    current_value = current
    diff = current_value - new_value
    if diff > 0:
        return '+' + str(round(diff, 2))
    elif diff < 0:
        return str(round(diff, 2))
    else:
        return '0'

# ETH Delta 25 SKEW ##############################################

def get_average_skew(CSV_FILE):
    # Read the csv file into a pandas dataframe
    df = pd.read_csv(CSV_FILE)
    # Calculate the average of the "Skew 30 Days" column
    avg_skew = df['Skew 30 Days'].mean()
    return round(avg_skew, 1)

# ETH Values
avg_skew_eth = get_average_skew(SKEW25_CURRENT_ETH)
avg_skew_eth_t1 = get_average_skew(SKEW25_T1_ETH)
avg_skew_eth_t7 = get_average_skew(SKEW25_T7_ETH)
avg_skew_eth_t30 = get_average_skew(SKEW25_T30_ETH)

diff_eth_t1 = get_diff(avg_skew_eth, avg_skew_eth_t1)
diff_eth_t7 = get_diff(avg_skew_eth, avg_skew_eth_t7)
diff_eth_t30 = get_diff(avg_skew_eth, avg_skew_eth_t30)

#  BTC Values
avg_skew_btc = get_average_skew(SKEW25_CURRENT_BTC)
avg_skew_btc_t1 = get_average_skew(SKEW25_T1_BTC)
avg_skew_btc_t7 = get_average_skew(SKEW25_T7_BTC)
avg_skew_btc_t30 = get_average_skew(SKEW25_T30_BTC)

diff_btc_t1 = get_diff(avg_skew_btc, avg_skew_btc_t1)
diff_btc_t7 = get_diff(avg_skew_btc, avg_skew_btc_t7)
diff_btc_t30 = get_diff(avg_skew_btc, avg_skew_btc_t30)

# IV 25 DELTA CHANGES #####################################################################

def get_data(file_path):
    with open(file_path, 'r') as file:
        reader = csv.reader(file)
        headers = next(reader) # skip the header row
        for row in reader:
            if row[0] == '0.25':
                return row[1:]
        # If the desired row is not found, return a default value
        return [0, 0, 0, 0]

def add_25delta_iv_diff(data):
    today = float(data[0])
    yesterday = float(data[1])
    one_week_ago = float(data[2])
    one_month_ago = float(data[3])
    today_percent = 0
    yesterday_percent = get_diff(today, yesterday)
    one_week_ago_percent = get_diff(today, one_week_ago)
    one_month_ago_percent = get_diff(today, one_month_ago)
    return [yesterday_percent, one_week_ago_percent, one_month_ago_percent]

eth_get_delta25_row = get_data(ETH_IV_CHANGE_SKEW_CSV)
eth_diff_changes = add_25delta_iv_diff(eth_get_delta25_row)

btc_get_delta25_row = get_data(BTC_IV_CHANGE_SKEW_CSV)
btc_diff_changes = add_25delta_iv_diff(btc_get_delta25_row)

if eth_diff_changes:
    eth_iv_change_delta25_list = eth_get_delta25_row + eth_diff_changes
    print(eth_iv_change_delta25_list)
else:
    print("Desired row not found")

if btc_diff_changes:
    btc_iv_change_delta25_list = btc_get_delta25_row + btc_diff_changes
    print(btc_iv_change_delta25_list)
else:
    print("Desired row not found")

##############################################################################################

# MLTI-EXPIRY SKEW

def add_multi_expiry_diff(data):
    q1_iv = float(data[0])
    q2_iv = float(data[1])
    q3_iv = float(data[2])
    q4_iv = float(data[3])
    diff_with_q1_vs_q2 = get_diff(q1_iv, q2_iv)
    diff_with_q1_vs_q3 = get_diff(q1_iv, q3_iv)
    diff_with_q1_vs_q4 = get_diff(q1_iv, q4_iv)
    return [diff_with_q1_vs_q2, diff_with_q1_vs_q3, diff_with_q1_vs_q4]

eth_multi_expiry_delta25_row = get_data(MULTI_EXPIRY_SKEW_ETH)
eth_multi_expiry_diff_changes = add_multi_expiry_diff(eth_multi_expiry_delta25_row)

btc_multi_expiry_delta25_row = get_data(MULTI_EXPIRY_SKEW_BTC)
btc_multi_expiry_diff_changes = add_multi_expiry_diff(btc_multi_expiry_delta25_row)

############################ Pass to webpage ###################################################

# Volatility Carry - IV - RV (Realized Vol) = spread.   Last 24 hrs spread vs historical.

ETH_MIN_SPREAD = "-93.58"
ETH_MAX_SPREAD = "58.18"
BTC_MIN_SPREAD = "-66.65"
BTC_MAX_SPREAD = "59.58"

def get_carry_spread(CSV_FILE):
    # Read the csv file into a pandas dataframe
    df = pd.read_csv(CSV_FILE)

    # Convert the DateTime column to a datetime object
    df['DateTime'] = pd.to_datetime(df['DateTime'])

    # Filter the dataframe to only include the last 24 hours of data
    end_time = datetime.now()
    start_time = end_time - timedelta(hours=24)
    df = df[df['DateTime'] >= start_time]

    # Calculate the average of the "Spread" column
    today_spread = df['Spread'].mean()

    return round(today_spread, 1)

eth_today_spread = get_carry_spread(ETH_VOL_CARRY_SPREAD)
btc_today_spread = get_carry_spread(BTC_VOL_CARRY_SPREAD)

################################################################################################

@app.route('/skew-dashboard')
def push_web():
    return render_template('table.html', data_avg_skew_eth=avg_skew_eth,
                                        data_avg_skew_eth_t1=avg_skew_eth_t1,
                                        data_avg_skew_eth_t7=avg_skew_eth_t7,
                                        data_avg_skew_eth_t30=avg_skew_eth_t30,
                                        data_diff_eth_t1=diff_eth_t1,
                                        data_diff_eth_t7=diff_eth_t7,
                                        data_diff_eth_t30=diff_eth_t30,
                                        data_avg_skew_btc=avg_skew_btc,
                                        data_avg_skew_btc_t1=avg_skew_btc_t1,
                                        data_avg_skew_btc_t7=avg_skew_btc_t7,
                                        data_avg_skew_btc_t30=avg_skew_btc_t30,
                                        data_diff_btc_t1=diff_btc_t1,
                                        data_diff_btc_t7=diff_btc_t7,
                                        data_diff_btc_t30=diff_btc_t30,
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
                                        data_multi_expiry_eth_q1_iv=eth_multi_expiry_delta25_row[0],
                                        data_multi_expiry_eth_q2_iv=eth_multi_expiry_delta25_row[1],
                                        data_multi_expiry_eth_q3_iv=eth_multi_expiry_delta25_row[2],
                                        data_multi_expiry_eth_q4_iv=eth_multi_expiry_delta25_row[3],
                                        data_multi_expiry_eth_q2_iv_diff=eth_multi_expiry_diff_changes[0],
                                        data_multi_expiry_eth_q3_iv_diff=eth_multi_expiry_diff_changes[1],
                                        data_multi_expiry_eth_q4_iv_diff=eth_multi_expiry_diff_changes[2],
                                        data_multi_expiry_btc_q1_iv=btc_multi_expiry_delta25_row[0],
                                        data_multi_expiry_btc_q2_iv=btc_multi_expiry_delta25_row[1],
                                        data_multi_expiry_btc_q3_iv=btc_multi_expiry_delta25_row[2],
                                        data_multi_expiry_btc_q4_iv=btc_multi_expiry_delta25_row[3],
                                        data_multi_expiry_btc_q2_iv_diff=btc_multi_expiry_diff_changes[0],
                                        data_multi_expiry_btc_q3_iv_diff=btc_multi_expiry_diff_changes[1],
                                        data_multi_expiry_btc_q4_iv_diff=btc_multi_expiry_diff_changes[2],
                                        data_eth_today_spread=eth_today_spread,
                                        data_eth_min_spread=ETH_MIN_SPREAD,
                                        data_eth_max_spread=ETH_MAX_SPREAD,
                                        data_btc_today_spread=btc_today_spread,
                                        data_btc_min_spread=BTC_MIN_SPREAD,
                                        data_btc_max_spread=BTC_MAX_SPREAD,
                                        data_q1_label=EXPIRY_1,
                                        data_q2_label=EXPIRY_2,
                                        data_q3_label=EXPIRY_3,
                                        data_q4_label=EXPIRY_4
                                        )

if __name__ == '__main__':
    app.run(debug=True, port=5005)
