import requests
import pandas as pd
from bs4 import BeautifulSoup
from splinter import Browser
from webdriver_manager.chrome import ChromeDriverManager


class scrape():

    mars_news = 'https://mars.nasa.gov/news/'
    mars_pics = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    mars_facts = 'https://space-facts.com/mars/'
    mars_hemisp = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'


    def __init__(self):

        executable_path = {'executable_path':ChromeDriverManager().install()}
        browser = Browser('chrome', **executable_path, headless=False)

    #---Scrape News------------------
        browser.visit(self.mars_news)
        browser.driver.maximize_window()
        soup_mars_news = BeautifulSoup(browser.html, 'lxml')

        list_soup_mars_news = soup_mars_news.find_all('li', class_='slide')
        self.mars_news_list = []
        for l in list_soup_mars_news:
            try:
                self.mars_news_list.append({'title':l.find('div', class_='content_title').text.strip(),\
                                            'content':l.find('div', class_='article_teaser_body').text.strip(),\
                                            'date':l.find('div', class_='list_date').text.strip()})
            except:
                pass
    #---------------------------------


    #---Scrape Pictures---------------
        browser.visit(self.mars_pics)
        browser.driver.maximize_window()
        soup_mars_pics = BeautifulSoup(browser.html, 'lxml')

        list_soup_mars_pics = soup_mars_pics.find_all('ul', class_='articles')[0].find_all('li', class_='slide')
        mars_pics_web = 'https://www.jpl.nasa.gov'
        lenn = len(list_soup_mars_pics)
        cur = 0
        self.mars_pics_list=[]
        for l in list_soup_mars_pics:
            try:
                release_date = {'release_date':l.find(class_='release_date').text}
                item_tease_overlay = {'item_tease_overlay':l.find(class_='item_tease_overlay').text}
                thumb = {'thumb':mars_pics_web+l.find(class_='thumb')['src']}
                large = {'large':mars_pics_web+l.a['data-fancybox-href']}

                cur+=1
                if cur == lenn:
                    nxt = 1
                    prv = cur - 1
                else:
                    nxt = cur + 1
                    if cur == 1:
                        prv = lenn
                    else:
                        prv = cur - 1
                
                page_indic = {'cur':cur, 'prv':prv, 'nxt':nxt}

                self.mars_pics_list.append(dict(release_date, **item_tease_overlay, **thumb, **large, **page_indic))
            except:
                pass
    #---------------------------------


    #---Scrape Facts------------------
        list_mars_facts = pd.read_html(self.mars_facts)

        self.mars_facts_list = []
        for l in list_mars_facts:
            fact_html_table = l.to_html(index=False)
            fact_html_table = fact_html_table.replace('style=', 'x=')
            fact_html_table = fact_html_table.replace('<th>0</th>', '<th>Description</th>')
            fact_html_table = fact_html_table.replace('<th>1</th>', '<th>Mars</th>')
            self.mars_facts_list.append({'fact_html_table' : fact_html_table})
    #---------------------------------


    #---Scrape Hemisphere-------------
        browser.visit(self.mars_hemisp)
        browser.driver.maximize_window()
        soup_mars_hemisp = BeautifulSoup(browser.html, 'lxml')

        list_soup_mars_hempisp = soup_mars_hemisp.find_all('div', class_='collapsible results')[0].find_all('div', class_='item')
        mars_hemisp_web = 'https://astrogeology.usgs.gov'
        self.mars_hemisp_list = []
        for l in list_soup_mars_hempisp:
            try:
                title = l.h3.text.replace(' Enhanced', '')
                link = BeautifulSoup(requests.get(mars_hemisp_web+l.a['href']).text, 'lxml')
                img_url = link.find_all('div', class_='downloads')[0].a['href']
                self.mars_hemisp_list.append({'title':title, 'img_url':img_url})
            except:
                pass
    #---------------------------------

        browser.driver.close()