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
    address += " " + listing_soup.find("span",{"class":"filter-suburb pull-left"}).text
    i = 0
    price = listing_soup.find("span",{"class":"filter-price pull-left bbcsMatch"+str(i)})
    thumbnail= listing_soup.find("img")['src']
    while(price ==None):
        i +=1
        price = listing_soup.find("span",{"class":"filter-price pull-left bbcsMatch"+str(i)})
        if(i>10):
            break
    if(price !=None):
        price = price.text
    #get listing specific soup
    link= root_url+listing_soup.find("a",{"class":"listing-item"},href=True)['href']
    listing_html = simple_get(link)
    listing_specific_soup = BeautifulSoup(str(listing_html),"html.parser")
    facilities = re.findall('\d+',listing_specific_soup.find("div",{"class":"bbc-icons clearfix"}).text)
    #descriptions sepecfic soup, extract herotext and descriptions
    description_html = listing_specific_soup.find("div",{"class":"col-md-24 property-description"})
    description_specific_soup = BeautifulSoup(str(description_html),"html.parser")
    title = description_specific_soup.find("div",{"class":"inner"}).text
    title = title.replace(r"\n","").replace(r"\t","")
    
    description = description_specific_soup.find("div",{"class":"inner border-bot"}).p.text
    description = description.replace(r"\r","")
    print(description)
    listing_info = {"heroText":title,
                    "description":description,
                    "price":price,
                    "address":address,
                    "pet":"no info",                    
                    "bedrooms":facilities[0],
                    "bathrooms":facilities[1],
                    "parking":facilities[2],
                    "url":link,
                    "image":thumbnail,
                    "agent":"darling"}
    return listing_info
def darling_scrape():
    all_listings = []
    raw_html = simple_get(raw_url)
    soup = BeautifulSoup(raw_html,"html.parser")
    listings = soup.findAll("a",{"class":"listing-item"})
    for listing in listings:
        all_listings.append(parse_listing(listing))
    return all_listings
