from django.db import models
from django.db.models import Q
from django.utils.dateparse import parse_datetime
import logging

logger = logging.getLogger('ftpuploader')

class ArticleManager(models.Manager):
    def get_new_article(self, url=None, url_image=None, reporter=None, body=None, source=None, description=None, headline=None, published_date=None):  
        try:
            # Checking if article exist in db      
            the_article = Article.objects.filter(url=url)
            if the_article:
                print(f"Headline:'{headline}'\nSouce: '{source}'\nAlready have this article\n")
                Article.objects.update_article(the_article, reporter=reporter, body=body, published_date=published_date)
            else:
                if reporter is not None:
                    if len(reporter) == 2:
                        # Checking if Reporter exist in db
                        the_reporter = Reporter.objects.filter(first_name=reporter['first_name'], last_name=reporter['last_name'])
                        if the_reporter:
                            reporter_foreignKey = Reporter(id=the_reporter[0].id)
                        else:                         
                            reporter_foreignKey = Reporter(first_name=reporter['first_name'], last_name=reporter['last_name'])
                        reporter_foreignKey.save()
                    else:
                        the_reporter = Reporter.objects.filter(first_name=reporter['first_name'])
                        if the_reporter:
                            reporter_foreignKey = Reporter(id=the_reporter[0].id)
                        else:
                            reporter_foreignKey = Reporter(first_name=reporter['first_name'])
                        reporter_foreignKey.save()
                else:
                    the_reporter = Reporter.objects.filter(first_name=None)
                    reporter_foreignKey = Reporter(id=the_reporter[0].id)
                reporter_foreignKey.save()

                the_source = Source.objects.filter(name=source)
                if the_source:
                    source_foreignKey = Source(id=the_source[0].id, name=source)
                else:
                    source_foreignKey = Source(name=source)
                source_foreignKey.save()
                
                Article.objects.create(url=url, url_image=url_image, reporter=reporter_foreignKey, body=body, source=source_foreignKey, description=description, headline=headline, published_date=published_date)
                print(f"\n*********\nSAVED:\n'{url}'\n{source}\n*********\n")
        except BaseException as e:
            logger.error(f'Failed:{e}')

    def update_article(self, the_article, url=None, url_image=None, reporter=None, body=None, source=None, description=None, headline=None, published_date=None):
        for i in the_article:
            if not i.body:
                i.body = body
                i.save()
                print("Body Updated")
            if not i.published_date:
                i.published_date = published_date
                i.save()
                print("Published Date Updated")
            if i.reporter.first_name is None:
                if (len(reporter)) == 2:
                    the_reporter = Reporter.objects.filter(first_name=reporter['first_name'], last_name=reporter['last_name'])
                    if the_reporter:
                        i.reporter.id = the_reporter[0].id
                        i.reporter.save()
                        print("Reporter Updated")
                    else:                     
                        the_reporter = Reporter.objects.filter(first_name=None)
                        if the_reporter:
                            i.reporter.first_name = reporter['first_name']
                            i.reporter.last_name = reporter['last_name']
                            i.reporter.save()
                            print("Reporter Updated")
                else:
                    the_reporter = Reporter.objects.filter(first_name=None)
                    i.reporter.first_name = reporter['first_name']
                    i.reporter.id = the_reporter[0].id
                    i.reporter.save()
                    print("Reporter Updated")


class Source(models.Model):
    name = models.CharField(max_length=100)
    objects = models.Manager()

    def __str__(self):
        return f"{self.name}"

class Reporter(models.Model):
    first_name = models.CharField(max_length=100, null=True)
    last_name = models.CharField(max_length=100, null=True)
    url = models.CharField(max_length=1000, null=True)
    objects = models.Manager()

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

class Article(models.Model):
    unique_id = models.CharField(max_length=1000, blank=True, null=True)
    url = models.CharField(max_length=1000, null=True)
    url_image = models.CharField(max_length=1000,blank=True, null=True)
    reporter = models.ForeignKey(Reporter, on_delete=models.CASCADE, null=True)
    body = models.CharField(max_length=15000, blank=True, null=True)
    source = models.ForeignKey(Source, on_delete=models.CASCADE, null=True)
    description = models.CharField(max_length=1000, null=True)
    headline = models.CharField(max_length=1000, null=True)
    published_date = models.DateTimeField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    objects = ArticleManager()




