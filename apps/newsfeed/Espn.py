from dateutil import parser
from bs4 import BeautifulSoup as bs
import xml.etree.ElementTree as ET
import json, requests
from .models import Article
from .parsehelper import get_page, get_bleacher_report_body_text
from .keywords import keywords

class Espn:
    rss_nba_url = "http://www.espn.com/espn/rss/nba/news"

    def get_rssfeed_articles(self):
        reponse = get_page(self.rss_nba_url)
        root = ET.fromstring(reponse)
        for i in root.iter('item'):
            try:
                url = i.find('link').text
                print(url)
                article_dict = get_espn_article(url)
                reporter = article_dict['Reporter']
                body = article_dict['Body']
                url_image = article_dict['UrlImage']
                headline = i.find('title').text
                description = i.find('description').text
                pdate = i.find('pubDate').text
                #Fri, 7 Sep 2018 14:54:33 EST
                published_date = parser.parse(pdate)
                source = "ESPN"
                Article.objects.new_article(url,url_image, reporter, body, source, description, headline, published_date)
            except:
                pass

def get_espn_article(url):
    article_dict = {}
    response = requests.get(url)
    soup = bs(response.text, 'html.parser')
    try:
        article = soup.find('article', attrs={'class':'article'})
        headline = article.find('header', attrs={'class':'article-header'})
        article_body = article.find('div', attrs={'class':'article-body'})
        url_image = article.find('picture').find('source')['srcset']
        reporter = article_body.find('div', attrs={'class':'author has-bio'}).find('span').previous_sibling
        article_dict['Url'] = f"{url}"
        article_dict['UrlImage'] = url_image
        article_dict['Headline'] = headline.text
        article_dict['Reporter'] = reporter
        article_dict['Body'] = article_body.text
    except:
        pass

    return article_dict