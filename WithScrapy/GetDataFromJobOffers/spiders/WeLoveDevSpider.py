import scrapy
import json
import re

class WeLoveDevsSpider(scrapy.Spider):
    name = 'welovedevs'
    allowed_domains = ['welovedevs.com']
    start_urls = ['https://welovedevs.com/app/fr/jobs?query=Data']

    def parse(self, response):
        # Extract JSON data from the script tag
        script_text = response.xpath('//script[contains(., "__INSTANTSEARCH_SERVER_STATE__")]/text()').get()
        if script_text:
            # Extract the JSON string using regex
            pattern = r'"results"\s*:\s*\[(.*?)\]\}'
            match = re.search(pattern, script_text)
            if match:
                data = match.group(1)
                json_data = json.loads(data)
                yield json_data
