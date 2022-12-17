import requests
from bs4 import BeautifulSoup

def download_html(url, file_name):
    """Downloads the HTML from the given URL and saves it to the specified file."""
    response = requests.get(url)
    with open(file_name, 'wb') as f:
        f.write(response.content)

def parse_html(file_name):
    """Parses the HTML from the specified file and returns a BeautifulSoup object."""
    with open(file_name, 'r') as f:
        contents = f.read()
        soup = BeautifulSoup(contents, 'html.parser')
    return soup

# Set the date
last_month_date = "11102022"

# Build the URLs for the HTML files
cpi_url = 'https://www.bls.gov/news.release/cpi.nr0.htm'
cpi_url_last_month = '/'.join(['https://www.bls.gov/news.release/archives/cpi', last_month_date + '.htm'])

# Download and parse the HTML files
download_html(cpi_url, 'cpi.htm')
download_html(cpi_url_last_month, 'cpi_archive.htm')
soup = parse_html('cpi.htm')
soup_archive = parse_html('cpi_archive.htm')

# Find the span elements with the 'datavalue' class
spans = soup.find_all('span', class_='datavalue')
spans_archive = soup_archive.find_all('span', class_='datavalue')

# Get the values of the span elements
try:
    last_month_core_inflation = float(spans[0].text)
    latest_core_inflation = float(spans[1].text)
    y_on_y_inflation = float(spans[2].text)
except (IndexError, ValueError):
    print('Error: Unable to parse span elements')

try:
    y_on_y_inflation_archive = float(spans_archive[0].text)
except (IndexError, ValueError):
    print('Error: Unable to parse span elements from archive')

# Print the values of the span elements
print('Last month core inflation: {}'.format(last_month_core_inflation))
print('Latest core inflation: {}'.format(latest_core_inflation))
print('Year-on-year inflation: {}'.format(y_on_y_inflation))

# Compare the values of the span elements
if latest_core_inflation < last_month_core_inflation:
    print('Inflation lower')
elif latest_core_inflation == last_month_core_inflation:
    print('Inflation match')
else:
    print('Inflation higher')
