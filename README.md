# SupDeVinci-DataScienceOverJobOffers

Init project :
py -m venv venv
venv\Scripts\activate
pip install -r requirements.txt

For run with bs4 :
py .\WithBS4\GetDataFromJobOffersWithBS4\GetDataFromWeLoveDev.py

For run with scrapy :
cd .\WithScrapy\
scrapy crawl indeed -o ./result/output.json