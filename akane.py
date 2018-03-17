import asyncio

from discord import Client, opus
from main_listener import MainListener
from config import CONFIG
from music.manager import Manager


class Akane():
    def __init__(self):
        self.client = Client()
        MainListener(self.client, Manager())

        opus.load_opus('libopus-0.x86.dll')
        # libs: 'libopus-0.x86.dll', 'libopus-0.x64.dll',
        # 'libopus-0.dll', 'libopus.so.0', 'libopus.0.dylib'.

        loop = asyncio.get_event_loop()
        try:
            loop.run_until_complete(self.run())
        except KeyboardInterrupt:
            loop.run_until_complete(self.client.logout())
            print('Offline.')
        finally:
            loop.close()
            quit()

    async def run(self):
        await self.client.start(CONFIG['discord_token'])

Akane()
