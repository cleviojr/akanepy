import discord
from commands.utils.core import Runner

class MainListener():
    def __init__(self, client, manager):
        self.client  = client
        self.manager = manager

        @self.client.event
        async def on_ready():
            connected_servers = 0
            for j in self.client.servers: 
                connected_servers += 1
            
            message = f'Online for {connected_servers} servers.'
            print(message)
            await self.client.change_presence(game=discord.Game(name=message))

        @self.client.event
        async def on_message(message):
            # the bot is not parsing non command-like messages
            content     = message.clean_content
            not_command = not content or content[0] is not '!' or message.author.bot
            if not_command:
                return

            print('New command detected.')
            command = Runner(self.client, message, self.manager)
            await command.run()

        #@self.client.event on server join on server leave
