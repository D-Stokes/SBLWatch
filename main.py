import os
from dotenv import load_dotenv
import requests
import pandas as pd
import isodate
from datetime import date, timedelta
from video_ids import VIDEO_ID

"""
This will be a daily datapull from scotts bass lessons to pull video metadata with
the intention of analysing video lifecycles and subscriber count
"""


load_dotenv()
api_key = os.getenv("YOUTUBE_API_KEY")
handle = "devinebass"
url = f"https://www.googleapis.com/youtube/v3/search?part=snippet&type=channel&q={handle}&key={api_key}"

# set dates and empty list object
today = date.today().strftime("%Y-%m-%d")
yesterday = (date.today() - timedelta(1)).strftime("%Y-%m-%d")
yesterday_csv_path = f'output/video_data{yesterday}.csv'
today_csv_path = f'output/video_data{today}.csv'
new_rows = []

response = requests.get(url).json()
channel_id = response["items"][0]["snippet"]["channelId"]

print("Channel ID:", channel_id)

"""
main loop, iterates through list of video ids, pulls all metadata and 
inserts it in to a csv file
"""
for video_id in VIDEO_ID:
    print("Video ID:", video_id)
    url = f"https://www.googleapis.com/youtube/v3/videos?part=snippet,statistics,contentDetails&id={video_id}&key={api_key}"

    response = requests.get(url)
    data = response.json()

    # Parse the stats
    if data:
        stats = data["items"][0]["statistics"]
        content = data["items"][0]["contentDetails"]
        snip = data["items"][0]["snippet"]
        dur_secs = int(isodate.parse_duration(content["duration"]).total_seconds())
        flat_data = {'video_id':video_id, 'date':date.today().isoformat(), 'dur_secs':dur_secs} | stats | content | snip
        new_rows.append(flat_data)
    else:
        print("Video not found or API key error.")

append_df = pd.DataFrame(new_rows) # convert to dataframe

if os.path.exists(yesterday_csv_path): # check if csv exists, if not create empty df
    existing_df = pd.read_csv(yesterday_csv_path)
else:
    existing_df = pd.DataFrame()

if not existing_df.empty: # if csv exists combine and drop dupes
    combined_df = pd.concat([existing_df, append_df], ignore_index=True)
    combined_df.drop_duplicates(subset=['video_id', 'date'], inplace=True)
else:
    combined_df = append_df

combined_df.to_csv(today_csv_path, index=False)
