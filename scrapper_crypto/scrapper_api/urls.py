from django.urls import path
from .views import RedditTopicList
# , YouTubeVideoList

urlpatterns = [
    path('reddit-topics/', RedditTopicList.as_view(), name='reddit-topic-list'),
]
