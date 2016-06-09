from __future__ import unicode_literals

from django.db import models


class Blog(models.Model):
    username = models.CharField(max_length=30)
    name = models.CharField('Default Blog Name', max_length=30)
    time = models.TimeField(auto_now=True)
    content = models.TextField('Empty Blog')


class Comments(models.Model):
    username = models.CharField(max_length=30)
    parent = models.IntegerField()  # for threaded comments
    time = models.TimeField(auto_now=True)
    content = models.TextField('Null')
    blog_name = models.CharField(max_length=30)
