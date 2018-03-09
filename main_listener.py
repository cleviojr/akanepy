import discord
from commands.utils.core import Runner
import asyncio

class MainListener():   
    def __init__(self, client, manager):
        self.client            = client
        self.manager           = manager
        self.connected_servers = 0
        self.game              = ''

        @self.client.event
        async def on_ready():
            for j in self.client.servers: 
                self.connected_servers += 1
            
            await self.update_game()
            print(self.game)

        @self.client.event
        async def on_message(message):
            # the bot is not parsing non command-like messages
            content     = message.clean_content
            not_command = not content or content[0] is not '!' or message.author.bot
            if not_command:
                return

            print('Command prefix detected.')
            command = Runner(self.client, message, self.manager)
            await command.run()

        @self.client.event
        async def on_server_join(server):
            self.connected_servers += 1
            await self.update_game()

        @self.client.event
        async def on_server_remove(server):
            self.connected_servers -= 1
            await self.update_game()

    async def update_game(self):
        self.game = f'Online for {self.connected_servers} servers.'
        await self.client.change_presence(game=discord.Game(name=self.game)) 
