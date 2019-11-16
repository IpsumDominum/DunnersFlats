from bs4 import BeautifulSoup
try:
    from Scrapers.utils import simple_get
except Exception:
    from utils import simple_get
import re
root_url = "https://www.darlingrealty.co.nz/"
raw_url = "https://www.darlingrealty.co.nz/?/residential/sold/false"
def parse_listing(listing):
    listing_soup = BeautifulSoup(str(listing),"html.parser")
    address = listing_soup.find("span",{"class":"filter-address pull-left"}).text
    title = listing_soup.find("span",{"class":"filter-address pull-left"}).text
    i = 0
    price = listing_soup.find("span",{"class":"filter-price pull-left bbcsMatch"+str(i)})
    while(price ==None):
        i +=1
        price = listing_soup.find("span",{"class":"filter-price pull-left bbcsMatch"+str(i)})
        if(i>10):
            break
    if(price !=None):
        price = price.text
    link= root_url+listing_soup.find("a",{"class":"listing-item"},href=True)['href']
    listing_html = simple_get(link)
    listing_specific_soup = BeautifulSoup(str(listing_html),"html.parser")
    facilities = re.findall('\d+',listing_specific_soup.find("div",{"class":"bbc-icons clearfix"}).text)
    thumbnail= listing_soup.find("img")['src']
    listing_info = {"title":title,
                    "price":price,
                    "bedrooms":facilities[0],
                    "bathrooms":facilities[1],
                    "garages":facilities[2],
                    "link":link,
                    "thumbnail":thumbnail,
                    "manager":"darling"}
    return listing_info
def darling_scrape():
    all_listings = []
    raw_html = simple_get(raw_url)
    soup = BeautifulSoup(raw_html,"html.parser")
    listings = soup.findAll("a",{"class":"listing-item"})
    for listing in listings:
        all_listings.append(parse_listing(listing))
    return all_listings
