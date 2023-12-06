from dotenv import load_dotenv
import os


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

class ScrapDataAPIReddit(APIView):
    CLIENT_ID_REDDIT =  os.environ.get('CLIENT_ID_REDDIT')
    CLIENT_SECRET_REDDIT = os.environ.get('CLIENT_SECRET_REDDIT')
    SELF_AGENT = os.environ.get('USER_AGENT')
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.reddit_results = []
        
    
    def get(self, request, format=None):
        reddit = praw.Reddit(client_id= self.CLIENT_ID_REDDIT,
                    client_secret=self.CLIENT_SECRET_REDDIT,
                    user_agent=self.SELF_AGENT)

        subreddit_name = "crypto"
        subreddit = reddit.subreddit(subreddit_name)
        search_keywords = request.GET.get('search_keywords', '')
        year_ago = datetime.utcnow() - timedelta(days=365)

        reddit_results = []
        
        for submission in subreddit.search(search_keywords, time_filter='year'):
            if submission.created_utc >= year_ago.timestamp():
                reddit_results.append({
                    'Title': submission.title,
                    'URL': submission.url,
                    'Posted': datetime.utcfromtimestamp(submission.created_utc).isoformat()
                })
        # return Response({
        #     'reddit_results': reddit_results,
        # })
        return render(request, 'reddit_results.html', {'reddit_results': reddit_results})
        
class ScrapDataAPIYoutube(APIView):
    API_KEY_YOUTUBE = os.environ.get('API_KEY_YOUTUBE')
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.youtube_results = []
    
    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)
    
    def get(self, request, format=None, *args, **kwargs):
        api_key = self.API_KEY_YOUTUBE
        youtube = build('youtube', 'v3', developerKey=api_key)

        search_keywords = request.GET.get('search_keywords', '')
        year_ago = datetime.utcnow() - timedelta(days=365)
        
        youtube_results = []
        search_response = []
        
        search_response = youtube.search().list(
            q=search_keywords,
            part='id,snippet',
            type='video',
            maxResults=20
            ).execute()
        
        return render(request, 'youtube_results.html', {'youtube_results': search_response})
