from youtubesearchpython import PlaylistsSearch, VideosSearch, Playlist
from api.json_utils import find_key
from api.utils import get_yt_link
import customtkinter as ctk
import threading as thr
from app_gui.image_from_url import load_image
from app_gui.videobutton import VideoButton


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


def parallel_task(instance, func, *args, **kwargs):
    """
    a function that creates a separate thread (performing a another function),
    so that the main application (tkinter) does not stop
    :param instance: instance of a class (App, VideoFrame, etc.)
    :param func: function, that executed in another thread
    :param args: optional arguments, passed to the function
    :param kwargs: keyword arguments passed to the function
    :return: None
    """
    # create the distinct thread with required parameters
    thread = thr.Thread(target=func,
                        args=(instance, *args),
                        kwargs=kwargs)

    thread.start()  # start the thread


def yt_search(inst: ctk.CTk, max_results=5):
    """
    This function searches for YouTube videos via youtubesearchpython
    :param inst: instance of an App class
    :param max_results:  required number of results
    """

    inst.search_button.configure(state='disabled')
    # self.entry.get(), self.type_var.get()
    if inst.type_var.get() == 0:  # video search
        response = VideosSearch(inst.entry.get(), limit=max_results).result()
    elif inst.type_var.get() == 1:  # playlist search
        response = PlaylistsSearch(inst.entry.get(), limit=max_results).result()
    else:
        raise ValueError('invalid search type (expected value 0 or 1')

    youtube_list = []
    for r in response['result']:
        title = find_key('title', r)
        yt_id = find_key('id', r)
        thumb = find_key('url', find_key('thumbnails', r))
        youtube_list.append(YouTube(title=title, thumbnail=thumb, yt_id=yt_id))

    for v in youtube_list:
        # trim string if it's too long
        title = v.title if len(v.title) < 45 else v.title[:42] + '...'

        image = load_image(v.thumbnail)  # load video thumbnail

        button = VideoButton(master=inst.scroll_frame, text=title,
                             yt_id=v.yt_id, image=image, anchor='w')
        button.bind('<Button-1>',
                    lambda event, b=button: inst.select_button(b))
        button.pack(padx=10, pady=10)

        inst.search_button.configure(state='normal')


def get_playlist_videos(inst, pl_id: str):
    """
    get all videos in required playlist and placed them into toplevel window
    :param inst: instance of a PlaylistFrame class
    :param pl_id: id of the required playlist
    """
    youtube_list = []

    link = get_yt_link(pl_id, 'playlist')  # get full link
    playlist = Playlist(playlistLink=link)

    # list throw all videos in playlist
    for v in playlist.videos:
        title = find_key('title', v)
        pl_id = find_key('id', v)
        thumb = find_key('url', find_key('thumbnails', v))
        youtube_list.append(YouTube(title=title, thumbnail=thumb, yt_id=pl_id))

    inst.videos = youtube_list
    # display videos as VideoButton class in scrollable frame
    inst.toplevel.scroll_frame.display_results(
            inst.videos, inst.toplevel_selected)
    inst.combobox_var.set(value=inst.res[0])


if __name__ == '__main__':
    pass