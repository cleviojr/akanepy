from config                 import CONFIG
from random                 import shuffle
from commands.utils.youtube import Youtube
from collections            import deque

import asyncio

class ServerManager():
    def __init__(self, client, textch):
        #in args
        self.client       = client
        self.textch       = textch

        #not in args
        self.server       = textch.server
        self.id           = self.server.id
        self.voice_client = self.client.voice_client_in(self.server)
        self.loop         = self.voice_client.loop
        self.playlist     = deque()
        self.volume       = CONFIG['DEFAULT_VOLUME']
        self.is_paused    = False
        self.player       = None
        self.is_skipping  = False

    def is_playing(self):
        if self.player:
            return not self.player.is_done()

    def on_song_end(self):
        asyncio.run_coroutine_threadsafe(self.skip(), self.loop)

    async def add_to_playlist(self, video_id):
        self.playlist.append(video_id)

        await self.play()

    async def load_playlist(self, playlist_id, start_index=None):
        ytplaylist = Youtube().list_playlist_videos(playlist_id)

        if start_index:
            ytplaylist[:start_index - 1] = []

        self.playlist.extend(ytplaylist)
                    
        await self.play()
            
    async def play(self):      
            if not self.is_playing():
                self.player = await self.voice_client.create_ytdl_player(self.playlist.popleft(), after=self.on_song_end)
                self.player.volume = self.volume
                self.player.start()
    
    async def skip(self, is_command=False):
        if is_command:
            self.is_skipping = True
        
        if self.player:
            self.player.stop()
            if self.player.is_done() and self.is_skipping:
                self.is_skipping = False
                return

        if self.playlist:
            await self.play()

    def shuffle(self):
        shuffle(self.playlist)

    def clear(self):
        self.playlist.clear()