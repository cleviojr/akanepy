from music.servermanager import ServerManager


class Manager(object):
    def __init__(self):
        self.managers = {}

    def insert_server(self, client, textch):
        server_id = textch.server.id
        self.managers[f'{server_id}'] = ServerManager(client, textch)
