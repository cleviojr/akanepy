from commands.utils.youtube import Youtube

class PlayCmd():
    def __init__(self, client, manager):
        self.client  = client
        self.manager = manager

    async def run(self, message, args):
        author_voicech = message.author.voice.voice_channel
        server         = message.server

        if self.client.is_voice_connected(server):
            voice_client = self.client.voice_client_in(server)
        else:
            voice_client = await self.client.join_voice_channel(author_voicech)
        
        bot_voicech = voice_client.channel

        if author_voicech:
            if not bot_voicech == author_voicech:
                await voice_client.move_to(author_voicech)

            if not f'{server.id}' in self.manager.server_managers.keys():
                await self.manager.insert_server_and_play(self.client, message.channel, Youtube().search(' '.join(args)))
            else:
                await self.manager.server_managers[f'{server.id}'].play(Youtube().search(' '.join(args)))
