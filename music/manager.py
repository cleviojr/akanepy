from music.servermanager import ServerManager

class Manager(object):
    def __init__(self):
        self.server_managers = {}

    async def insert_server_and_play(self, client, textch, vid):
        server_id = textch.server.id
        if not f'{server_id}' in self.server_managers.keys():
            self.server_managers[f'{server_id}'] = ServerManager(client, textch)

        await self.server_managers[f'{server_id}'].play(vid)