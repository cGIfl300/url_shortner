from django.db import models


class Urls(models.Model):
    destination = models.CharField(max_length=2048)
    short = models.CharField(max_length=6)
    pub_date = models.DateTimeField(auto_now=True)
