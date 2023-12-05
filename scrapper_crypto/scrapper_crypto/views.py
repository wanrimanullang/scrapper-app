from django.shortcuts import render
from django.http import JsonResponse

from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from praw import Reddit
from datetime import datetime, timedelta
from googleapiclient.discovery import build
from datetime import datetime, timedelta
import praw

# from .models import RedditTopic, YouTubeVideo
# from .serializers import RedditTopicSerializer,YouTubeVideoSerializer

# class RedditTopicList(generics.ListAPIView):
#     queryset = RedditTopic.objects.all()
#     serializer_class = RedditTopicSerializer

# class YouTubeVideoList(generics.ListAPIView):
#     queryset = YouTubeVideo.objects.all()
#     serializer_class = YouTubeVideoSerializer

class ScrapDataAPIReddit(APIView):
    def get(self, request, format=None):
        reddit = praw.Reddit(client_id='1fVF21JTWEKv3oydcmfmbg',
                    client_secret='oliFQH4M7_mshYBrBdGrkEE9A5kjlg',
                    user_agent='user_agent')

        subreddit_name = "crypto"
        subreddit = reddit.subreddit(subreddit_name)
        search_keywords = "what's a good course to learn crypto"
        year_ago = datetime.utcnow() - timedelta(days=365)

        reddit_results = []
        
        for submission in subreddit.search(search_keywords, time_filter='year'):
            if submission.created_utc >= year_ago.timestamp():
                reddit_results.append({
                    'Title': submission.title,
                    'URL': submission.url,
                    'Posted': datetime.utcfromtimestamp(submission.created_utc).isoformat()
                })

        return Response({
            'reddit_results': reddit_results,
        })
        
class ScrapDataAPIYoutube(APIView):
    def get(self, request, format=None):
        api_key = 'AIzaSyA0cwQobkZ0bc3JQMMqLvRO6IYnswVphcM'
        youtube = build('youtube', 'v3', developerKey=api_key)
        
        search_keywords = "what's a good course to learn crypto"
        year_ago = datetime.utcnow() - timedelta(days=365)
        
        youtube_results = []
        
        search_response = youtube.search().list(
            q=search_keywords,
            part='id,snippet',
            type='video',
            maxResults=10
            ).execute()
        
        return Response({
            'youtube_results': search_response,
        })
