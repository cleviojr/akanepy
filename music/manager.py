from music.servermanager import ServerManager

class Manager(object):
    def __init__(self):
        self.server_managers = {}

    def insert_server(self, client, textch):
        server_id = textch.server.id
        self.server_managers[f'{server_id}'] = ServerManager(client, textch)
