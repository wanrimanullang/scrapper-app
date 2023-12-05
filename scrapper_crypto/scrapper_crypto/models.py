from django.db import models

class RedditTopic(models.Model):
    title = models.CharField(max_length=255)
    url = models.URLField()
    posted = models.DateTimeField()
    
class YouTubeVideo(models.Model):
    title = models.CharField(max_length=255)
    url = models.URLField()