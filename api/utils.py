import textwrap as tw


def strip_line(text, line_length=100):
    if not isinstance(text, str):
        text = str(text)
    dedented_text = tw.dedent(text).strip()
    return tw.fill(dedented_text, width=line_length)


def get_yt_link(yt_id: str, yt_type='video'):
    if yt_type == 'video':
        return 'http://youtube.com/watch?v=' + yt_id
    elif yt_type == 'playlist':
        return 'https://www.youtube.com/playlist?list=' + yt_id


