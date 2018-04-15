import asyncio

from discord import Client, opus
from main_listener import MainListener
from config import CONFIG
from music.manager import Manager


class Akane():
    def __init__(self):
        self.client = Client()
        MainListener(self.client, Manager())

        self.loop = asyncio.get_event_loop()
        try:
            self.loop.run_until_complete(self.run())
        except KeyboardInterrupt:
            self.loop.run_until_complete(self.client.logout())
            print('Offline.')
        finally:
            self.loop.close()
            quit()

    async def run(self):
        await self.client.start(CONFIG['discord_token'])

Akane()
