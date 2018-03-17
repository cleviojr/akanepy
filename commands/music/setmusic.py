from utils.embeds import send_executed_embed


class SetMusicCmd():
    def __init__(self, client, manager):
        self.client = client
        self.manager = manager

    async def run(self, message, args):
        server_id = message.server.id
        channel = message.channel
        try:
            if args:
                if args[0] == 'mute':
                    self.manager.server_managers[f'{server_id}'].textch = None

                    await send_executed_embed(self.client, message,
                                              command='setmusic',
                                              text='I won\'t send any'
                                                   'music command reply.')
            else:
                self.manager.server_managers[f'{server_id}'].textch = channel

                await send_executed_embed(self.client, message,
                                          command='setmusic',
                                          text='The channel I will be replying'
                                               'music commands is now'
                                               f'{channel.mention}.')
        except KeyError:
            pass
