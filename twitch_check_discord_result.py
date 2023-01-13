import os
import json
import time
import argparse

import discord
from discord.ext import commands

from twitchAPI.twitch import Twitch

# https://github.com/Teekeks/pyTwitchAPI

# get secrets from environment variables
TWITCH_SECRET = os.environ.get("TWITCH_SECRET")
TWITCH_APPID = os.environ.get("TWITCH_APPID")
DISCORD_BOT_TOKEN = os.environ.get("DISCORD_BOT_TOKEN")

# create instance of twitch API and create app authentication
twitch = Twitch(TWITCH_APPID, TWITCH_SECRET)

# https://discordpy.readthedocs.io/en/stable/intro.html

class MyClient(discord.Client):
    async def on_ready(self):
        print(f'Logged on as {self.user}!')
        channel = discord.utils.get(self.get_all_channels(), name="📹steam-videos-notifier")
        channel_id = channel.id
        print(channel_id)
        self.target_channel = self.get_channel(channel_id)
        await self.send_message(channel_id, message)

    async def send_message(self, channel_id, message):
        #resp = f'There are **{nb_streams}** streams on **Dashpong**!\n**{max_viewer_name}** is the most watched streamer with **{max_viewer}** viewers.\n\n🔴 Stream title: *{max_viewer_title}*\n🔗 Link: {max_viewer_link}'
        #asyncio.get_event_loop().create_task(channel.send(resp))
        #channel = client.get_channel(channel_id)
        await self.target_channel.send(message)
        await self.close()

def read_game_list(filepath):
    with open(filepath) as f:
        data = json.load(f)
    return data

def write_game_list(data, filepath):
    with open(filepath, 'w') as f:
        json.dump(data, f, ensure_ascii=False)

def get_streams_of_games(game_names):
    game_id = twitch.get_games(names=game_names)
    # Get all the streams
    streams = twitch.get_streams(game_id=[game_id['data'][0]['id']], first=100)
    return streams

def check_for_new_stream(streams):
    # Load the streams from the previous script run
    # Check first if file exists
    if os.path.isfile("streams_list.json"):
        past_streams_list = read_game_list("streams_list.json")["streams"]
    else:
        past_streams_list = None

    print("Past stream: ", past_streams_list)

    new_streams_list = []
    streams_to_notify = []
    # Compare to this which stream is new, or deleted
    if past_streams_list != None:
        for d in streams['data']:
            id = d['id']
            new_streams_list.append(id)
            # Stream is still in list, do nothing
            if id in past_streams_list:
                pass
            # Stream wasn't in list, it's a new one!
            else:
                streams_to_notify.append(d)
    else:
        for d in streams['data']:
            id = d['id']
            streams_to_notify.append(d)

    new_data = {
        "timestamp": time.time(),
        "streams": new_streams_list
    }

    # Update and write the streams list
    write_game_list(new_data, "streams_list.json")

    return streams_to_notify

def main():
    # Used to modify global var
    global message

    parser = argparse.ArgumentParser(
                    prog = 'Twitch check Discord bot',
                    description = 'Check Twitch for livestream of the specified game and send a notification on discord')
    parser.add_argument('game_name')           # positional argument

    args = parser.parse_args()

    streams = get_streams_of_games([args.game_name])
    new_streams = check_for_new_stream(streams)

    print("New streams: ", streams)
    print("Streams notification: ", new_streams)

    if len(new_streams) == 0:
        return

    elif len(new_streams) == 1:
        user_name = new_streams[0]['user_name']
        viewers = new_streams[0]['viewer_count']
        title = new_streams[0]['title']
        link = "https://twitch.tv/"+new_streams[0]['user_login']
        message = f'Someone is streaming **{args.game_name}**!\n**{user_name}** is streaming with **{viewers}** viewers.\n\n🔴 Stream title: *{title}*\n🔗 Link: {link}'
    else:
        max_viewer = 0
        max_viewer_link = ""
        max_viewer_name = ""
        max_viewer_title = ""
        for d in new_streams:
            if d['viewer_count'] > max_viewer:
                max_viewer = d['viewer_count']
                max_viewer_link = "https://twitch.tv/"+d['user_login']
                max_viewer_name = d['user_name']
                max_viewer_title = d['title']
        streams_count = len(new_streams)
        message = f'There are **{streams_count}** streams on **{args.game_name}**!\n**{max_viewer_name}** is the most watched streamer with **{max_viewer}** viewers.\n\n🔴 Stream title: *{max_viewer_title}*\n🔗 Link: {max_viewer_link}'

    intents = discord.Intents.default()
    intents.message_content = True
    client = MyClient(intents=intents)
    client.run(DISCORD_BOT_TOKEN)

message = ""

if __name__ == "__main__":
    main()
    