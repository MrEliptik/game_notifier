import os

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
        channel = discord.utils.get(client.get_all_channels(), name="🌟┃general")
        channel_id = channel.id
        print(channel_id)
        target_channel = self.get_channel(channel_id)
        await channel.send("HELLO WORLD")

    async def on_message(self, message):
        print(f'Message from {message.author}: {message.content}')
        parse_command(message.content)

    def parse_command(msg):
        if not msg.startswith('!'): return

# @bot.command()
# async def stream(ctx):
#     pass
        

intents = discord.Intents.default()
intents.message_content = True

# client = MyClient(intents=intents)
# client.run('MTAxNzU0MTQ5ODQ4NjY3MzQ2OQ.GUvqFH.bczIg2WzxwcQ-SKhU_EGIgBlQq4t2lPe63wA2A')

# bot = commands.Bot(command_prefix='/')
# bot.add_command(stream)

bot = commands.Bot(command_prefix='/', intents=intents)

@bot.hybrid_command(name="stream", guild_ids=['847213579870797828']) #Add the guild ids in which the slash command will appear. If it should be in all, remove the argument, but note that it will take some time (up to an hour) to register the command if it's for all guilds.
async def stream(ctx, arg):
    # arguments = ' '.join(args)
    arguments = arg
    game_id = twitch.get_games(names=[arguments])
    print(game_id['data'][0]['id'])

    streams = twitch.get_streams(game_id=[game_id['data'][0]['id']], first=100)
    nb_streams = len(streams['data'])
    max_viewer = 0
    max_viewer_link = ""
    max_viewer_name = ""
    max_viewer_title = ""
    for d in streams['data']:
        if d['viewer_count'] > max_viewer:
            max_viewer = d['viewer_count']
            max_viewer_link = "https://twitch.tv/"+d['user_login']
            max_viewer_name = d['user_name']
            max_viewer_title = d['title']
    resp = f'There are **{nb_streams}** streams on **{arguments}**!\n**{max_viewer_name}** is the most watched streamer with **{max_viewer}** viewers.\n\n🔴 Stream title: *{max_viewer_title}*\n🔗 Link: {max_viewer_link}'
    await ctx.send(resp)

bot.run(DISCORD_BOT_TOKEN)