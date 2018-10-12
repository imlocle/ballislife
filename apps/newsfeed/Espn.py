from dateutil import parser
from bs4 import BeautifulSoup as bs
import xml.etree.ElementTree as ET
import json, requests
from .models import Article
from .parsehelper import get_page, get_reporter_name
import logging

logger = logging.getLogger('ftpuploader')

class Espn:
    rss_nba_url = "http://www.espn.com/espn/rss/nba/news"

    def get_rssfeed_articles(self):
        response = get_page(self.rss_nba_url).text
        root = ET.fromstring(response)
        for i in root.iter('item'):
            url = i.find('link').text
            print(f'\n**** processing ESPN  ****\nURL:{url}\n****  **** ****\n')
            article_dict = get_espn_article(url)
            body = article_dict['Body']
            url_image = article_dict['UrlImage']
            headline = i.find('title').text
            description = i.find('description').text
            pdate = i.find('pubDate').text
            #Fri, 7 Sep 2018 14:54:33 EST
            published_date = parser.parse(pdate)
            source = "ESPN"
            reporter = article_dict['Reporter']
            Article.objects.get_new_article(url,url_image, reporter, body, source, description, headline, published_date)

def get_espn_article(url):
    article_dict = {}
    response = get_page(url)
    soup = bs(response.text, 'html.parser')
    try:
        article = soup.find('article', attrs={'class':'article'})
        headline = article.find('header', attrs={'class':'article-header'})
        article_body = article.find('div', attrs={'class':'article-body'})
        try:
            url_image = article.find('picture').find('source')['srcset']
        except:
            url_image = None
        try:
            reporter = article_body.find('div', attrs={'class':'author has-bio'}).find('span').previous_sibling
        except:
            reporter = None
        if reporter is None:
            try:
                reporter = article.find('div', attrs={'class':'author'}).find('span').previous_sibling
            except:
                reporter = None
        article_dict['Url'] = f"{url}"
        article_dict['UrlImage'] = url_image
        article_dict['Headline'] = headline.text
        article_dict['Reporter'] = get_reporter_name(reporter)
        article_dict['Body'] = article_body.text
        article_dict['Source'] = "ESPN"
    except BaseException as e:
        logger.error(f'Failed:{e}')
    return article_dict