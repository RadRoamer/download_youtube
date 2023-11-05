from youtubesearchpython import PlaylistsSearch, VideosSearch, Playlist
from api.json_utils import find_key, find_all_keys
from api.utils import get_yt_link
import time


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
    This function searches for YouTube videos via youtubesearchpython and
    returns a list of results as objects including title, thumbnail, and ID.
    :param search_request: a string that`s represent the search query
    :param search_type: type of required request (video, playlist or full channel)
    :param max_results: required number of results
    :return: list of YouTube objects
    """
    if search_type == 0:  # video search
        response = VideosSearch(search_request, limit=max_results).result()
    elif search_type == 1:  # playlist search
        response = PlaylistsSearch(search_request, limit=max_results).result()
    else:
        raise ValueError('invalid search type (expected value 0 or 1')

    youtube_list = []
    for r in response['result']:
        title = find_key('title', r)
        yt_id = find_key('id', r)
        thumb = find_key('url', find_key('thumbnails', r))
        youtube_list.append(YouTube(title=title, thumbnail=thumb, yt_id=yt_id))

    return youtube_list


def get_playlist_videos(pl_id: str):
    youtube_list = []

    link = get_yt_link(pl_id, 'playlist')
    playlist = Playlist(playlistLink=link)

    for v in playlist.videos:
        title = find_key('title', v)
        pl_id = find_key('id', v)
        thumb = find_key('url', find_key('thumbnails', v))
        youtube_list.append(YouTube(title=title, thumbnail=thumb, yt_id=pl_id))

    return youtube_list


if __name__ == '__main__':
    get_playlist_videos('PL6plRXMq5RAAb9gwGqmgAoA-KIr-7CMuz')
