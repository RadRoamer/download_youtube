import os
import re
from datetime import timedelta
from dotenv import load_dotenv
from googleapiclient.discovery import build
from json_utils import find_all_keys

load_dotenv()
API_KEY = os.getenv('API_KEY')
VERSION = 'v3'
NAME = 'youtube'
hour_pat, minute_pat, second_pat = (re.compile(fr'(\d+){x}') for x in 'HMS')


def get_total_seconds(videos):
    """
     get the total seconds of video length per pageToken
    :param videos: list of strings in specific format
    :return: floating point number of total time in seconds
    """
    videos = list(videos)
    videos_length = []
    for video in videos:
        hours = hour_pat.search(video)
        minutes = minute_pat.search(video)
        seconds = second_pat.search(video)

        hours = int(hours.group(1)) if hours else 0
        minutes = int(minutes.group(1)) if minutes else 0
        seconds = int(seconds.group(1)) if seconds else 0

        total_seconds = timedelta(
            hours=hours,
            minutes=minutes,
            seconds=seconds
        ).total_seconds()
        videos_length.append(total_seconds)
    return videos_length


def get_channel_name(youtube_api, channel_id: str):
    request = youtube_api.channels().list(
        part='snippet',
        id=channel_id
    )
    response = request.execute()
    # get the channel name from json
    channel_title = response['items'][0]['snippet']['title']
    return channel_title


def main():
    youtube = build(NAME, VERSION, developerKey=API_KEY)
    next_page_token = None
    total_seconds = 0
    channel_id = 'UCtLKO1Cb2GVNrbU7Fi0pM0w'

    while True:
        pl_request = youtube.playlistItems().list(
            part='contentDetails, snippet',
            playlistId='PLcDkQ2Au8aVNYsqGsxRQxYyQijILa94T9',
            maxResults=50,
            pageToken=next_page_token)
        pl_response = pl_request.execute()
        video_ids = find_all_keys('videoId', pl_response)
        videos_request = youtube.videos().list(
            part='contentDetails',
            id=','.join(video_ids)
        )
        videos_response = videos_request.execute()

        videos_length = find_all_keys('duration', videos_response)
        videos_length = get_total_seconds(videos_length)
        total_seconds += sum(videos_length)

        next_page_token = pl_response.get('nextPageToken')
        if not next_page_token:
            break

    minutes, seconds = divmod(total_seconds, 60)
    hours, minutes = divmod(minutes, 60)
    print(f'youtube channel: {get_channel_name(youtube, channel_id)}')
    print(f'total duration of playlist:', end=' ')
    print(f'Hours: {hours}, Minutes: {minutes}, Seconds: {seconds}')


if __name__ == '__main__':
    main()
