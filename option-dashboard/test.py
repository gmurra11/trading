import csv

# Data Directory
DIR = "/home/gmurray/REPO/trading/data-skew"

# In Laevitas it's called "ETH Time Lapse Skew" under https://app.laevitas.ch/eth/deribit/options/volatility/iv
IV_CHANGE_SKEW_CSV = f"{DIR}/LVT-25DELTA-IV-CHANGE.csv"

def get_data(file_path):
    with open(file_path, 'r') as file:
        reader = csv.reader(file)
        headers = next(reader) # skip the header row
        for row in reader:
            if row[0] == '0.25':
                return row[1:]
        # If the desired row is not found, return a default value
        return [0, 0, 0, 0]

def add_percentages(data):
    today = float(data[0])
    yesterday = float(data[1])
    one_week_ago = float(data[2])
    one_month_ago = float(data[3])
    today_percent = 0
    yesterday_percent = round((today - yesterday) / yesterday * 100, 1)
    one_week_ago_percent = round((today - one_week_ago) / one_week_ago * 100, 1)
    one_month_ago_percent = round((today - one_month_ago) / one_month_ago * 100, 1)
    return [yesterday_percent, one_week_ago_percent, one_month_ago_percent]

get_delta25_row = get_data(IV_CHANGE_SKEW_CSV)
percentage_diff_changes = add_percentages(get_delta25_row)
if percentage_diff_changes:
    iv_change_delta25_list = get_delta25_row + percentage_diff_changes
    print(iv_change_delta25_list)
else:
    print("Desired row not found")
