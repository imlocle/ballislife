from django.db import models

class ArticleManager(models.Manager):
    def new_article(self, url, url_image, reporter, body, source, description, headline, published_on):
        the_article = Article.objects.filter(url = url)
        if the_article:
            return False
        else:
            # utilize foreignkey function
            reporter_f = Reporter()
            source_f = Source()
            Article.objects.create(url=url, url_image=url_image, reporter=reporter_f, body=body, source=source_f, description=description, headline=headline, published_on=published_on)

class Source(models.Model):
    name = models.CharField(max_length=100)

class Reporter(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    url = models.CharField(max_length=1000)

class Article(models.Model):
    unique_id = models.CharField(max_length=1000, blank=True, null=True)
    url = models.CharField(max_length=1000)
    url_image = models.CharField(max_length=1000,blank=True, null=True)
    reporter = models.ForeignKey(Reporter, on_delete=models.CASCADE)
    body = models.CharField(max_length=15000, blank=True, null=True)
    source = models.ForeignKey(Source, on_delete=models.CASCADE)
    description = models.CharField(max_length=1000)
    headline = models.CharField(max_length=1000)
    published_on = models.CharField(max_length=1000,blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    objects = ArticleManager()



