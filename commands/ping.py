class PingCmd():
    def __init__(self, client):
        self.client = client
    
    async def run(self, message, args):
        await self.client.send_message(message.channel, 'pong')