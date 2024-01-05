from api.utils import get_yt_link
from api.json_utils import find_key, find_all_keys
import yt_dlp as ytd


def dlp_video(link, vid_name, res, path):
    """
    a function that allows you to download videos through the  yt-dlp library
    :param link: full url-link of the YouTube video
    :param vid_name: title of the video
    :param res: required resolution
    :param path: path to the saved directory
    :return: None
    """
    options = {
        'format': f'bestvideo[height<={res}]+bestaudio[ext=m4a]/best[ext=mp4]/best',
        'outtmpl': f'{path}\\{vid_name}.mp4'  # Название сохраняемого файла
    }

    # create an YouTubeDl object via context manager
    with ytd.YoutubeDL(options) as yt:
        # get webpage url
        result = yt.extract_info(link, download=False)
        if 'entries' in result:  # if more than one result was found
            video_info = result['entries'][0]
        else:
            video_info = result

        yt.download([video_info['webpage_url']])


def download_video(inst, path: str, yt_id, progress_val):
    """
    download the requested video by URL with the
    required file path and the required video quality
    :param progress_val: a progress bar value
    :param inst: instance of a class (PlaylistWindow, VideoFrame, etc.)
    :param yt_id: id of video
    :param path: path in the root file system where the video will be stored
    """

    # create a full  url link (which starts with 'https://')
    link = get_yt_link(yt_id)
    extract_options = {
        "extract_flat": True
    }
    quality = inst.combobox_var.get()  # get quality label from combobox
    # Create yt-dlp object
    with ytd.YoutubeDL(extract_options) as extr:
        title = find_key('title', extr.extract_info(link, download=False))

    inst.textbox.insert('end', f'Downloading: {title} ...\n')
    # download video with yt-dlp library
    dlp_video(link, title, quality, path)

    inst.textbox.insert('end', 'video downloaded successfully!!\n')
    inst.info.progressbar.set(progress_val)


def download_playlist(inst, path: str):
    """
    The same as video download function, but for full playlist
    :param inst: instance of a class PlaylistWindow
    :param path: path in the root file system where the video will be stored
    """

    length = len(inst.ids)
    progress = (100 / length) * .01
    # download all videos one by one
    inst.textbox.configure(state='normal')
    start = f"""
downloading videos from next playlist: {inst.title}\n
{'*' * 78}
    """
    inst.textbox.insert('end', start)
    for idx, yt_id in enumerate(inst.ids, start=1):
        value = progress * idx
        download_video(inst, path, yt_id, value)
        inst.textbox.insert(
            'end', f'downloaded {idx}/{length} videos...\n')

    end = f"""
playlist {inst.title} was successful downloaded!!!\n
{'*' * 78}\n
    """
    inst.textbox.insert('end', end)

    inst.textbox.configure(state='disabled')


def get_res(inst):
    # create a full  url link (which starts with 'https://')
    link = get_yt_link(inst.dedicated_butt.yt_id)
    extract_options = {
        'format': 'best'
    }

    # Создайте объект yt-dlp
    with ytd.YoutubeDL(extract_options) as extr:
        # extract info from webpage
        info = extr.extract_info(link, download=False)
        # find all available resolutions for the video
        res = find_all_keys('height', info)
        # get only well-known resolutions (144, 360, 720p, etc.)
        res = {x for x in res if x and x % 12 == 0}
        # convert values to string because combobox works only with str
        res = [str(x) for x in sorted(res, reverse=True)]

        inst.combobox.configure(values=res, state='normal')
        inst.combobox_var.set(res[0])

        inst.download_button.configure(state='normal')


if __name__ == '__main__':
    pass
