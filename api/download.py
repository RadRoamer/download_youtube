from pytube import YouTube
from api.utils import get_yt_link


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
    yt_obj = YouTube(link)

    inst.textbox.insert('end', f'Downloading: {yt_obj.title} ...\n')
    quality = inst.combobox_var.get()  # get quality label from combobox
    # find stream with required quality
    stream = yt_obj.streams.filter(res=quality).first()

    stream.download(output_path=path)  # download stream
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
    setup = f"""
downloading videos from next playlist: {inst.title}\n
{'*' * 80}\n
    """
    inst.textbox.insert('end', setup)
    for idx, yt_id in enumerate(inst.ids, start=1):
        value = progress * idx
        download_video(inst, path, yt_id, value)
        inst.textbox.insert(
            'end', f'downloaded {idx}/{length} videos...\n')

    punch = f"""
playlist {inst.title} was successful downloaded!!!\n
{'*' * 80}\n
    """
    inst.textbox.insert('end', punch)

    inst.textbox.configure(state='disabled')


def video_res(inst):
    """get all available resolution for specific video"""
    video = YouTube(get_yt_link(inst.dedicated_butt.yt_id))

    # got unique values
    res = {x.resolution for x in video.streams if x.resolution}
    # sort values in descending order by digits
    res = sorted(res, key=lambda x: int(x[:-1]), reverse=True)

    inst.combobox.configure(values=res, state='normal')
    inst.combobox_var.set(res[0])

    inst.download_button.configure(state='normal')


if __name__ == '__main__':
    pass
