from pprint import pprint
from twitchAPI.twitch import Twitch

# https://github.com/Teekeks/pyTwitchAPI

# get secrets from environment variables
TWITCH_SECRET = os.environ.get("TWITCH_SECRET")
TWITCH_APPID = os.environ.get("TWITCH_APPID")

# create instance of twitch API and create app authentication
twitch = Twitch(TWITCH_APPID, TWITCH_SECRET)

game_id = twitch.get_games(names=['Dashpong'])
game_id = twitch.get_games(names=['Splatoon 3'])
print(game_id['data'][0]['id'])

streams = twitch.get_streams(game_id=[game_id['data'][0]['id']])
pprint(streams)

videos = twitch.get_videos(game_id=[game_id['data'][0]['id']])
pprint(videos)

# for x in streams['data']:
#     print(x['user_name'])
#     print('https://twitch.tv/'+x['user_login'])