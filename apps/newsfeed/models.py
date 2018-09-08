from django.db import models
from django.db.models import Q
from django.utils.dateparse import parse_datetime

class ArticleManager(models.Manager):
    def new_article(self, url, url_image, reporter, body, source, description, headline, published_date):
        obj, create = Article.objects.filter(url=url).update_or_create(url=url)
        if obj:
            print(published_date)
            print(type(published_date))
            print (obj.url)
            print("*****")
            return False
        if create:
            # utilize foreignkey function
            if reporter is not None:
                reporter_list = reporter.split()
                if len(reporter_list) > 2 or len(reporter_list) == 1:
                    reporter_foreignKey = Reporter(first_name=reporter)
                else:
                    reporter_foreignKey = Reporter(first_name=reporter_list[0], last_name=reporter_list[1])
            else:
                reporter_foreignKey = Reporter(first_name=reporter)
            reporter_foreignKey.save()
            source_foreignKey = Source(name=source)
            source_foreignKey.save()

            Article.objects.create(url=url, url_image=url_image, reporter=reporter_foreignKey, body=body, source=source_foreignKey, description=description, headline=headline, published_date=published_date)
            print(f"SAVED: '{url}'")

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
    url = models.CharField(max_length=1000)
    url_image = models.CharField(max_length=1000,blank=True, null=True)
    reporter = models.ForeignKey(Reporter, on_delete=models.CASCADE)
    body = models.CharField(max_length=15000, blank=True, null=True)
    source = models.ForeignKey(Source, on_delete=models.CASCADE)
    description = models.CharField(max_length=1000)
    headline = models.CharField(max_length=1000)
    published_date = models.DateTimeField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    objects = ArticleManager()




