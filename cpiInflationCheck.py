import csv, json, requests, configparser
from bs4 import BeautifulSoup, Tag
#from deribitMarketOrder import place_market_order_buy, get_access_token

# Read the configuration file
config = configparser.ConfigParser()
config.read('config.ini')

#client_id = config['DEFAULT']['client_id']
#client_secret = config['DEFAULT']['client_secret']

#access_token = get_access_token(client_id, client_secret)

def get_inflation_data(url, find):
    response = requests.get(url)
    contents = response.content
    soup = BeautifulSoup(contents, 'html.parser')
    inflation_data = soup.find('td', headers=find)
    return inflation_data.find('span', class_='datavalue')

def get_float(data):
    if isinstance(data, Tag):
        return float(data.text)
    return 0

def compare_inflation(last_month, today):
    status = ""
    if today < last_month:
        print('Inflation print lower  --> GO LONG')
        status = "LOWER"
    elif today == last_month:
        print('Inflation print match --> JUDGEMENT POSSIBLE SHORT')
        status = "MATCH"
    else:
        print('Inflation print higher--> GO SHORT')
        status = "HIGHER"
    return status

def compare_market_expectation(market_expectation, today):
    if today < market_expectation:
        print('Inflation print lower --> GO LONG')
    elif today == market_expectation:
        print('Inflation print match  --> JUDGEMENT POSSIBLE SHORT')
    else:
        print('Inflation print higher --> GO SHORT')

# SET DATE
last_month_date = "12132022"

cpi_url = 'https://www.bls.gov/news.release/cpi.nr0.htm'
cpi_url_last_month = 'https://www.bls.gov/news.release/archives/cpi_' + last_month_date + '.htm'

m_on_m_last_month = get_inflation_data(cpi_url, "cpi_pressa.r.1.3 cpi_pressa.h.1.2 cpi_pressa.h.2.7")
m_on_m_today = get_inflation_data(cpi_url, "cpi_pressa.r.1.3 cpi_pressa.h.1.2 cpi_pressa.h.2.8")
m_on_m_market_expectation = 0.3

m_on_m_last_month_decimal = get_float(m_on_m_last_month)
m_on_m_today_decimal = get_float(m_on_m_today)

y_on_y_last_month = get_inflation_data(cpi_url_last_month, "cpi_pressa.r.1.3 cpi_pressa.h.1.9")
y_on_y_today = get_inflation_data(cpi_url, "cpi_pressa.r.1.3 cpi_pressa.h.1.9")
y_on_y_market_expectation = 5.7

y_on_y_last_month_decimal = get_float(y_on_y_last_month)
y_on_y_today_decimal = get_float(y_on_y_today)

m_market_order_decision = compare_inflation(m_on_m_last_month_decimal, m_on_m_today_decimal)
y_market_order_decision = compare_inflation(y_on_y_last_month_decimal, y_on_y_today_decimal)


#MARKET ORDER DECISION TREE
#if m_market_order_decision == "LOWER" and y_market_order_decision == "LOWER" or y_market_order_decision == "MATCH":
#    place_market_order_buy("ETH_USDC-PERPETUAL", 0.01, "cpi_market_order", access_token)
#elif m_market_order_decision == "MATCH" and y_market_order_decision == "LOWER":
#    place_market_order_buy("ETH_USDC-PERPETUAL", 0.01, "cpi_market_order", access_token)
#elif m_market_order_decision == "MATCH" and y_market_order_decision == "MATCH" or y_market_order_decision == "HIGHER":
#    place_market_order_sell("ETH_USDC-PERPETUAL", 0.01, "cpi_market_order", access_token)
#else:
#    place_market_order_sell("ETH_USDC-PERPETUAL", 0.01, "cpi_market_order", access_token)

print("\nm on m print")
print("Market Expectation: " + str(m_on_m_market_expectation))
print("Today's: " + m_on_m_today.text)
compare_market_expectation(m_on_m_market_expectation, m_on_m_today_decimal)

print("\ny on y print")
print("==============")

print("Market Expectation: " + str(y_on_y_market_expectation))
print("Today's: " + y_on_y_today.text)
compare_market_expectation(y_on_y_market_expectation, y_on_y_today_decimal)

print("\nm on m Print")
print("==============")
print("Last Month: " + m_on_m_last_month.text)
print("Today's: " + m_on_m_today.text)

print("\ny on y Print")
print("==============")
print("Last Month: " + y_on_y_last_month.text)
print("Today's: " + y_on_y_today.text)
