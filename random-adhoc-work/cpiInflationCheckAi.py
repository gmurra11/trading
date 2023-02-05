import csv, json, configparser
from bs4 import BeautifulSoup, Tag
from deribitMarketOrder import get_access_token
import aiohttp
import asyncio
import threading

# Read the configuration file
config = configparser.ConfigParser()
config.read('config.ini')

client_id = config['DEFAULT']['client_id']
client_secret = config['DEFAULT']['client_secret']

access_token = get_access_token(client_id, client_secret)

async def get_inflation_data(url, find):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            contents = await response.text()
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
last_month_date = "11102022"

cpi_url = 'https://www.bls.gov/news.release/cpi.nr0.htm'
cpi_url_last_month = 'https://www.bls.gov/news.release/archives/cpi_' + last_month_date + '.htm'

async def main():
    m_on_m_last_month = await get_inflation_data(cpi_url, "cpi_pressa.r.1.3 cpi_pressa.h.1.2 cpi_pressa.h.2.7")
    m_on_m_today = await get_inflation_data(cpi_url, "cpi_pressa.r.1.3 cpi_pressa.h.1.2 cpi_pressa.h.2.8")
    m_on_m_market_expectation = 0.3

    m_on_m_last_month_decimal = get_float(m_on_m_last_month)
    m_on_m_today_decimal = get_float(m_on_m_today)

    y_on_y_last_month = await get_inflation_data(cpi_url_last_month, "cpi_pressa.r.1.3 cpi_pressa.h.1.9")
    y_on_y_today = await get_inflation_data(cpi_url, "cpi_pressa.r.1.3 cpi_pressa.h.1.9")
    y_on_y_market_expectation = 6.3

    y_on_y_last_month_decimal = get_float(y_on_y_last_month)
    y_on_y_today_decimal = get_float(y_on_y_today)

    m_market_order_decision = compare_inflation(m_on_m_last_month_decimal, m_on_m_today_decimal)
    y_market_order_decision = compare_inflation(y_on_y_last_month_decimal, y_on_y_today_decimal)

    #MARKET ORDER DECISION TREE
    if m_market_order_decision == "LOWER":
        if y_market_order_decision == "LOWER":
            print('BOTH MARKET ORDERS: LONG')
            thread1 = threading.Thread(target=place_market_order_buy)
            thread2 = threading.Thread(target=place_market_order_buy)
            thread1.start()
            thread2.start()
            thread1.join()
            thread2.join()
        elif y_market_order_decision == "MATCH":
            compare_market_expectation(y_on_y_market_expectation, y_on_y_today_decimal)
    elif m_market_order_decision == "MATCH":
        if y_market_order_decision == "LOWER":
            print('MONTH ON MONTH SHORT, YEAR ON YEAR LONG')
            thread1 = threading.Thread(target=place_market_order_sell)
            thread2 = threading.Thread(target=place_market_order_buy)
            thread1.start()
            thread2.start()
            thread1.join()
            thread2.join()
        elif y_market_order_decision == "MATCH":
            compare_market_expectation(m_on_m_market_expectation, m_on_m_today_decimal)
            compare_market_expectation(y_on_y_market_expectation, y_on_m_on_m_today_decimal = get_float(m_on_m_today)

    y_on_y_last_month = await get_inflation_data(cpi_url_last_month, "cpi_pressa.r.1.3 cpi_pressa.h.1.9")
    y_on_y_today = await get_inflation_data(cpi_url, "cpi_pressa.r.1.3 cpi_pressa.h.1.9")
    y_on_y_market_expectation = 6.3

    y_on_y_last_month_decimal = get_float(y_on_y_last_month)
    y_on_y_today_decimal = get_float(y_on_y_today)

    m_market_order_decision = compare_inflation(m_on_m_last_month_decimal, m_on_m_today_decimal)
    y_market_order_decision = compare_inflation(y_on_y_last_month_decimal, y_on_y_today_decimal)

    #MARKET ORDER DECISION TREE
    if m_market_order_decision == "LOWER":
        if y_market_order_decision == "LOWER":
            print('BOTH MARKET ORDERS: LONG')
            thread1 = threading.Thread(target=place_market_order_buy)
            thread2 = threading.Thread(target=place_market_order_buy)
            thread1.start()
            thread2.start()
            thread1.join()
            thread2.join()
        elif y_market_order_decision == "MATCH":
            compare_market_expectation(y_on_y_market_expectation, y_on_y_today_decimal)
        else:
            print('MONTH ON MONTH LONG, YEAR ON YEAR SHORT')
            thread1 = threading.Thread(target=place_market_order_buy)
            thread2 = threading.Thread(target=place_market_order_sell)
            thread1.start()
            thread2.start()
            thread1.join()
            thread2.join()
    elif m_market_order_decision == "MATCH":
        if y_market_order_decision == "LOWER":
            print('MONTH ON MONTH SHORT, YEAR ON YEAR LONG')
            thread1 = threading.Thread(target=place_market_order_sell)
            thread2 = threading.Thread(target=place_market_order_buy)
            thread1.start()
            thread2.start()
            thread1.join()
            thread2.join()
        elif y_market_order_decision == "MATCH":
            compare_market_expectation(m_on_m_market_expectation, m_on_m_today_decimal)
            compare_market_expectation(y_on_y_market_expectation, y_on_y_today_decimal)
