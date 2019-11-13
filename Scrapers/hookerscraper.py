from requests import get
from requests.exceptions import RequestException
from contextlib import closing
from bs4 import BeautifulSoup
import re
root_url = "https://www.ljhooker.co.nz"
raw_url = "https://www.ljhooker.co.nz/search/property?tt=rent&pid=&r=Otago&d=51&s%5B%5D=&ss=1&bp1=&bp2=&rp1=&rp2=&b1=&b2=&pt=&b=&c=&k=&searchType=residential&op=Find+Properties&form_build_id=form-15V1TjoaVV0yQRHmp1RyDmaAglDVAJ7Y-7Yct3eaab4&form_id=residential_property_search_form&pg=2"
current_page = 1

def simple_get(url):
     try:
        with closing(get(url, stream=True)) as resp:
            if is_good_response(resp):
                return resp.content
            else:
                return None
     except RequestException as e:
        log_error('Error during requests to {0} : {1}'.format(url, str(e)))
        return None
def is_good_response(resp):
    """
    Returns True if the response seems to be HTML, False otherwise.
    """
    content_type = resp.headers['Content-Type'].lower()
    return (resp.status_code == 200 
            and content_type is not None 
            and content_type.find('html') > -1)

def log_error(e):
    """
    It is always a good idea to log errors. 
    This function just prints them, but you can
    make it do anything.
    """
    print(e)

def parse_listing(listing):
    listing_soup = BeautifulSoup(str(listing),"html.parser")
    ##############find various things
    title = listing_soup.find("h2").text
    price = re.search('\d+',listing_soup.find("div",{"class":"featured_price_boxes"}).text)
    facilities = re.findall('\d+',listing_soup.find("div",{"class":"quick_summary"}).text)
    link= root_url+listing_soup.find("a",{"class":"property_link"},href=True)['href']
    thumbnail= "http://"+listing_soup.find("img")['src'][2:]
    if(price!=None):
        price = price.group()
    listing_info = {"title":title,
                    "price":price,
                    "bedrooms":facilities[0],
                    "bathrooms":facilities[1],
                    "garages":facilities[2],
                    "link":link,
                    "thumbnail":thumbnail}
    return listing_info
def hooker_scrape():
    all_listings = []
    current_page = 1
    while(True):
        page_now = raw_url + "&pg="+ str(current_page)
        raw_html = simple_get(page_now)
        soup = BeautifulSoup(raw_html,"html.parser")
        finished = soup.find("li",{"class": "prev_next_button disabled"})
        listings = soup.findAll("div",{"class":"property_snippet"})
        for listing in listings:
            all_listings.append(parse_listing(listing))
        current_page +=1
        if(finished==None):
            pass
        elif("Next"== str(finished.text)):
            break
    return all_listings


