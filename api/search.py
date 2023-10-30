from api.setup import youtube
from api.json_utils import find_key, find_all_keys
from api.utils import strip_line


class YouTube:
    """
    simple data container of YouTube objects, that contains title,
    thumbnail_url, and unique id, that can represent
    video, playlist or channel
    """
    def __init__(self, *args, **kwargs):
        self.title = kwargs.get('title')
        self.thumbnail = kwargs.get('thumbnail')
        self.yt_id = kwargs.get('yt_id')

    def __str__(self):
        return f'{self.title}, {self.thumbnail}, {self.yt_id}'


def yt_search(search_request, search_type, max_results=5):
    """
    This function searches for YouTube videos via YouTube data api and
    returns a list of results as objects including title, thumbnail, and ID.
    :param search_request: a string that`s represent the search query
    :param search_type: type of required request (video, playlist or full channel)
    :param max_results: required number of results
    :return: list of YouTube objects
    """

    s_types = {
        0: ('video', 'videoId'),
        1: ('playlist', 'playlistId'),
        2: ('channel', 'channelId')}

    if isinstance(search_type, int):
        search_type = s_types[search_type]

    search_response = youtube.search().list(
        q=search_request,
        type=search_type[0],
        part='snippet',
        maxResults=max_results
    ).execute()
    if search_type[1] == 'channelId':
        yt_ids = find_all_keys('channelId', find_all_keys('snippet', search_response))
    else:
        yt_ids = find_all_keys(search_type[1], search_response)

    titles = find_all_keys('title', search_response)

    thumbnails = find_all_keys('thumbnails', search_response)
    thumbnails = [find_key('medium', x)['url'] for x in thumbnails]

    youtube_list = [YouTube(title=t, thumbnail=th, yt_id=yt_id)
                    for t, th, yt_id in zip(titles, thumbnails, yt_ids)]

    return youtube_list


def check_channel(ch_id):
    next_page_token = None
    results_count = 0
    channel_response = youtube.channels().list(
        part='contentDetails',
        id=ch_id
    ).execute()

    uploads_playlist_id = find_key('uploads', channel_response)
    playlist_items = youtube.playlistItems().list(
        part="contentDetails",
        playlistId=uploads_playlist_id,
        maxResults=50,
        pageToken=next_page_token
    ).execute()

    results_count = find_key('totalResults', playlist_items)
    print(results_count)


if __name__ == '__main__':
    pass

