import customtkinter as ctk
from customtkinter import CTkScrollableFrame, CTkEntry
import pytube as pt
from videobutton import VideoButton
from image_from_url import load_image
from typing import Tuple

ctk.set_default_color_theme("dark-blue")
ctk.set_appearance_mode('dark')


def find_videos(search: str) -> Tuple[list, list, list]:
    """
    found videos by search request (request must be a string)
    :param search: a string represents a user
    :return:  thumbnail urls, video titles, channel_ids (all it`s a lists of strings)
    """

    # search videos by string request and choose first five results
    search = pt.Search(search)
    results = search.results[:5]

    # grab id`s thumbs and titles from each YouTube object in a list
    channel_ids = [x.channel_id for x in results]
    thumb_urls = [x.thumbnail_url for x in results]
    titles = [x.title for x in results]

    return thumb_urls, titles, channel_ids


class Frame(ctk.CTkFrame):
    def __init__(self, master, column,
                 row, weight, **kwargs):
        super().__init__(master, **kwargs)

        self.grid_columnconfigure(0, weight=weight)
        self.grid(column=column, row=row, padx=10)


class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.geometry('900x600')
        self.grid_columnconfigure(0, weight=1)

        self.search_frame = Frame(self, row=0, column=0,
                                  fg_color='transparent', weight=1)
        self.entry = CTkEntry(self.search_frame, placeholder_text='python', width=500)
        self.entry.grid(row=0, column=0, padx=20, pady=10)

        self.search_button = ctk.CTkButton(self.search_frame,
                                           text='search videos',
                                           state='disabled',
                                           command=self.display_results)
        self.search_button.grid(row=1, column=0, pady=10)

        self.scroll_frame = CTkScrollableFrame(self.search_frame, width=500, height=200)
        self.scroll_frame.grid(row=2, column=0)

        self.entry.bind("<KeyRelease>", self.check_entry_content)

    def display_results(self):
        """
        Display found videos on Scrollable Frame via CTkButton
        """
        # clear the scrollable frame
        for widget in self.scroll_frame.winfo_children():
            widget.destroy()

        # get video thumbnail, title and video id
        thumb_urls, titles, ids = find_videos(self.entry.get())

        for url, title, ch_id in zip(thumb_urls, titles, ids):
            # trim string if it's too long
            title = title if len(title) < 45 else title[:42] + '...'

            image = load_image(url)  # load video thumbnail

            button = VideoButton(master=self.scroll_frame, text=title,
                                 channel_id=ch_id, image=image, anchor='w')
            button.bind('<Button-1>', self.toggle_button)
            button.pack(padx=10, pady=10)

    def check_entry_content(self, *args):
        """
        Checks if an input field is empty
        """
        # Getting the content of ctkEntry
        entry_content = self.entry.get()

        # If the field is empty, deactivate the button, otherwise activate it
        if not entry_content:
            self.search_button.configure(state="disabled")
        else:
            self.search_button.configure(state="normal")

    def toggle_button(self, *args):
        pass


if __name__ == "__main__":
    app = App()
    app.mainloop()
