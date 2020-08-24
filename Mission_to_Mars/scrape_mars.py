from bs4 import BeautifulSoup
import requests
import pandas as pd


class scrape():

    mars_news = 'https://mars.nasa.gov/news/'
    mars_pics = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    mars_facts = 'https://space-facts.com/mars/'
    mars_hemisp = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'

    mars_pics_web = 'https://www.jpl.nasa.gov'

    def __init__(self):

        soup_mars_news = BeautifulSoup(requests.get(self.mars_news).text,'lxml')
        list_soup_mars_news = soup_mars_news.find_all(class_='slide')
        self.mars_news_list = []
        for l in list_soup_mars_news:
            try:
                self.mars_news_list.append({'title':l.find('div', class_='content_title').text.strip(), 'content':l.find('div', class_='rollover_description_inner').text.strip()})
            except:
                pass


        soup_mars_pics = BeautifulSoup(requests.get(self.mars_pics).text, 'lxml')
        list_soup_mars_pics = soup_mars_pics.find_all('li', class_='slide')
        self.mars_pics_list=[]
        for l in list_soup_mars_pics:
            try:
                release_date = {'release_date':l.find(class_='release_date').text}
                item_tease_overlay = {'item_tease_overlay':l.find(class_='item_tease_overlay').text}
                thumb = {'thumb':self.mars_pics_web + l.find(class_='thumb')['src']}
                large = {'large':self.mars_pics_web + l.a['data-fancybox-href']}
                self.mars_pics_list.append(dict(release_date, **item_tease_overlay, **thumb, **large))
            except:
                pass


        list_mars_facts = pd.read_html(self.mars_facts)
        self.mars_facts_list = []
        for l in list_mars_facts:
            self.mars_facts_list.append({'fact_html_table' : l.to_html()})


        self.mars_hemisp_list = [{"title":"Valles Marineris Hemisphere", "img_url":"https://astropedia.astrogeology.usgs.gov/download/Mars/Viking/valles_marineris_enhanced.tif/full.jpg"},\
                                {"title":"Cerberus Hemisphere", "img_url":"https://astropedia.astrogeology.usgs.gov/download/Mars/Viking/cerberus_enhanced.tif/full.jpg"},\
                                {"title":"Schiaparelli Hemisphere", "img_url":"https://astropedia.astrogeology.usgs.gov/download/Mars/Viking/schiaparelli_enhanced.tif/full.jpg"},\
                                {"title":"Syrtis Major Hemisphere", "img_url":"https://astropedia.astrogeology.usgs.gov/download/Mars/Viking/syrtis_major_enhanced.tif/full.jpg"}]
