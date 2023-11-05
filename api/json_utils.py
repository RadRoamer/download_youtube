import json
from typing import List
from api.setup import youtube
from api.utils import strip_line


def json_write(json_obj, name: str):
    if not name.endswith('.json'):
        name = f'{name}.json'
    with open(name, 'w') as f:
        json.dump(json_obj, f, indent=3)


def json_load(filepath):
    with open(filepath, 'r') as f:
        json_dict = json.load(f)

    return json_dict


def find_all_keys(required_key: str, data) -> List:
    results = []

    if isinstance(data, dict):
        for key, value in data.items():
            if key == required_key:
                results.append(value)
            if isinstance(value, (dict, list)):
                results.extend(find_all_keys(required_key, value))
    elif isinstance(data, list):
        for item in data:
            results.extend(find_all_keys(required_key, item))

    return results


def find_key(required_key: str, seq):
    if not seq:
        return None
    if required_key in seq:
        return seq[required_key]
    if isinstance(seq, (list, dict)):
        for v in seq:
            if isinstance(seq, dict):
                v = seq[v]
            if isinstance(v, dict):
                result = find_key(required_key, v)
                if result:
                    return result
            elif isinstance(v, list):
                for idx, i in enumerate(v):
                    result = find_key(required_key, v[idx])
                    if result:
                        return result


if __name__ == '__main__':
    channel_name = 'python'
    search_request = youtube.search().list(
        q=channel_name,
        type='channel',
        part='snippet'
    )
    search_response = search_request.execute()
    key = 'thumbnails'
    info = find_all_keys(key, search_response)
    thumb_key = 'url'
    small_urls = find_all_keys('url', info)
    print(f'{key}: {small_urls}'.center(100), '+' * 70, sep='\n')
    print(strip_line(search_response, line_length=150))
