import scrapy

class IndeedSpider(scrapy.Spider):
    name = 'indeed'
    start_urls = ['https://fr.indeed.com/jobs?q=Data&l=France&from=searchOnHP&vjk=ae910163a2c190ba']

    def parse(self, response):
        job_cards = response.css('.jobsearch-SerpJobCard')

        for job_card in job_cards:
            yield {
                'title': job_card.css('.title a::text').get(),
                'company': job_card.css('.company::text').get(),
                'location': job_card.css('.location::text').get(),
                'summary': job_card.css('.summary::text').get(),
                'salary': job_card.css('.salaryText::text').get()
            }

        # Pagination
        next_page = response.css('.pagination a:last-child::attr(href)').get()
        if next_page:
            yield scrapy.Request(url=response.urljoin(next_page), callback=self.parse)