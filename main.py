import os
from dotenv import load_dotenv
import requests
import pandas as pd
import isodate
from functions import get_channel_videos, get_video_stats
from video_ids import VIDEO_ID

"""
This will be a daily datapull from scotts bass lessons to pull video metadata with
the intention of analysing video lifecycles and subscriber count
"""


load_dotenv()
api_key = os.getenv("YOUTUBE_API_KEY")
handle = "devinebass"
url = f"https://www.googleapis.com/youtube/v3/search?part=snippet&type=channel&q={handle}&key={api_key}"

response = requests.get(url).json()
channel_id = response["items"][0]["snippet"]["channelId"]

print("Channel ID:", channel_id)
uploads_playlist_id = "UU" + channel_id[2:]
print(uploads_playlist_id)

results = get_channel_videos(api_key, uploads_playlist_id)
print(results)

video_data = []

for item in results:
    snippet = item['snippet']
    content = item['contentDetails']

    video_data.append({
        'title': snippet['title'],
        'video_id': content['videoId'],
        'publish_date': snippet['publishedAt'],
        'channel': snippet['channelTitle'],
        'description': snippet['description'],
        'thumbnail_url': snippet['thumbnails'].get('high', {}).get('url'),
        'video_url': f"https://www.youtube.com/watch?v={content['videoId']}"
    })

# Create DataFrame
df = pd.DataFrame(video_data)

# Optional: Convert publish date to datetime
df['publish_date'] = pd.to_datetime(df['publish_date'])

# Preview the data
print(df.head())


video_id = VIDEO_ID[0]

url = f"https://www.googleapis.com/youtube/v3/videos?part=snippet,statistics,contentDetails&id={video_id}&key={api_key}"

response = requests.get(url)
data = response.json()

# Parse the stats
if data['items']:
    stats = data['items'][0]['statistics']
    details = data['items'][0]['contentDetails']

    views = (stats.get('viewCount'))
    likes = (stats.get('likeCount'))
    comments = ( stats.get('commentCount'))
    isoduration = ( details.get('duration'))
    duration = isodate.parse_duration(str(isoduration))
    print(views, likes, comments, duration)
else:
    print("Video not found or API key error.")

