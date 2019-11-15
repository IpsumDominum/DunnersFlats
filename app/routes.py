from Scrapers.hookerscraper import hooker_scrape
from app import app
from flask import render_template
from flask import request
import math
import re
listings = hooker_scrape()
total_pages = math.ceil(len(listings)/8)
total_house = len(listings)
@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')
@app.route('/findproperty')
def findproperty():
    if(request.args.get('page')!=None):
        page = re.search('\d+',request.args.get('page'))
    else:
        page = None
    if(page==None):
        return render_template('properties.html',listings=listings,page=1,total_pages=total_pages,total_house=total_house)
    else:
        if(int(page.group())<1 or int(page.group())>total_pages):
            return render_template('404.html')
        else:
            return render_template('properties.html',listings=listings,page=page.group(),total_pages=total_pages,total_house=total_house)
@app.route('/rate')
def rate():
    return render_template('rate.html')
