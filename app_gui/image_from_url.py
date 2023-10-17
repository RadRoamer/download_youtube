import io
import customtkinter as ctk
from PIL import Image
import requests
from requests import HTTPError, ConnectionError
from typing import Tuple

IMG_URL = 'https://www.google.com/images/branding/googlelogo/1x/googlelogo_color_272x92dp.png'
NON_IMG_URL = 'https://habr.com/ru/companies/otus/articles/481806/'


def load_by_url(url: str) -> bytes:
    """
    Load image from the url
    :param url: link to download image from internet
    :return: image in byte representation
    """

    try:
        response = requests.get(url)
        if response.status_code == 200:  # check if the connection is successful
            return response.content
        else:
            raise ValueError('connection is not successful')
    except ConnectionError:
        raise ConnectionError('cannot connect to internet')
    except HTTPError:
        raise HTTPError('cannot connect to server')
    except ValueError:
        raise ValueError(f'following url= ({url}) is incorrect!')


def load_image(url, size: Tuple[int, int] = (100, 100)) -> ctk.CTkImage:
    """
    :param url: link to download image from internet
    :param size: image size (should be a tuple of two int`s)
    :return: CTKImage object
    """

    thumbnail = Image.open(io.BytesIO(load_by_url(url)))

    return ctk.CTkImage(thumbnail, size=size)


def template_ctk():
    window = ctk.CTk()
    window.geometry('800x600')

    image = load_image(IMG_URL)

    label = ctk.CTkLabel(window, image=image)
    label.pack()

    window.mainloop()


if __name__ == '__main__':
    template_ctk()
