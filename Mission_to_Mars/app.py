from scrape_mars import scrape as sc
from flask import Flask, render_template, redirect
from datetime import datetime
import pymongo

    
mongo_db = pymongo.MongoClient('mongodb://localhost:27017').Mission_to_Mars_DB


app = Flask(__name__)

@app.route('/scrape')
def scrape():
    scraper = sc()

    for c in mongo_db.list_collection_names():
        mongo_db[c].drop()

    mongo_db.Mars_News.insert_many(scraper.mars_news_list)
    mongo_db.Mars_Pics.insert_many(scraper.mars_pics_list)
    mongo_db.Mars_Facts.insert_many(scraper.mars_facts_list)
    mongo_db.Mars_Hemisphere.insert_many(scraper.mars_hemisp_list)
    mongo_db.Scrape_Date.insert_one({'scrape_date':datetime.now().strftime('%A %d %B %Y - %X')})

    return redirect('/')


@app.route('/')
def index():

    mars_news = list(mongo_db.Mars_News.find())
    mars_pics = list(mongo_db.Mars_Pics.find())
    mars_facts = list(mongo_db.Mars_Facts.find())
    mars_hemisp = list(mongo_db.Mars_Hemisphere.find())
    scrape_date = list(mongo_db.Scrape_Date.find())

    return render_template('index.html', mars_news=mars_news[0], mars_pics=mars_pics, mars_facts=mars_facts[0], mars_hemisp=mars_hemisp, scrape_date=scrape_date[0])


if __name__ == "__main__":
    app.run(debug=True)