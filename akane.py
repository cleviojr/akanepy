import asyncio

from discord import Client, opus
from main_listener import MainListener
from music.manager import Manager
import sys
import config


class Akane():
    def __init__(self):
        self.info = config.CONFIG['bots'][0]
        self.client = Client()
        MainListener(self.client, Manager())
        self.loop = asyncio.get_event_loop()

        self.loop.run_until_complete(self.start())
    async def start(self):
        try:
            await self.client.start(self.info['discord_token'])
        except KeyboardInterrupt:
            await self.stop()

    async def stop(self):
        print('Offline.')
        await self.client.logout()

Akane()
