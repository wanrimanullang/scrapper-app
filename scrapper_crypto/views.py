from dotenv import load_dotenv
import os

from django.shortcuts import render
from django.http import JsonResponse
import json
from googleapiclient.errors import HttpError

from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from datetime import datetime, timedelta
from googleapiclient.discovery import build
import praw
import re 

def clean_html_tags(text):
    clean_text = re.sub(r'<.*?>', '', text)
    return clean_text

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

        subreddit_name = "all"
        subreddit = reddit.subreddit(subreddit_name)
        search_keywords = request.GET.get('search_keywords', '')
        year_ago = datetime.utcnow() - timedelta(days=365)

        reddit_results = []
        reddit_comments = []

        for submission in subreddit.search(search_keywords, time_filter='year'):
            if submission.created_utc >= year_ago.timestamp():
                # comments = submission.comments.list()
                # modify_posted = lambda comment_datail: {
                #      'posted': datetime.utcfromtimestamp(comment_datail.created_utc).isoformat(),
                #      'author': comment_datail.author.name if comment_datail.author else '[deleted]',
                #      'comment_text': comment_datail.body
                # }
                reddit_results.append({
                    'Title': submission.title,
                    'URL': submission.url,
                    'IframeURL': submission.url.replace('https://www.reddit.com', 'https://reddit.artemisdigital.io'),
                    'Posted': datetime.utcfromtimestamp(submission.created_utc).isoformat(),
                    'Id': submission.id,
                    # 'Comments': list(map(modify_posted, comments))
                })
                
                # submission.comments.replace_more(limit=None)
                # comment_count = 0
                # for comment in submission.comments.list():
                #     reddit_comments.append({
                #         'author': comment.author.name if comment.author else '[deleted]',
                #         'comment_text': comment.body,
                #         'posted': datetime.utcfromtimestamp(comment.created_utc).isoformat(),
                #     })
                #     comment_count += 1

                #     if comment_count >= 10:
                #         break
                    

        return render(request, 'reddit_results.html', {'reddit_results': reddit_results})
        # return render(request, 'reddit_results.html', {'reddit_results': reddit_results,'reddit_comments': reddit_comments})

class ScrapDataAPIYoutube(APIView):
    API_KEY_YOUTUBE = os.environ.get('API_KEY_YOUTUBE')

    def get(self, request, format=None, *args, **kwargs):
        youtube = build('youtube', 'v3', developerKey=self.API_KEY_YOUTUBE)

        search_keywords = request.GET.get('search_keywords', '')
        year_ago = datetime.utcnow() - timedelta(days=365)

        search_response = []

        try:
            search_response = youtube.search().list(
                q=search_keywords,
                part='id,snippet',
                type='video',
                maxResults=20,
                videoSyndicated='true',
            ).execute()

            video_ids = [item['id']['videoId'] for item in search_response.get('items', [])]
            comments_response = []

            for video_id in video_ids:
                try:
                    comments = youtube.commentThreads().list(
                        part='snippet',
                        videoId=video_id,
                        maxResults=10
                    ).execute()
                    comments_response.extend(comments.get('items', []))

                except HttpError as e:
                    error_details = json.loads(e.content.decode('utf-8'))
                    if any(error.get('reason') == 'commentsDisabled' for error in error_details.get('error', {}).get('errors', [])):
                        print(f"Comments are disabled for video with ID: {video_id}")
                    else:
                        print(f"Error fetching comments for video with ID {video_id}: {error_details}")

            for comment in comments_response:
                comment_text = comment['snippet']['topLevelComment']['snippet']['textDisplay']
                cleaned_comment_text = clean_html_tags(comment_text)
                comment['snippet']['topLevelComment']['snippet']['cleaned_text'] = cleaned_comment_text

                comment_date = comment['snippet']['topLevelComment']['snippet']['publishedAt']
                formatted_comment_date = datetime.strptime(comment_date, "%Y-%m-%dT%H:%M:%S%z").strftime("%d %m %Y %m %H")
                comment['snippet']['topLevelComment']['snippet']['formatted_comment_date'] = formatted_comment_date

        except HttpError as e:
            error_details = json.loads(e.content.decode('utf-8'))
            print(f"Error searching videos: {error_details}")
            return HttpResponse(status=500)

        return render(request, 'youtube_results.html', {'youtube_results': search_response, 'comments': comments_response})