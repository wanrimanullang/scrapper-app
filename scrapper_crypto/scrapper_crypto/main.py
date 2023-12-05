import praw
from datetime import datetime, timedelta
from googleapiclient.discovery import build
# from .models import RedditTopic, YouTubeVideo
import json
import csv


reddit = praw.Reddit(client_id='1fVF21JTWEKv3oydcmfmbg',
                    client_secret='oliFQH4M7_mshYBrBdGrkEE9A5kjlg',
                    user_agent='scrapper-crypto by onlyManullang')

api_key = 'AIzaSyA0cwQobkZ0bc3JQMMqLvRO6IYnswVphcM'
youtube = build('youtube', 'v3', developerKey=api_key)

subreddit_name = "crypto"
subreddit = reddit.subreddit(subreddit_name)
search_keywords = "what's a good course to learn crypto"
year_ago = datetime.utcnow() - timedelta(days=365)

reddit_results = []
youtube_results = []

search_response = youtube.search().list(
    q=search_keywords,
    part='id,snippet',
    type='video',
    maxResults=10
).execute()

with open('output.csv', 'w', newline='') as csv_file:
    csv_writer = csv.writer(csv_file)
    csv_writer.writerow(['Title', 'URL', 'Posted'])
    for result in reddit_results:
        csv_writer.writerow([result['Title'], result['URL'], result['Posted']])
    for result in youtube_results:
        csv_writer.writerow([result['Title'], result['URL']])
        
for submission in subreddit.search(search_keywords, time_filter='year'):
    if submission.created_utc >= year_ago.timestamp():
        reddit_results.append({
            'Title': submission.title,
            'URL': submission.url,
            'Posted': datetime.utcfromtimestamp(submission.created_utc).isoformat()
        })
        
# for item in search_response['items']:
#     video_id = item['id']['videoId']
#     video_info = youtube.videos().list(part='snippet', id=video_id).execute()
#     video_title = video_info['items'][0]['snippet']['title']
#     video_url = f'https://www.youtube.com/watch?v={video_id}'
#     YouTubeVideo.objects.create(
#         title=video_title,
#         url=video_url
#     )