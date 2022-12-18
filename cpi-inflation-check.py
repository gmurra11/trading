import csv, json, requests
from bs4 import BeautifulSoup, Tag

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
    if today < last_month:
        print('Inflation print lower')
    elif today == last_month:
        print('Inflation print match')
    else:
        print('Inflation print higher')

# SET DATE
last_month_date = "11102022"

cpi_url = 'https://www.bls.gov/news.release/cpi.nr0.htm'
cpi_url_last_month = 'https://www.bls.gov/news.release/archives/cpi_' + last_month_date + '.htm'

m_on_m_last_month = get_inflation_data(cpi_url, "cpi_pressa.r.1.3 cpi_pressa.h.1.2 cpi_pressa.h.2.7")
m_on_m_today = get_inflation_data(cpi_url, "cpi_pressa.r.1.3 cpi_pressa.h.1.2 cpi_pressa.h.2.8")

y_on_y_last_month = get_inflation_data(cpi_url_last_month, "cpi_pressa.r.1.3 cpi_pressa.h.1.9")
y_on_y_today = get_inflation_data(cpi_url, "cpi_pressa.r.1.3 cpi_pressa.h.1.9")

m_on_m_last_month_decimal = get_float(m_on_m_last_month)
m_on_m_today_decimal = get_float(m_on_m_today)

compare_inflation(m_on_m_last_month_decimal, m_on_m_today_decimal)
print(m_on_m_last_month.text)
print(m_on_m_today.text)

y_on_y_last_month_decimal = get_float(y_on_y_last_month)
y_on_y_today_decimal = get_float(y_on_y_today)

compare_inflation(y_on_y_last_month_decimal, y_on_y_today_decimal)
print(y_on_y_last_month.text)
print(y_on_y_today.text)
