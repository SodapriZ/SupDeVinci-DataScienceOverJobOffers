import requests
from bs4 import BeautifulSoup
import json
import re

# URL of the webpage
url = "https://welovedevs.com/app/fr/jobs?query=&refinementList%5Bdetails.remotePolicy.frequency%5D%5B0%5D=fullTime&place%5Blocation%5D=Nantes%2C%20France&place%5BlatLng%5D=47.218371%2C-1.553621&place%5BplaceId%5D=ChIJra6o8IHuBUgRMO0NHlI3DQQ"

# Fetch the HTML content of the webpage
response = requests.get(url)
html_content = response.content

# Parse the HTML content with Beautiful Soup
soup = BeautifulSoup(html_content, "html.parser")

# Find the script tag containing the JavaScript object
script_tags = soup.find_all("script")

# Define the pattern to search for
pattern = r'window\.__INSTANTSEARCH_SERVER_STATE__\s*=\s*({.*?})}}'

# Iterate through each script tag and search for the pattern
for script in script_tags :
    if script.string:  # Check if script.string is not None
        match = re.search(pattern, script.string)
        if match:
            data = match.group(1)
            print(data)
            # # Parse the JSON data
            # json_data = json.loads(data)
            # # Now you have the JSON data, you can access it as a Python dictionary
            # # For example, to access the initialResults key:
            # initial_results = json_data['initialResults']
            # print(initial_results)