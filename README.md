# Game notifier

*DISCLAIMER: This is a WIP. The scripts and github action works but are undocumented for now.*

[![youtube-check](https://github.com/MrEliptik/game_notifier/actions/workflows/youtube-check.yml/badge.svg)](https://github.com/MrEliptik/game_notifier/actions/workflows/youtube-check.yml)

Two python scripts to check Twitch and Youtube for livestreams and videos about a game running on GitHub action to send the result with a Discord Bot.

## 🧰 Setup

### 🟣 Twitch

- **Step 1 - Create a Twitch application**

    - *TODO*

- **Step 2 - Create a Discord bot**

    - *TODO*

- **Step 3 - Setups GitHub env variables**

    - *TODO*

- **Step 4 - Setup the GitHub action**

    - *TODO*

### 📹 Youtube

- **Step 1 - Get a YouTube API key**

    - *TODO*

- **Step 2 - Create a Discord bot**

    - *TODO*

- **Step 3 - Setups GitHub env variables**

    - *TODO*

- **Step 4 - Setup the GitHub action**

    - *TODO*

## ⚙️ How it works

### 🟣 Twitch

The python script calls the [Twitch API](https://dev.twitch.tv/docs/api/reference) to get the livestreams in a category. It compares the result with the latest run, stored in [streams_list.json](streams_list.json) to check if there are new livestreams to announce.

If new streams should be announced, it connects to the [Discord API](https://discordpy.readthedocs.io/en/stable/api.html) to send a message in a specific channel.

### 📹 Youtube

The python scripts calls the [YouTube API](https://developers.google.com/youtube/v3/docs/videos/list) to get the new videos after a certain date. The date is read from the last run, and corresponds to the last video found. 

It checks to see if there are new videos and if there are, it sends the new videos using the [Discord API](https://discordpy.readthedocs.io/en/stable/api.html) in a specific channel.


## 📝 TODO

- [ ] Update readme with setup instructions
- [ ] Choose a license
- [X] Use arguments to pass game list
- [X] Move Twitch app ID to environment variable

## About me

Full time indie gamedev 🎮

- [Discord](https://discord.gg/83nFRPTP6t)
- [YouTube](https://www.youtube.com/c/MrEliptik)
- [TikTok](https://www.tiktok.com/@mreliptik)
- [Twitter](https://twitter.com/mreliptik_) 
- [Instagram](https://www.instagram.com/_mreliptik)
- [Itch.io](https://mreliptik.itch.io/)

If you enjoyed this project and want to support me:

<a href='https://ko-fi.com/H2H23ODS7' target='_blank'><img height='36' style='border:0px;height:36px;' src='https://cdn.ko-fi.com/cdn/kofi1.png?v=3' border='0' alt='Buy Me a Coffee at ko-fi.com' /></a>

## LICENSE & Credits

*TODO*
