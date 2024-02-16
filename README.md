# SupDeVinci-DataScienceOverJobOffers

Init project :
py -m venv venv
venv\Scripts\activate
py -m pip install -r requirements.txt

For run with bs4 :
cd .\WithBS4\GetDataFromJobOffersWithBS4
py .\GetDataFromWeLoveDev.py

For run with scrapy :
cd .\WithScrapy\
scrapy crawl welovedevs -o ./result/we_love_dev-output_from_scrapy.json

For install new librairie :
pip install ...
py -m pip freeze > requirements.txt
After the commit the user need to do this command :
py -m pip install -r requirements.txt