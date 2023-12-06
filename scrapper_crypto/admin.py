from django.contrib import admin
from .models import RedditTopic, YouTubeVideo

admin.site.register(RedditTopic)
admin.site.register(YouTubeVideo)