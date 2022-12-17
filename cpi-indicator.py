import csv, json, requests
from bs4 import BeautifulSoup, Tag

#SET DATE
last_month_date = "11102022"

cpi_url = 'https://www.bls.gov/news.release/cpi.nr0.htm'
cpi_url_last_month = 'https://www.bls.gov/news.release/archives/cpi_' + last_month_date + '.htm'

r = requests.get(cpi_url)
file_output = 'cpi.htm'

o = requests.get(cpi_url_last_month)
file_output_archive = 'cpi_archive.htm'

with open(file_output, 'wb') as w:
    w.write(r.content)

with open(file_output_archive, 'wb') as w2:
    w2.write(o.content)

with open('cpi_archive.htm', 'r') as o:
    contents_archive = o.read()

    # Parse the HTML using BeautifulSoup
    soup_archive = BeautifulSoup(contents_archive, 'html.parser')

    y_on_y_inflation_line_archive = soup_archive.find('td', headers='cpi_pressa.r.1.3 cpi_pressa.h.1.9')

    y_on_y_inflation_line_archive_print = y_on_y_inflation_line_archive.find('span', class_='datavalue')

with open('cpi.htm', 'r') as f:
    contents = f.read()

    # Parse the HTML using BeautifulSoup
    soup = BeautifulSoup(contents, 'html.parser')

    # Find the td element with the headers attribute set to 'cpi_pressa.r.1.3 cpi_pressa.h.1.9'
    last_month_core_inflation_line = soup.find('td', headers='cpi_pressa.r.1.3 cpi_pressa.h.1.2 cpi_pressa.h.2.7')
    latest_core_inflation_line = soup.find('td', headers='cpi_pressa.r.1.3 cpi_pressa.h.1.2 cpi_pressa.h.2.8')
    y_on_y_inflation_line = soup.find('td', headers='cpi_pressa.r.1.3 cpi_pressa.h.1.9')

    # Find the span element within the td element
    last_month_core_inflation_print = last_month_core_inflation_line.find('span', class_='datavalue')
    latest_core_inflation_print = latest_core_inflation_line.find('span', class_='datavalue')
    y_on_y_inflation_line_print = y_on_y_inflation_line.find('span', class_='datavalue')

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

if isinstance(y_on_y_inflation_line_archive_print, Tag):
    y_on_y_inflation_line_archive_decimal = float(y_on_y_inflation_line_archive_print.text)

if isinstance(y_on_y_inflation_line_print, Tag):
    y_on_y_inflation_line_decimal = float(y_on_y_inflation_line_print.text)

if y_on_y_inflation_line_decimal < y_on_y_inflation_line_archive_decimal:
    print('Y on Y Inflation print lower')
elif y_on_y_inflation_line_decimal == last_month_core_inflation_decimal:
   print('Y on Y inflation print match')
else:
    print('Y on Y Inflation print higher')

# Print the text inside the span element
print(y_on_y_inflation_line_archive_decimal)
print(y_on_y_inflation_line_decimal)
