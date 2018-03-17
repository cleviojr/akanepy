class SkipCmd():
    def __init__(self, client, manager):
        self.client  = client
        self.manager = manager
    
    async def run(self, message, args):
        server_id = message.server.id

        try:
            await self.manager.server_managers[f'{server_id}'].skip(is_command=True, message=message)
        except KeyError:
            pass
        