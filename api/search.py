import yt_dlp as ytd
from youtubesearchpython import (
    PlaylistsSearch,
    VideosSearch,
    Playlist)
from api.json_utils import find_all_keys
from api.utils import get_yt_link
import threading as thr
from api.utils import yt_get_attrs


def multithread_task(func, *args, **kwargs):
    """
    a function that creates a separate thread (performing a another function),
    so that the main application (tkinter) does not stop
    :param func: function, that executed in another thread
    :param args: optional arguments, passed to the function
    :param kwargs: keyword arguments passed to the function
    :return: None
    """
    # create the distinct thread with required parameters
    thread = thr.Thread(target=func,
                        args=(*args,),
                        kwargs=kwargs)

    thread.start()  # start the thread


def yt_search(yt_type, query, max_results=5):
    search_dict = {0: VideosSearch, 1: PlaylistsSearch}

    response = search_dict[yt_type](query, limit=max_results).result()

    return yt_get_attrs(response['result'][:max_results])


def get_playlist_videos(pl_id: str):
    """
    get all videos in required playlist and placed them into toplevel window
    :param pl_id: id of the required playlist
    """

    link = get_yt_link(pl_id, 'playlist')  # get full link
    playlist = Playlist(playlistLink=link)

    # list throw all videos in playlist
    return yt_get_attrs(playlist.videos)


def get_res(yt_id):
    # create a full  url link (which starts with 'https://')
    link = get_yt_link(yt_id)

    with ytd.YoutubeDL({'format': 'best'}) as extr:
        # extract info from webpage
        info = extr.extract_info(link, download=False)
        # find all available resolutions for the video
        res = find_all_keys('height', info)
        # get only well-known resolutions (144, 360, 720p, etc.)
        res = {x for x in res if x and x % 12 == 0}
        # sort set and convert values to string because combobox works only with str
        res = [str(x) for x in sorted(res, reverse=True)]

    return res


if __name__ == '__main__':
    for i in yt_search(0, 'youtube rewind 2016'):
        print(i)
