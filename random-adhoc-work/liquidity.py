import csv

options_file = "March-Q1-Options.txt"
csv_file = "LVT-WEEKLY-31MAR23.csv"

def extract_call_totals(options_file, csv_file):
    strike_list = []

    # Read the options file and extract the strike
    with open(options_file, 'r') as f:
        for line in f:
            strike = line.split('-')[2]
            strike_list.append(strike)

    # Read the csv file and find the corresponding strike
    call_totals = []
    with open(csv_file, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            if row["Strike"] in strike_list:
                strike = row["Strike"]
                calls_buy = abs(int(row["Calls Buy"]))
                calls_sell = abs(int(row["Calls Sell"]))
                calls_total = calls_buy + calls_sell
                call_totals.append((calls_total))
    return call_totals

print(extract_call_totals(options_file, csv_file))
