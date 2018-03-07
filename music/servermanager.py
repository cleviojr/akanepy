from config import CONFIG
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
        self.playlist     = []
        self.volume       = CONFIG['DEFAULT_VOLUME']
        self.is_empty     = True
        self.is_paused    = False
        self.player       = None
        self.is_skipping  = False

    def on_song_end(self):
        asyncio.run_coroutine_threadsafe(self.skip(), self.loop)

    async def play(self, vid):      
        if self.is_empty:
            if self.player:
                if not self.player.is_done():
                    self.playlist.append(vid)
                    self.is_empty = False
                    return

            self.is_empty = False
            self.player = await self.voice_client.create_ytdl_player(vid, after=self.on_song_end)
            
            self.player.volume = self.volume
            self.player.start()

        else:
            self.playlist.append(vid)

    
    async def skip(self, command=False):
        if command:
            self.is_skipping = True
        
        if self.player.is_done() and self.is_skipping:
            self.is_skipping = False
            return

        self.player.stop()
        if self.playlist:
            self.player = await self.voice_client.create_ytdl_player(self.playlist.pop(), after=self.on_song_end)
            self.player.volume = self.volume
            self.player.start()
            
            if not self.playlist:
                self.is_empty = True
        else:
            self.is_empty = True
