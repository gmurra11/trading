import csv, json, requests
from bs4 import BeautifulSoup, Tag

def download_html(url, file_name):
    """Downloads the HTML from the given URL and saves it to the given file."""
    response = requests.get(url)
    with open(file_name, 'wb') as f:
        f.write(response.content)

def parse_html(file_name):
    """Parses the HTML from the given file and returns the parsed HTML."""
    with open(file_name, 'r') as f:
        contents = f.read()
    return BeautifulSoup(contents, 'html.parser')

# SET DATE
last_month_date = "11102022"

cpi_url = 'https://www.bls.gov/news.release/cpi.nr0.htm'
cpi_url_last_month = '/'.join(['https://www.bls.gov/news.release/archives/cpi', last_month_date, 'htm'])

download_html(cpi_url, 'cpi.htm')
download_html(cpi_url_last_month, 'cpi_archive.htm')

soup_archive = parse_html('cpi_archive.htm')
soup = parse_html('cpi.htm')

# Find the span elements with the 'datavalue' class
span_elements = soup.find_all('span', class_='datavalue')

# Extract the values from the span elements
try:
    last_month_core_inflation = float(span_elements[0].text)
    latest_core_inflation = float(span_elements[1].text)
    y_on_y_inflation = float(span_elements[2].text)
except (IndexError, ValueError):
    print("Error parsing span elements")

# Compare the values
if latest_core_inflation < last_month_core_inflation:
    print('Inflation lower')
elif latest_core_inflation == last_month_core_inflation:
   print('Inflation match')
else:
    print('Inflation higher')

# Print the values
print("Last month's core inflation: {0:.2f}".format(last_month_core_inflation))
print("Latest core inflation: {0:.2f}".format(latest_core_inflation))
print("Year-on-year inflation: {0:.2f}".format(y_on_y_inflation))

# Find the span element for the year-on-year inflation for the last month
try:
    y_on_y_inflation_archive = float(soup_archive.find('span', class_='datavalue').text)
except (AttributeError, ValueError):
    print("Error parsing span element")

# Print the value
print("Year-on-year inflation for the last month: {0:.2f}".format(y_on_y_inflation_archive))
