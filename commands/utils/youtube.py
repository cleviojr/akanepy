from googleapiclient.discovery import build
from config import CONFIG

service = build('youtube', 'v3', developerKey=CONFIG['YOUTUBE_API_KEY'])

class Youtube():
    def __init__(self):
        pass
        
    def search(self, query):
        result = service.search().list(type='video', part='id,snippet', q=query, maxResults=1).execute()['items'][0]
        print(f"found a song: {result['snippet']['title']}")
        return result['id']['videoId']
    
    def list_playlist_videos(self, playlist_id):
        result = service.playlistItems().list(part='contentDetails', playlistId=playlist_id, maxResults=50).execute()['items'] 
        return [item['contentDetails']['videoId'] for item in result]
