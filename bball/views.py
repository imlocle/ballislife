from django.shortcuts import render, redirect, HttpResponse
from .models import Article
from .scrape import newsapi


def index(request):
    return render(request, "index.html")

def scrape(request):
    newsapi()
    return redirect('/')

