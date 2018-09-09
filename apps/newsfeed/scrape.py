import requests, json
from .models import Article
from .config import *
from .parsehelper import parse_definition, get_page
from django.utils.dateparse import parse_datetime
from .keywords import keywords

newapi_url_list = [
    "https://newsapi.org/v2/top-headlines?sources=espn&apiKey=", 
    "https://newsapi.org/v2/everything?sources=bleacher-report&apiKey="
    ]

def newsapi():
    for j in newapi_url_list:
        url = f'{j}{news_api_key}'
        getapi = requests.get(url).text
        converttojson = json.loads(getapi)['articles']
        for i in range(len(converttojson)):
            description = converttojson[i]['description']
            headline = converttojson[i]['title']
            if any(x in description for x in keywords):
                url = converttojson[i]['url']
                url_image = converttojson[i]['urlToImage']
                reporter = converttojson[i]['author']
                print(reporter)
                body = "none"
                source = converttojson[i]['source']['name']
                published_date = parse_datetime(converttojson[i]['publishedAt'])
                Article.objects.new_article(url, url_image, reporter, body, source, description, headline, published_date)
            else:
                print(f"This '{headline}' is not basketball related")
                continue
            i+=1

def espn():
    rss_feed_url = "http://www.espn.com/espn/rss/nba/news"
    result = get_page(rss_feed_url)

    