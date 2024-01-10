import api.json_utils as ju


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


def get_yt_link(yt_id: str, yt_type='video'):
    if yt_type == 'video':
        return 'http://youtube.com/watch?v=' + yt_id
    elif yt_type == 'playlist':
        return 'https://www.youtube.com/playlist?list=' + yt_id


def yt_get_attrs(iterable):
    yt_list = []
    for i in iterable:
        title = ju.find_key('title', i)
        yt_id = ju.find_key('id', i)
        thumb = ju.find_key('url', ju.find_key('thumbnails', i))
        yt_list.append(YouTube(title=title, thumbnail=thumb, yt_id=yt_id))
    return yt_list
