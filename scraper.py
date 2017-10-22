from datetime import datetime
from bs4 import BeautifulSoup as bs
import requests
import scraperwiki
import itertools
import json


def scrape_asins(base_url, vendors):
    for vendor in vendors:
        s = requests.session()
        for page in itertools.count():
            pages = s.post(base_url.format(vendor, page + 1, vendor))
            soup = json.loads(pages.text)
            if not soup['products']:
                break
            products = soup['products']
            for product in products:
                price = product['price']
                asin = product['detailPageUrlsMap']['products_widget'].split('dp/')[-1].split('?')[0]
                todays_date = str(datetime.now())
                scraperwiki.sqlite.save(unique_keys=['Date'], data={"Seller ID": vendor, "ASIN": asin.strip(), "Price": price.strip(), "Date": todays_date})
                print asin


def scrape(vendors):
    base_url = 'http://www.amazon.com/sp/ajax/products?marketplaceID=ATVPDKIKX0DER&productSearchRequestData=%7B%22marketplace%22%3A%22ATVPDKIKX0DER%22%2C%22seller%22%3A%22{}%22%2C%22url%22%3A%22%2Fsp%2Fajax%2Fproducts%22%2C%22pageSize%22%3A12%2C%22searchKeyword%22%3A%22%22%2C%22extraRestrictions%22%3A%7B%7D%2C%22pageNumber%22%3A{}%7D&seller={}'
    scrape_asins(base_url, vendors)


if __name__ == '__main__':
    vendors = ['A2OD7IFUHIW1N3', 'A2C5MPYTBFJ93K', 'A1Y40LKWIIUT7S', 'A2C5MPYTBFJ93K',
    'A3M8FJC1EJFXFS', 'A26QRKYYX4QC29', 'A2NFLQYUS6IWR7']
    scrape(vendors)
    
