from commands.utils.youtube import Youtube
from urllib.parse           import urlparse

class PlayCmd():
    def __init__(self, client, manager):
        self.client  = client
        self.manager = manager

    async def run(self, message, args):
        author_voice_channel = message.author.voice.voice_channel
        current_server       = message.server

        #checks the channel, connects, etc
        if self.client.is_voice_connected(current_server):
            voice_client = self.client.voice_client_in(current_server)
        else:
            voice_client = await self.client.join_voice_channel(author_voice_channel)
        
        bot_voice_channel = voice_client.channel

        #checks where the author is, so she can move
        if author_voice_channel:
            if not bot_voice_channel == author_voice_channel:
                await voice_client.move_to(author_voice_channel)

            #checks current server in dict of server_id->servermanager
            if not f'{current_server.id}' in self.manager.server_managers.keys():
                self.manager.insert_server(self.client, message.channel)

            current_server_manager = self.manager.server_managers[f'{current_server.id}']
            #checks if it is a youtube link, playlist, common video, or a video search
            url = urlparse(args[0])
            if url.netloc == 'youtube.com' or url.netloc == 'www.youtube.com':
                if 'list=' in url.query:
                    if '/watch' in url.path:
                        split = url.query.split('&')
                        index = None
                        for j in split:
                            if j.startswith('t='):
                                split.remove(j)
                            if j.startswith('index='):                               
                                index = int(j.split('=')[1])
                                split.remove(j)

                        playlist_id = split[1].split('=')[1]
                        await current_server_manager.load_playlist(playlist_id, start_index=index)
                    elif '/playlist' in url.path:
                        playlist_id = url.query.split('=')[1]
                        await current_server_manager.load_playlist(playlist_id)

                    return
                else:
                    if '/watch' in url.path:
                        video_id = url.query.split('=')[1]            
            else:
                video_id = Youtube().search(' '.join(args))

            await current_server_manager.add_to_playlist(video_id)
