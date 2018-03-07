from googleapiclient.discovery import build
from config import CONFIG

service = build('youtube', 'v3', developerKey=CONFIG['YOUTUBE_API_KEY'])
class Youtube():
    def __init__(self):
        pass
        
    def search(self, query):
        resultado = service.search().list(type='video', part='id,snippet', q=query, maxResults=1).execute()['items'][0]
        print(f"musica encontrada: {resultado['snippet']['title']}")
        return resultado['id']['videoId']
    
    def list_playlist_videos(self, id):
        pass