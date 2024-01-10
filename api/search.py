from youtubesearchpython import (
    PlaylistsSearch,
    VideosSearch,
    Playlist)
from api.json_utils import find_key
from api.utils import get_yt_link
import customtkinter as ctk
import threading as thr
from app_gui.image_from_url import load_image
from app_gui.videobutton import VideoButton
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
    srch_dict = {0: VideosSearch, 1: PlaylistsSearch}

    response = srch_dict[yt_type](query, limit=max_results).result()

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


if __name__ == '__main__':
    for i in yt_search(0, 'python'):
        print(i)
