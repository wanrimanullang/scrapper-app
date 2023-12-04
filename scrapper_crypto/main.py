import praw
from datetime import datetime, timedelta
from googleapiclient.discovery import build
from scrapper_api.models import RedditTopic
import json
import csv


reddit = praw.Reddit(client_id='1fVF21JTWEKv3oydcmfmbg',
                    client_secret='oliFQH4M7_mshYBrBdGrkEE9A5kjlg',
                    user_agent='scrapper-crypto by onlyManullang')

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
        
with open('output.csv', 'w', newline='') as csv_file:
    csv_writer = csv.writer(csv_file)
    csv_writer.writerow(['Title', 'URL', 'Posted'])
    for result in reddit_results:
        csv_writer.writerow([result['Title'], result['URL'], result['Posted']])
        
for submission in subreddit.search(search_keywords, time_filter='year'):
    if submission.created_utc >= year_ago.timestamp():
        RedditTopic.objects.create(
            title=submission.title,
            url=submission.url,
            posted=datetime.utcfromtimestamp(submission.created_utc).isoformat()
        )