from googleapiclient.discovery import build
from config import CONFIG

service = build('youtube', 'v3', developerKey=CONFIG['youtube_key'])


class Youtube():
    def __init__(self):
        pass

    def search(self, query):
        result = service.search().list(
                                       type='video',
                                       part='id,snippet',
                                       q=query,
                                       maxResults=1
                                      ).execute()['items'][0]
        return result['id']['videoId'], result['snippet']['title']

    def list_playlist_videos(self, playlist_id):
        result = service.playlistItems().list(
                                              part='contentDetails',
                                              playlistId=playlist_id,
                                              maxResults=50
                                             ).execute()['items']
        return [item['contentDetails']['videoId'] for item in result]
