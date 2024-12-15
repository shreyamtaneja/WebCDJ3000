from django.db import models

class React(models.Model):
    albumart = models.URLField(max_length=2000)
    artists = models.CharField(max_length=500)
    duration = models.IntegerField()
    name = models.CharField(max_length=500)
    preview_url = models.URLField(max_length=2000)
    track_number = models.SmallIntegerField()
    uri = models.URLField(max_length=2000)