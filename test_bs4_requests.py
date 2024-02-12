import requests
from bs4 import BeautifulSoup
import json
import re

# URL of the webpage
url = "https://welovedevs.com/app/fr/jobs?query=Data"

# Fetch the HTML content of the webpage
response = requests.get(url)
html_content = response.content

# Parse the HTML content with Beautiful Soup
soup = BeautifulSoup(html_content, "html.parser")

# Find the script tag containing the JavaScript object
script_tags = soup.find_all("script")

import re

# Assuming `soup` contains the parsed HTML
scripts = soup.find_all('script')

# Define the pattern to search for
pattern = r'window\.__INSTANTSEARCH_SERVER_STATE__\s*=\s*({.*?})'

# Iterate through each script tag and search for the pattern
for script in scripts:
    match = re.search(pattern, script.string)
    if match:
        data = match.group(1)
        print(data)  # This will print the extracted data
        break  # Assuming you only need the first match