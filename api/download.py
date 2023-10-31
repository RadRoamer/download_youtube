from pytube import Playlist, YouTube
from api.setup import DEFAULT_DOWN_PATH, youtube
from api.utils import get_yt_link
from api.json_utils import find_key, find_all_keys
from customtkinter import CTkTextbox
from app_gui.videobutton import VideoButton
from pytube import YouTube


def download_video(path: str, yt_obj: YouTube = None, quality='144p',
                   textbox: CTkTextbox = None, yt_id: str = '') -> str:
    """
    download the requested video by URL with the
    required file path and the required video quality
    :param yt_id: id of the video
    :param path: path in the root file system where the video will be stored
    :param yt_obj: instance of VideoButton class
    :param quality: quality of the video (144p, 360p, 720p, etc.)
    :param textbox: instance of textbox to display current information
    :return: returns the path where the file is stored as a sign that the function completed successfully
    """
    if not yt_id and not yt_obj:
        raise ValueError(
            'At least one of the parameters (yt_id or yt_obj) must be filled in')

    if not isinstance(yt_obj, YouTube):
        # create a full  url link (which starts with 'https://')
        link = get_yt_link(yt_id, 'video')
        yt_obj = YouTube(link)

    # find stream with required quality
    stream = yt_obj.streams.filter(res=quality).first()
    textbox.insert('end', f'Downloading: {yt_obj.title} ...\n')
    print(f'Downloading: {yt_obj.title} ...')

    stream.download(output_path=path)  # download stream
    textbox.insert('end', 'video downloaded successfully!!\n')
    print('video downloaded successfully!!')

    return path


def download_playlist(yt_id: str, path: str = DEFAULT_DOWN_PATH, quality='144p'):
    """
    The same as video download function, but for full playlist
    :param yt_id: id of the playlist
    :param path: path in the root file system where the video will be stored
    :param quality: quality of each video (144p, 360p, 720p, etc.)
    :return: returns the path where the videos are stored as a sign that the function completed successfully
    """
    # create a full  url link (which starts with 'https://')
    link = get_yt_link(yt_id, 'playlist')
    p = Playlist(link)

    length = len(p.videos)  # count of all videos in playlist

    # download all videos one by one
    for idx, video in enumerate(p.videos, start=1):
        download_video(video.video_id(), path, quality)
        print(f'download {idx}/{length} videos...')

    print(f'playlist {p.title} was successful downloaded!')
    return path


def download_channel(yt_id, path: str = DEFAULT_DOWN_PATH, quality='144p'):
    next_page_token = None

    # find info about channel
    channel_response = youtube.channels().list(
        part='contentDetails',
        id=yt_id
    ).execute()

    uploads_playlist_id = find_key('uploads', channel_response)
    # looping until  all the videos are downloaded.
    while True:
        pl_response = youtube.playlistItems().list(
            part="contentDetails",
            playlistId=uploads_playlist_id,
            maxResults=50,
            pageToken=next_page_token
        ).execute()

        video_ids = find_all_keys('videoId', pl_response)
        for v in video_ids:
            download_video(v, path, quality)

        next_page_token = pl_response.get('nextPageToken')
        if not next_page_token:  # if token is None, end the loop
            break


def video_res(vid_id: str, butt: VideoButton = None):
    video = YouTube(get_yt_link(vid_id, 'video'))
    if butt:
        butt.Youtube = video

    # got unique values
    res = {x.resolution for x in video.streams if x.resolution}
    # sort values in descending order by digits
    return sorted(res, key=lambda x: int(x[:-1]), reverse=True)


if __name__ == '__main__':
    video_id = get_yt_link('MunPNYumw6M')
    print(video_res(video_id))
