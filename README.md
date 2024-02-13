# SupDeVinci-DataScienceOverJobOffers

Init project :
py -m venv venv
venv\Scripts\activate
pip install -r requirements.txt

For run with bs4 :
cd .\WithBS4\GetDataFromJobOffersWithBS4
py .\GetDataFromWeLoveDev.py

For run with scrapy :
cd .\WithScrapy\
scrapy crawl welovedevs -o ./result/we_love_dev-output_from_scrapy.json