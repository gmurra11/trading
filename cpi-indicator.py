import csv, json, requests
from bs4 import BeautifulSoup, Tag

cpi_url = 'https://www.bls.gov/news.release/cpi.nr0.htm'

r = requests.get(cpi_url)
file_output = 'cpi.htm'

with open(file_output, 'wb') as w:
    w.write(r.content)

with open('cpi.htm', 'r') as f:
    contents = f.read()

    # Parse the HTML using BeautifulSoup
    soup = BeautifulSoup(contents, 'html.parser')

    # Find the td element with the headers attribute set to 'cpi_pressa.r.1.3 cpi_pressa.h.1.9'
    last_month_core_inflation_line = soup.find('td', headers='cpi_pressa.r.1.3 cpi_pressa.h.1.2 cpi_pressa.h.2.7')
    latest_core_inflation_line = soup.find('td', headers='cpi_pressa.r.1.3 cpi_pressa.h.1.2 cpi_pressa.h.2.8')

    # Find the span element within the td element
    last_month_core_inflation_print = last_month_core_inflation_line.find('span', class_='datavalue')
    latest_core_inflation_print = latest_core_inflation_line.find('span', class_='datavalue')

    #print(last_month_core_inflation_print.text)

    if isinstance(last_month_core_inflation_print, Tag):
        last_month_core_inflation_decimal = float(last_month_core_inflation_print.text)

    if isinstance(latest_core_inflation_print, Tag):
        latest_core_inflation_decimal = float(latest_core_inflation_print.text)

    if latest_core_inflation_decimal < last_month_core_inflation_decimal:
        print('Inflation print lower')
    elif latest_core_inflation_decimal == last_month_core_inflation_decimal:
       print('Inflation print match')
    else:
        print('Inflation print higher')

    # Print the text inside the span element
    print(last_month_core_inflation_print.text)
    print(latest_core_inflation_print.text)
