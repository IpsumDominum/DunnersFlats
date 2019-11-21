from Scrapers.hookerscraper import hooker_scrape
from Scrapers.manascraper import mana_scrape
from Scrapers.darlingscraper import darling_scrape
import requests
import json

if __name__ == "__main__":
    databaseAPI = "https://nathanhollows.com/flats/api/flats"
    deleteAPI = "https://nathanhollows.com/flats/api/flats/id/"
    listings = hooker_scrape() + mana_scrape() + darling_scrape()    
    #listings  = []
    #listings = darling_scrape()
    #listings = hooker_scrape()
    #listings = mana_scrape()
    result = requests.get(databaseAPI)
    database = result.json()
    #Post anything which is not already in the database
    #Delete anything in the database which is not in the listings
    expired_entries = {entry['id']:entry['address'] for entry in database['data']}
    for listing in listings:
        not_present = True
        for entry in database['data']:
            if(entry['address']==listing['address']):
                not_present = False
                del expired_entries[entry['id']]
        if not_present:
            print("+",listing['address'])
            post = requests.post(url=databaseAPI,data=listing)

    print(expired_entries)
    for expired in expired_entries:
        print("-",expired_entries[expired])
        delete = requests.delete(url=deleteAPI+expired)
    result = requests.get(databaseAPI)
    database = result.json()
    print("="*10)
    for data in database['data']:
        print(data['address'])
  
