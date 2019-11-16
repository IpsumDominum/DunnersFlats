from bs4 import BeautifulSoup
import re
import urllib.request, json 
try:
    from Scrapers.utils import simple_get
except Exception:
    from utils import simple_get
root_url = "https://www.manaproperty.co.nz"
raw_url = "https://www.manaproperty.co.nz/getPropertiesAsJSON?fbclid=IwAR02KLQKd3hClZuRsvpdE8p7U2S80ItRZ2CFS-qNuXNDIeJUEcBU1uuY_AA"


def parse_listing(listing):
    title = listing['street'] + listing['streetNumber']
    price = listing['rent']
    bedrooms = listing['bedrooms']
    bathrooms = listing['bathrooms']
    garages = listing['garages']
    if(garages==""):
        garages = 0
    link = root_url + listing['url']
    thumbnail = root_url + listing['images'][0]['url']
    listing_info = {"title":title,
                    "price":price,
                    "bedrooms":bedrooms,
                    "bathrooms":bathrooms,
                    "garages":garages,
                    "link":link,
                    "thumbnail":thumbnail,
                    "manager":"mana"}

    return listing_info
def mana_scrape():
    all_listings = []
    with urllib.request.urlopen(raw_url) as url:
        data = json.loads(url.read().decode())
    for listing in data:
        all_listings.append(parse_listing(listing))
    return all_listings
