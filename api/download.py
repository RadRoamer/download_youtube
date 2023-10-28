from pytube import Playlist, YouTube
from api.setup import DEFAULT_DOWN_PATH, youtube
from api.utils import get_yt_link
from api.json_utils import find_key, find_all_keys


def download_video(yt_id: str, path=DEFAULT_DOWN_PATH, quality='144p') -> str:
    """
    download the requested video by URL with the
    required file path and the required video quality
    :param yt_id: id of the video
    :param path: path in the root file system where the video will be stored
    :param quality: quality of the video (144p, 360p, 720p, etc.)
    :return: returns the path where the file is stored as a sign that the function completed successfully
    """
    # create a full  url link (which starts with 'https://')
    link = get_yt_link(yt_id, 'video')
    yt = YouTube(link)

    # find stream with required quality
    stream = yt.streams.filter(res=quality).first()
    print(f'Downloading {yt.title} ...')

    stream.download(output_path=path)  # download stream
    print('video downloaded successful!!')

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

    channel_response = youtube.channels().list(
        part='contentDetails',
        id=yt_id
    ).execute()

    uploads_playlist_id = find_key('uploads', channel_response)

    playlist_items = youtube.playlistItems().list(
        part="contentDetails",
        playlistId=uploads_playlist_id,
        maxResults=1
    ).execute()

    video_ids = find_all_keys('videoId', playlist_items)
    for v in video_ids:
        download_video(v, path, quality)


if __name__ == '__main__':
    pl_link = get_yt_link('PL5d6bqDAwb48UxlX7FsGatmZAdcVuRQH9', 'playlist')
    playlist = Playlist(pl_link)
    length = len(playlist.videos)
    print(length)
