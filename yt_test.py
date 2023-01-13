import os
# API client library
import googleapiclient.discovery

# API information
api_service_name = "youtube"
api_version = "v3"
# API key
YT_SECRET = os.environ.get("YOUTUBE_SECRET")
# API client
youtube = googleapiclient.discovery.build(
    api_service_name, api_version, developerKey = YT_SECRET)
# 'request' variable is the only thing you must change
# depending on the resource and method you need to use
# in your query
request = youtube.search().list(
        part="id,snippet",
        type='video',
        q="Dashpong",
        videoDefinition='high',
        order='date',
        maxResults=100,
        publishedAfter="2022-09-08T11:00:05Z",
        fields="items(id(videoId),snippet(publishedAt,channelId,channelTitle,title,description))"
)


# Query execution
response = request.execute()
# Print the results
#print(response)
for item in response['items']:
    print(item)