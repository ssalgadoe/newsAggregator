from django.db import models

# Create your models here.
from django.db import models

class news_sources(models.Model):
    name = models.CharField(max_length=40, blank=False, null=True)
    url = models.CharField(max_length=40, blank=False, null=True)
    description = models.CharField(max_length=60, blank=True, null=True)
    comments = models.CharField(max_length=60, blank=True, null=True)

    def __str__(self):
        return(self.name)


class news_items(models.Model):
    source = models.CharField(max_length=100, blank=False, null=True)
    title = models.CharField(max_length=200, blank=False, null=True)
    url = models.CharField(max_length=200, blank=False, null=True)
    body = models.CharField(max_length=5000, blank=True, null=True)
    time_st = models.CharField(max_length=60, blank=True, null=True)

    def __str__(self):
        return(self.title)


class active_news_items(models.Model):
    source = models.CharField(max_length=100, blank=False, null=True)
    title = models.CharField(max_length=200, blank=False, null=True)
    url = models.CharField(max_length=200, blank=False, null=True)
    body = models.CharField(max_length=5000, blank=True, null=True)
    time_st = models.CharField(max_length=60, blank=True, null=True)

    def __str__(self):
        return(self.title)
