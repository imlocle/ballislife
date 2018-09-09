from django.shortcuts import render, redirect, HttpResponse
from django import db
from .models import Article
from .NewsApi import NewsApi
from .Espn import Espn


def index(request):
    newsfeed = []
    for i in Article.objects.raw("SELECT * FROM newsfeed_article ORDER BY published_date DESC"):
        newsfeed.append(i)
    context = {'newsfeed': newsfeed}
    return render(request, "index.html", context)

def scrape(request):
    NewsApi().get_articles()
    Espn().get_rssfeed_articles()
    return redirect('/')

