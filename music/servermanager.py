from random import shuffle
from commands.utils.youtube import Youtube
from collections import deque
from utils.embeds import send_playing_embed
from utils.embeds import send_empty_playlist_embed
from utils.embeds import send_playlist_extend_embed
from utils.embeds import send_executed_embed

import asyncio


class ServerManager():
    def __init__(self, client, textch):
        # from args
        self.client = client
        self.textch = textch

        self.server = self.textch.server
        self.id = self.server.id
        self.voice_client = self.client.voice_client_in(self.server)
        self.loop = self.voice_client.loop
        self.playlist = deque()
        self.is_paused = False
        self.player = None
        self.is_skipping = False

    def is_playing(self):
        if self.player:
            return not self.player.is_done()

    def on_song_end(self):
        asyncio.run_coroutine_threadsafe(self.skip(), self.loop)

    async def add_to_playlist(self, video_id, video_title, message=None):
        self.playlist.append(video_id)

        text = f'Added: [{video_title}]'\
               f'(http://www.youtube.com/{video_id}).\n'\
               'Queue size: '\
               f'{len(self.playlist)}.'

        if message:
            await send_executed_embed(self.client, message,
                                      command='play',
                                      text=text)

        await self.play()

    async def load_playlist(self, playlist_id, start_index=None):
        ytplaylist = Youtube().list_playlist_videos(playlist_id)

        if start_index:
            ytplaylist[:start_index - 1] = []

        self.playlist.extend(ytplaylist)

        if self.textch:
            await send_playlist_extend_embed(self.client, self.textch,
                                             newsize=len(self.playlist))

        await self.play()

    async def play(self):
            if not self.is_playing():
                self.player = await self.voice_client.create_ytdl_player(
                                self.playlist.popleft(),
                                ytdl_options={'quiet': True},
                                after=self.on_song_end,
                            )
                self.player.start()

                if self.textch:
                    await send_playing_embed(self.client, self.textch,
                                             self.player.uploader,
                                             self.player.title,
                                             self.player.url)

    async def skip(self, is_command=False, message=None):
        if is_command and message:
            self.is_skipping = True
            await send_executed_embed(self.client, message,
                                      command='skip',
                                      text='Going to the next song.')

        if self.player:
            self.player.stop()
            if self.player.is_done() and self.is_skipping:
                self.is_skipping = False
                return

        if self.playlist:
            await self.play()
        else:
            if self.textch:
                await send_empty_playlist_embed(self.client, self.textch)

    async def shuffle(self, message=None):
        shuffle(self.playlist)

        if message:
            await send_executed_embed(self.client, message,
                                      command='shuffle',
                                      text='I just shuffled '
                                           'the server playlist.')

    async def clear(self, message):
        self.playlist.clear()

        await send_executed_embed(self.client, message,
                                  command='clear',
                                  text='I just cleared the server playlist.')
