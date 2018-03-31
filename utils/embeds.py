from discord import Embed, Colour
from datetime import datetime

embed_msg = Embed()
embed_msg.color = Colour(int('FFB6C1', 16))

async def send_playing_embed(client, textch, uploader, name, url):
    embed_msg.title = ':musical_note: Now Playing:'
    embed_msg.url = Embed.Empty
    embed_msg.description = f'[{name}](http://www.youtube.com/watch?v={url}).'
    embed_msg.set_footer(text=uploader)
    await client.send_message(textch, embed=embed_msg)

async def send_empty_playlist_embed(client, textch):
    embed_msg.title = 'The playlist is now empty.'
    embed_msg.url = Embed.Empty
    embed_msg.description = 'I won\'t leave the channel, '\
                            'feel free to play anything '\
                            'else when you feel like.'
    embed_msg.set_footer(text=Embed.Empty)
    await client.send_message(textch, embed=embed_msg)

async def send_playlist_extend_embed(client, textch, newsize):
    embed_msg.title = 'I just found a playlist from youtube.'
    embed_msg.url = Embed.Empty
    embed_msg.description = f'Playlist size is now {newsize}.'
    embed_msg.set_footer(text=Embed.Empty)
    await client.send_message(textch, embed=embed_msg)

async def send_executed_embed(client, message, command=None, text=None):
    embed_msg.title = f'Found !{command}.'
    embed_msg.url = Embed.Empty
    embed_msg.description = text
    embed_msg.set_footer(text=message.author.name,
                         icon_url=message.author.avatar_url)
    await client.send_message(message.channel, embed=embed_msg)

async def send_failed_embed(client, message, command=None, text=None):
    embed_msg.title = f'Failed to execute !{command}.'
    embed_msg.url = Embed.Empty
    embed_msg.description = text
    embed_msg.set_footer(text=message.author.name,
                         icon_url=message.author.avatar_url)
    await client.send_message(message.channel, embed=embed_msg)

async def send_nyaa_search(client, message, search):
    embed_msg.title = search.title
    embed_msg.url = search.url

    embed_msg.description = f"File size: `{search.file_size}`.\n"\
                            f"Upload date: `{search.upload_date}`.\n"\
                            'Seeders/Leechers:'\
                            f'`{search.seeders}/{search.leechers}`.\n'\
                            f"Download: [Torrent]({search.torrent}).\n"

    embed_msg.set_footer(text=message.author.name,
                         icon_url=message.author.avatar_url)
    await client.send_message(message.channel, embed=embed_msg)
