from scrape_mars import scrape as sc
from flask import Flask
import pymongo


app = Flask(__name__)

@app.route('/scrape')
def scrape():
    scraper = sc()

    mongo_client = pymongo.MongoClient('mongodb://localhost:27017')
    mongo_db = mongo_client.Mission_to_Mars_DB

    mongo_collection = mongo_db.Mars_News
    for n in scraper.mars_news_list:
        mongo_collection.insert_one(n)

    mongo_collection = mongo_db.Mars_Pics
    for p in scraper.mars_pics_list:
        mongo_collection.insert_one(p)

    mongo_collection = mongo_db.Mars_Facts
    for f in scraper.mars_facts_list:
        mongo_collection.insert_one(f)

    mongo_collection = mongo_db.Mars_Hemisphere
    for h in scraper.mars_hemisp_list:
        mongo_collection.insert_one(h)


@app.route('/')
def index():
    pass