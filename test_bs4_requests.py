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

# Search for the script tag containing the window.__INSTANTSEARCH_SERVER_STATE__ object
for script in script_tags:
    print(script)

# Extract the JSON data from the script tag
# if target_script:
#     # Extract JSON data from the script tag using regex
#     json_data_str = re.search(r'window\.__INSTANTSEARCH_SERVER_STATE__\s*=\s*({.*?});', str(target_script))

#     print(json_data_str)

#     if json_data_str:
#         # Parse the JSON data
#         json_data = json.loads(json_data_str.group(1))

#         # Extract job offers
#         job_offers = json_data['initialResults']['public_jobs']['results']
        
#         # Print job details
#         for job in job_offers:
#             print("Title:", job['title'])
#             print("Company:", job['smallCompany']['companyName'])
#             print("Location:", job['formattedPlaces'][0])
#             print("Description:", job['descriptionPreview'])
#             print("-" * 50)
# else:
#     print("No script tag containing window.__INSTANTSEARCH_SERVER_STATE__ found.")