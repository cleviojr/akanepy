from commands.utils.parser import parse

#general commands
from commands.ping import PingCmd

#music commands
from commands.play    import PlayCmd
from commands.skip    import SkipCmd
from commands.vol     import VolCmd
from commands.shuffle import ShuffleCmd
from commands.clear   import ClearCmd

GENERAL_COMMAND_LIST = {
    '!ping': PingCmd,
}

MUSIC_COMMAND_LIST = {
    '!play': PlayCmd,
    '!skip': SkipCmd,
    '!vol': VolCmd,
    '!shuffle': ShuffleCmd,
    '!clear': ClearCmd,
}

class Runner():
    def __init__(self, client, message, manager):
        self.message = message
        self.client  = client
        self.manager = manager
            
        self.key, self.args = parse(message)

    def is_command(self):
        for j in GENERAL_COMMAND_LIST.keys(): 
            if self.key == j: 
                return True 

    def is_music_command(self):
        for j in MUSIC_COMMAND_LIST.keys(): 
            if self.key == j: 
                return True

    async def run(self):
        command = None
        if self.is_command(): 
            command = GENERAL_COMMAND_LIST[self.key](self.client)
        elif self.is_music_command(): 
            command = MUSIC_COMMAND_LIST[self.key](self.client, self.manager)

        if command:
            await command.run(self.message, self.args)
            print(f'{self.key} with success.')
        else:
            print('It was not a command.')            