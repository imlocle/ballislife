from django.shortcuts import render, redirect, HttpResponse
from django import db
print (db.connections.databases)
from .models import Article
from .scrape import newsapi


def index(request):
    for i in Article.objects.raw("SELECT * FROM bball_article"):
        print("******")
        print (i)
    return render(request, "index.html")

def scrape(request):
    newsapi()
    return redirect('/')

