from commands.utils.parser import parse

# music commands
from commands.music.play import PlayCmd
from commands.music.skip import SkipCmd
from commands.music.shuffle import ShuffleCmd
from commands.music.clear import ClearCmd
from commands.music.setmusic import SetMusicCmd

# search commands
from commands.search.nyaa import NyaaCmd

MUSIC_COMMAND_LIST = {
    '!play': PlayCmd,
    '!skip': SkipCmd,
    '!shuffle': ShuffleCmd,
    '!clear': ClearCmd,
    '!setmusic': SetMusicCmd,
}

SEARCH_COMMAND_LIST = {
    '!nyaa': NyaaCmd,
}


class Runner():
    def __init__(self, client, message, manager):
        self.message = message
        self.client = client
        self.manager = manager

        self.key, self.args = parse(message)

    def is_music_command(self):
        for j in MUSIC_COMMAND_LIST.keys():
            if self.key == j:
                return True

    def is_search_command(self):
        for j in SEARCH_COMMAND_LIST.keys():
            if self.key == j:
                return True

    async def run(self):
        command = None
        if self.is_music_command():
            command = MUSIC_COMMAND_LIST[self.key](self.client, self.manager)
        elif self.is_search_command():
            command = SEARCH_COMMAND_LIST[self.key](self.client)

        if command:
            await command.run(self.message, self.args)
            print(f'{self.key} with success.')
        else:
            print('It was not a command.')
