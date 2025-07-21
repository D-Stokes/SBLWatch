import requests


def get_channel_videos(api_key, uploads_playlist_id, max_results=50):
    url = f"https://www.googleapis.com/youtube/v3/playlistItems?part=snippet,contentDetails&playlistId={uploads_playlist_id}&maxResults={max_results}&key={api_key}"
    response = requests.get(url).json()
    return response["items"]

def get_video_stats(api_key, video_id):
    url = f"https://www.googleapis.com/youtube/v3/videos?part=statistics,snippet&id={video_id}&key={api_key}"
    return requests.get(url).json()