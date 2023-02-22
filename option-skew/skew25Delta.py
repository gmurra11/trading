import pandas as pd
from flask import Flask, render_template

app = Flask(__name__)

# Data Directory
DIR = "/home/gmurray/REPO/trading/data-skew"
# T-1
T1 = "/home/gmurray/REPO/trading/data-skew/daily"
# T-7
T7 = "/home/gmurray/REPO/trading/data-skew/weekly"

SKEW25_CURRENT = f"{DIR}/LVT-SKEW25.csv"
SKEW25_T1 = f"{T1}/LVT-SKEW25.csv"
SKEW25_T7 = f"{T7}/LVT-SKEW25.csv"

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
#avg_skew = round(avg_skew, 1)
avg_skew = get_average_skew(SKEW25_CURRENT)
avg_skew_t1 = get_average_skew(SKEW25_T1)
avg_skew_t7 = get_average_skew(SKEW25_T7)

diff_t1 = get_skew_diff(avg_skew, avg_skew_t1)
diff_t7 = get_skew_diff(avg_skew, avg_skew_t7)

@app.route('/delta-25-skew')
def push_web():
    return render_template('table.html', data_avg_skew=avg_skew, data_avg_skew_t1=avg_skew_t1, data_avg_skew_t7=avg_skew_t7, data_diff_t1=diff_t1, data_diff_t7=diff_t7)

if __name__ == '__main__':
    app.run(debug=True, port=5005)
