from django.db import models
from django.db.models import Q
from django.utils.dateparse import parse_datetime
import logging

logger = logging.getLogger('ftpuploader')

class ArticleManager(models.Manager):
    def new_article(self, url=None, url_image=None, reporter=None, body=None, source=None, description=None, headline=None, published_date=None):
        try:      
            the_article = Article.objects.filter(url=url)          
            if the_article:
                for e in the_article:
                    if not e.body:
                        e.body = body
                        e.save()
                        print("Body Updated")
                    if not e.published_date:
                        e.published_date = published_date
                        e.save()
                        print("Published Date Updated")
            else:
                # utilize foreignkey function
                if reporter is not None:
                    reporter_list = reporter.split()
                    if len(reporter_list) == 2:
                        reporter_foreignKey = Reporter(first_name=reporter_list[0], last_name=reporter_list[1])
                    else:
                        reporter_foreignKey = Reporter(first_name=reporter)
                else:
                    reporter_foreignKey = Reporter(first_name=reporter)
                
                reporter_foreignKey.save()
                source_foreignKey = Source(name=source)
                source_foreignKey.save()    
                Article.objects.create(url=url, url_image=url_image, reporter=reporter_foreignKey, body=body, source=source_foreignKey, description=description, headline=headline, published_date=published_date)
                print(f"SAVED: '{url}'")
        except BaseException as e:
            logger.error('Failed to do something: ' + str(e))


class Source(models.Model):
    name = models.CharField(max_length=100, null=True)

    def __str__(self):
        return f"{self.name}"

class Reporter(models.Model):
    first_name = models.CharField(max_length=100, null=True)
    last_name = models.CharField(max_length=100, null=True)
    url = models.CharField(max_length=1000, null=True)

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




