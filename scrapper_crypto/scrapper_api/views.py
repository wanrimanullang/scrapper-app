from django.shortcuts import render

from rest_framework import generics
from .models import RedditTopic
from .serializers import RedditTopicSerializer

class RedditTopicList(generics.ListAPIView):
    queryset = RedditTopic.objects.all()
    serializer_class = RedditTopicSerializer
