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
    address = listing['street'] + " " + listing['streetNumber'] + " " + listing['suburb']
    price = listing['rent']
    bedrooms = listing['bedrooms']
    bathrooms = listing['bathrooms']
    garages = listing['garages']
    pet = int(listing['allowsPets'])
    description = listing['description']
    title = listing['furnishing']
    if(garages==""):
        garages = 0
    link = root_url + listing['url']
    thumbnail = root_url + listing['images'][0]['url']    
    listing_info = {"heroText":title,
                    "description":description,
                    "price":price,
                    "address":address,
                    "pet":pet,                    
                    "bedrooms":bedrooms,
                    "bathrooms":bathrooms,
                    "parking":garages,
                    "url":link,
                    "image":thumbnail,
                    "agent":"mana"}
    return listing_info
def mana_scrape():
    all_listings = []
    with urllib.request.urlopen(raw_url) as url:
        data = json.loads(url.read().decode())
    for listing in data:
        all_listings.append(parse_listing(listing))
    return all_listings
