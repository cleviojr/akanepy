class VolCmd():
    def __init__(self, client, manager):
        self.client  = client
        self.manager = manager

    async def run(self, message, args):
        server_id = message.server.id

        self.manager.server_managers[f'{server_id}'].volume        = float(args[0])
        self.manager.server_managers[f'{server_id}'].player.volume = float(args[0])