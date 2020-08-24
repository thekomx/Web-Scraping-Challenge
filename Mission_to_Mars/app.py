from scrape_mars import scrape as sc
from flask import Flask, render_template
import pymongo

    
mongo_db = pymongo.MongoClient('mongodb://localhost:27017').Mission_to_Mars_DB

app = Flask(__name__)

@app.route('/scrape')
def scrape():
    scraper = sc()

    mongo_db.Mars_News.insert_many(scraper.mars_news_list)
    mongo_db.Mars_Pics.insert_many(scraper.mars_pics_list)
    mongo_db.Mars_Facts.insert_many(scraper.mars_facts_list)
    mongo_db.Mars_Hemisphere.insert_many(scraper.mars_hemisp_list)

    return 'Successfully Scrapped.'


@app.route('/')
def index():

    mars_pics = list(mongo_db.Mars_Pics.find())
    mars_facts = list(mongo_db.Mars_Facts.find())

    return render_template('index.html', mars_pics=mars_pics, mars_facts=mars_facts)


if __name__ == "__main__":
    app.run(debug=True)