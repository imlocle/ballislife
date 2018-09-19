from dateutil import parser
from bs4 import BeautifulSoup as bs
import xml.etree.ElementTree as ET
import json, requests
from .models import Article
from .parsehelper import get_page, clean_html
from .keywords import keywords

class RealGm:
    rss_realgm_url = "https://basketball.realgm.com/rss/wiretap/0/0.xml"

    def get_rssfeed_articles(self):
        response = get_page(self.rss_realgm_url).text
        root = ET.fromstring(response)
        for i in root.iter('item'):
            try:
                headline = i.find('title').text
                if "RealGM Radio" in headline:
                    continue
                url = i.find('link').text
                pdate = i.find('pubDate').text
                #Sun, 16 Sep 2018 17:17:01 EDT
                published_date = parser.parse(pdate)
                body = clean_html(i.find('description').text)
                description = headline
                url_image = i.find("{http://search.yahoo.com/mrss/}thumbnail").get('url')
                Article.objects.get_new_article(url=url, url_image=url_image, body=body, source="RealGM", description=description, headline=headline, published_date=published_date)
            except:
                pass



# http://rssfeeds.usatoday.com/UsatodaycomNba-TopStories
