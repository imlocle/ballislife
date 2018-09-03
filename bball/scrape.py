import requests, json
from .models import Article
from .config import *
from .parsehelper import parse_definition, get_page

#keywords for filtering basketball related articles for newsapi
keywords={'Basketball', 'basketball', 'NBA', 'Kobe Bryant' 'Curry', 'double-double', 'LeBron', 'LaVar'}


def newsapi():
    url=f"https://newsapi.org/v2/top-headlines?sources=espn&{news_api_key}"
    getapi = requests.get(url).text
    converttojson = json.loads(getapi)['articles']
    for i in range(len(converttojson)):
        description = converttojson[i]['description']
        if any(x in description for x in keywords):
            url = converttojson[i]['url']
            url_image = converttojson[i]['urlToImage']
            reporter = converttojson[i]['author']
            body = "none"
            source = converttojson[i]['source']['name']
            headline = converttojson[i]['title']
            published_on = converttojson[i]['publishedAt']
            #Saving article to database
            Article.objects.new_article(url, url_image, reporter, body, source, description, headline, published_on)
        else:
            continue
        i+=1

def espn():
    rss_feed_url = "http://www.espn.com/espn/rss/nba/news"
    result = get_page(rss_feed_url)

    