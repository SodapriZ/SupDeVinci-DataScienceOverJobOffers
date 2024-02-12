import requests
from bs4 import BeautifulSoup
import json
import re
import json

def clean_string(text):
    # Remove HTML tags
    clean_text = re.sub(r'<[^>]+>', '', text)
    # Remove newlines
    clean_text = clean_text.replace("\n", '').replace('\r', ' ')
    # Remove extra whitespaces
    clean_text = re.sub(r'\s+', ' ', clean_text).strip()
    return clean_text

# URL of the webpage
url = "https://welovedevs.com/app/fr/jobs?query="

# Fetch the HTML content of the webpage
response = requests.get(url)
html_content = response.content

# Parse the HTML content with Beautiful Soup
soup = BeautifulSoup(html_content, "html.parser")

# Find the script tag containing the JavaScript object
script_tags = soup.find_all("script")

# Define the pattern to search for
pattern = r'window\.__INSTANTSEARCH_SERVER_STATE__\s*=\s*({.*?}}})'

# Iterate through each script tag and search for the pattern
for script in script_tags :
    if script.string:  # Check if script.string is not None
        script_string = clean_string(script.string)
        match = re.search(pattern, script_string)
        if match:
            # Load the modified JSON string
            data = match.group(1)
            data = data + "}]}]}}}"
            print(data)
            json_data = json.loads(data)
            # Print the cleaned JSON
            print(json.dumps(data, indent=4))
            # Define the output file path
            output_file = "output.json"
            # Write the JSON data to the file
            with open(output_file, "w", encoding="utf-8") as file:
                json.dump(json_data, file, indent=4, ensure_ascii=False)

            print("JSON data has been written to:", output_file)