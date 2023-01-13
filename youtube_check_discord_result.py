import os
import json
import time
import argparse

import discord
from discord.ext import commands
import googleapiclient.discovery

# get secrets from environment variables
YT_SECRET = os.environ.get("YOUTUBE_SECRET")
DISCORD_BOT_TOKEN = os.environ.get("DISCORD_BOT_TOKEN")
DISCORD_APPID = os.environ.get("DISCORD_APPID")

# API information
api_service_name = "youtube"
api_version = "v3"
# API client
youtube = googleapiclient.discovery.build(
    api_service_name, api_version, developerKey = YT_SECRET)

last_video_file = "last_video.json"

message = ""


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
        await self.target_channel.send(message)
        await self.close()

def read_last_game(filepath):
    with open(filepath) as f:
        data = json.load(f)
    return data

def write_last_game(data, filepath):
    with open(filepath, 'w') as f:
        json.dump(data, f, ensure_ascii=False)

def get_videos_of_games(game_names, published_after):
    if published_after == None:
        request = youtube.search().list(
            part="id,snippet",
            type='video',
            q=game_names,
            videoDefinition='high',
            order='date',
            maxResults=100,
            fields="items(id(videoId),snippet(publishedAt,channelId,channelTitle,title,description))"
        )
    else:
        request = youtube.search().list(
            part="id,snippet",
            type='video',
            q=game_names,
            videoDefinition='high',
            order='date',
            maxResults=100,
            publishedAfter=published_after,
            fields="items(id(videoId),snippet(publishedAt,channelId,channelTitle,title,description))"
        )

    # Query execution
    response = request.execute()
    return response['items']

def check_for_new_videos(videos, last_video_id, last_date):
    print("Past video: ", last_video_id)
    print("Past date: ", last_date)

    videos_to_notify = []

    new_last_date = last_date
    new_last_video_id = last_video_id

    if last_date != None:
        if videos[0]['snippet']['publishedAt'] != last_date:
            new_last_date = videos[0]['snippet']['publishedAt']
            new_last_video_id = videos[0]['id']['videoId']
        for video in videos:
            if video['snippet']['publishedAt'] == last_date: 
                continue
            videos_to_notify.append(video)
    else:
        new_last_date = videos[0]['snippet']['publishedAt']
        new_last_video_id = videos[0]['id']['videoId']
        for video in videos:
            videos_to_notify.append(video)

    new_data = {
        "timestamp": time.time(),
        "publication_date": new_last_date,
        "video_id": new_last_video_id
    }

    # Update and write the streams list
    write_last_game(new_data, last_video_file)

    return videos_to_notify

def main():
    # Used to modify global var
    global message

    parser = argparse.ArgumentParser(
                    prog = 'YouTube check Discord bot',
                    description = 'Check youtube for new videos of the specified game and send a notification on discord')
    parser.add_argument('game_name')           # positional argument

    args = parser.parse_args()

    last_video_id = ""
    last_date = ""

    # Load the last video
    # Check first if file exists
    if os.path.isfile(last_video_file):
        last_video_id = read_last_game(last_video_file)["video_id"]
        last_date = read_last_game(last_video_file)["publication_date"]
        if last_date == "": last_date = None
    else:
        last_video_id = None
        last_date = None

    videos = get_videos_of_games(args.game_name, last_date)
    new_videos = check_for_new_videos(videos, last_video_id, last_date)

    print("New videos: ", videos)
    print("Videos notification: ", new_videos)

    if len(new_videos) == 0:
        return
    elif len(new_videos) == 1:
        title = new_videos[0]['snippet']['title']
        channel_name = new_videos[0]['snippet']['channelTitle']
        publication_date = new_videos[0]['snippet']['publishedAt']
        link = 'https://www.youtube.com/watch?v='+new_videos[0]['id']['videoId']
        message = f'New video about **Dashpong** by {channel_name}!\n\n📹Title: *{title}*\n🗓️Published on: {publication_date}\n🔗 Link: {link}'
    else:
        message = f'There are {len(new_videos)} videos about **Dashpong**!'
        for video in new_videos:
            title = video['snippet']['title']
            channel_name = video['snippet']['channelTitle']
            publication_date = video['snippet']['publishedAt']
            link = 'https://www.youtube.com/watch?v='+video['id']['videoId']
            message += f'\n\n📹Title: *{title}* by {channel_name}\n🔗 Link: {link}'
            if len(message) > 1700: break

    print(message)

    intents = discord.Intents.default()
    intents.message_content = True
    client = MyClient(intents=intents)
    client.run(DISCORD_BOT_TOKEN)

if __name__ == "__main__":
    main()
    