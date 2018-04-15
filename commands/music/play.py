from commands.utils.youtube import Youtube
from urllib.parse import urlparse
from utils.embeds import send_failed_embed


class PlayCmd():
    def __init__(self, client, manager):
        self.client = client
        self.manager = manager

    async def run(self, message, args):
        author_voicech = message.author.voice.voice_channel
        if not author_voicech:
            await send_failed_embed(self.client, message,
                                    command='play',
                                    text='You are not in a voice channel.')
            return
        current_server = message.server

        # checks the channel, connects, etc
        if self.client.is_voice_connected(current_server):
            voice_client = self.client.voice_client_in(current_server)
        else:
            voice_client = await self.client.join_voice_channel(author_voicech)

        bot_voice_channel = voice_client.channel

        # checks where the author is, so she can move
        if author_voicech:
            if not bot_voice_channel == author_voicech:
                await voice_client.move_to(author_voicech)

            # checks current server in dict of server_id->servermanager
            if f'{current_server.id}' not in self.manager.managers.keys():
                self.manager.insert_server(self.client, message.channel)

            server_mng = self.manager.managers[f'{current_server.id}']

            """
                checks if it is a youtube link, playlist,
                common video, or search query
            """
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
                        await server_mng.load_playlist(playlist_id,
                                                       start_index=index)
                    elif '/playlist' in url.path:
                        playlist_id = url.query.split('=')[1]
                        await server_mng.load_playlist(playlist_id)

                    return
                else:
                    if '/watch' in url.path:
                        video_id = url.query.split('=')[1]
                        await server_mng.add_to_playlist(video_id,
                                                         None,
                                                         message)
            else:
                video_id, video_title = Youtube().search(' '.join(args))
                await server_mng.add_to_playlist(video_id,
                                                 video_title,
                                                 message)
