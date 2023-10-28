import customtkinter as ctk
from customtkinter import CTkScrollableFrame, CTkEntry, CTkButton
from api.download import download_video, download_playlist, download_channel
from api.search import yt_search
from app_gui.videobutton import VideoButton
from app_gui.image_from_url import load_image
from tkinter.filedialog import askdirectory

ctk.set_default_color_theme("dark-blue")
ctk.set_appearance_mode('dark')


class Frame(ctk.CTkFrame):
    def __init__(self, master, column, row,
                 columnspan=1, rowspan=1, weight=1, **kwargs):
        super().__init__(master, **kwargs)

        self.grid_columnconfigure(0, weight=weight)
        self.grid(column=column, row=row, rowspan=rowspan,
                  columnspan=columnspan, padx=10, pady=(0, 20))


class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.geometry('900x600')
        self.grid_columnconfigure((0, 1), weight=1)

        # class variables
        self.type_var = ctk.IntVar(value=0)
        self.path_var = ctk.StringVar(value=r'D:\\')
        self.id_var = ctk.StringVar(value='')

        self.search_frame = Frame(self, row=0, column=0, fg_color='transparent',
                                  columnspan=2, width=600)

        self.entry = CTkEntry(self.search_frame, placeholder_text='python',
                              width=500)
        self.entry.grid(row=0, column=0, padx=20, pady=(10, 0))

        # ------------------------> Control Buttons section
        self.buttons_frame = Frame(self.search_frame, row=1, column=0,
                                   fg_color='transparent')
        self.buttons_frame.grid()
        self.buttons_frame.grid_columnconfigure(0, weight=1)

        self.search_button = CTkButton(self.buttons_frame,
                                       text='search videos',
                                       state='disabled',
                                       command=self.search_results, )
        self.search_button.grid(row=1, column=0, pady=10, padx=(30, 70))

        self.download_button = CTkButton(self.buttons_frame,
                                         text='download',
                                         state='disabled',
                                         command=self.download_content)
        self.download_button.grid(row=1, column=1, pady=10, padx=(40, 10))
        # ------------------------>

        # ------------------------> Radio Buttons section
        self.radio_frame = Frame(self.search_frame, row=2, column=0,
                                 fg_color='transparent', height=100, width=500)

        self.radio_buttons = []
        for idx, text in enumerate(('video', 'playlist', 'channel')):
            b = ctk.CTkRadioButton(self.radio_frame,
                                   text=text, variable=self.type_var,
                                   value=idx, width=160)
            b.grid(row=0, column=idx)
            b.columnconfigure(0, weight=1)
            self.radio_buttons.append(b)
        # ------------------------>

        self.scroll_frame = CTkScrollableFrame(self.search_frame, width=500, height=200)
        self.scroll_frame.grid(row=3, column=0)

        self.entry.bind("<KeyRelease>", self.is_entry_empty)

    def search_results(self):
        """
        Display found videos on Scrollable Frame via CTkButton
        """
        # clear the id_var
        self.id_var.set(value='')

        # clear the scrollable frame
        for widget in self.scroll_frame.winfo_children():
            widget.destroy()

        self.download_button.configure(state='disabled')
        # get video thumbnail, title and video id
        videos = yt_search(self.entry.get(), self.type_var.get())

        for v in videos:
            # trim string if it's too long
            title = v.title if len(v.title) < 45 else v.title[:42] + '...'

            image = load_image(v.thumbnail)  # load video thumbnail

            button = VideoButton(master=self.scroll_frame, text=title,
                                 yt_id=v.yt_id, image=image, anchor='w')
            button.bind('<Button-1>',
                        lambda event, b=button: self.button_selected(b))
            button.pack(padx=10, pady=10)

    def is_entry_empty(self, *args):
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

    def button_selected(self, widget):
        """
        highlights the user-selected button
        :param widget: selected widget
        :return: None
        """
        self.download_button.configure(state='normal')
        for w in self.scroll_frame.winfo_children():
            if widget == w:
                w.change_state(True)
                self.id_var.set(value=w.yt_id)
            else:
                w.change_state(False)

    def download_content(self):
        """
        download selected YouTube object to desired filepath
        """
        path = askdirectory()  # ask the user to specify the path
        yt_type = self.type_var.get()  # type (video, playlist, channel)
        if yt_type == 0:  # downloading video
            download_video(self.id_var.get(), path)
        elif yt_type == 1:  # downloading playlist
            download_playlist(self.id_var.get(), path)
        elif yt_type == 2:  # downloading channel
            pass


if __name__ == "__main__":
    app = App()
    app.mainloop()
