from commands.utils.nyaa import Nyaa
from utils.embeds        import send_nyaa_search

class NyaaCmd:
    def __init__(self, client):
        self.client  = client

    async def run(self, message, args):
        await send_nyaa_search(self.client, message, Nyaa(' '.join(args)))
