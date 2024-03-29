import customtkinter as ctk
import tkinter
from customtkinter import (
    CTkScrollableFrame,
    CTkEntry,
    CTkButton,
    CTkComboBox)
from api.search import yt_search, multithread_task
from app_gui import load_image
from app_gui.videobutton import VideoButton
from app_gui.frame import (
    Frame,
    InfoFrame,
    VideoFrame,
    PlaylistWindow, )

ctk.set_default_color_theme("dark-blue")
ctk.set_appearance_mode('dark')


class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title('youtube downloader')

        # if tkinter doesn`t find icon, use another path
        try:
            self.iconbitmap('../icon.ico')
        except tkinter.TclError:
            self.iconbitmap('icon.ico')

        self.geometry('900x600')
        self.grid_columnconfigure((0, 1), weight=1)

        # ------------------------> class variables
        self.type_var = ctk.IntVar(value=0)
        self.id_var = ctk.StringVar(value='')
        self.result_count = ctk.StringVar(value='')
        # ------------------------>

        self.search_frame = Frame(self, row=0, column=0, fg_color='transparent',
                                  columnspan=2, width=600)

        self.control_frame = Frame(self, row=1, column=0, fg_color='transparent',
                                   minsize=100)
        self.info_frame = InfoFrame(self, row=1, column=1)

        self.entry = CTkEntry(self.search_frame, placeholder_text='python',
                              width=500)
        self.entry.grid(row=0, column=0, padx=20, pady=(10, 0))

        # ------------------------> Control Buttons section
        self.buttons_frame = Frame(self.search_frame, row=1, column=0,
                                   fg_color='transparent')
        self.buttons_frame.grid_columnconfigure(0, weight=1)

        self.search_button = CTkButton(self.buttons_frame,
                                       text='search',
                                       state='disabled',
                                       command=self.search_setup)
        self.search_button.grid(row=1, column=0, pady=10, padx=(30, 70))

        # ------------------------>
        self.result_values = [str(x) for x in range(5, 30, 5)]
        self.textbox = CTkComboBox(self.buttons_frame,
                                   variable=self.result_count,
                                   values=self.result_values)
        self.textbox.grid(row=1, column=1, pady=10, padx=(30, 70))
        # ------------------------> Radio Buttons section
        self.radio_frame = Frame(self.search_frame, row=2, column=0,
                                 fg_color='transparent', height=100, width=500)

        self.radio_buttons = []
        for idx, text in enumerate(('video', 'playlist')):
            b = ctk.CTkRadioButton(self.radio_frame,
                                   text=text, variable=self.type_var,
                                   value=idx, width=250)
            b.grid(row=0, column=idx)
            b.columnconfigure(0, weight=1)
            self.radio_buttons.append(b)
        # ------------------------>

        self.scroll_frame = CTkScrollableFrame(self.search_frame, width=500, height=200)
        self.scroll_frame.grid(row=3, column=0)

        # binding
        self.entry.bind("<KeyRelease>", self.is_entry_empty)

    def search_setup(self):
        """
        Display found videos on Scrollable Frame via CTkButton
        """
        # clear the id_var
        self.id_var.set(value='')
        self.control_frame.destroy()

        yt_type = self.type_var.get()  # type (video, playlist, channel)

        attrs = {'master': self, 'row': 1, 'info_frame': self.info_frame,
                 'column': 0, 'width': 250, 'textbox': self.info_frame.textbox}

        if yt_type == 0:  # video
            self.control_frame = VideoFrame(**attrs)
        elif yt_type == 1:  # playlist
            self.control_frame = PlaylistWindow(**attrs, fg_color='transparent')

        # function  that is responsible for the frame's actions during search
        self.control_frame.setup()

        # clear the scrollable frame
        for widget in self.scroll_frame.winfo_children():
            widget.destroy()

        # display found results on ScrollFrame
        max_results = int(self.result_count.get())

        multithread_task(self.search, max_results=max_results)

    def search(self, max_results):
        self.search_button.configure(state='disabled')

        youtube_list = yt_search(self.type_var.get(), self.entry.get(), max_results)

        for v in youtube_list:
            # trim string if it's too long
            title = v.title if len(v.title) < 45 else v.title[:42] + '...'

            image = load_image(v.thumbnail)  # load video thumbnail

            button = VideoButton(master=self.scroll_frame, text=title,
                                 yt_id=v.yt_id, image=image, anchor='w')
            button.bind('<Button-1>',
                        lambda event, b=button: self.select_button(b))
            button.pack(padx=10, pady=10)

        self.search_button.configure(state='normal')

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

    def select_button(self, widget: VideoButton):
        """
        highlights the user-selected button
        :param widget: selected button
        """
        if not widget.pressed:  # check if button has not been pressed

            for w in self.scroll_frame.winfo_children():
                if isinstance(w, VideoButton):  # if widget is VideoButton
                    if widget == w:
                        self.control_frame.selected(widget=widget)
                        w.change_state(True)
                        self.id_var.set(value=w.yt_id)
                    else:
                        w.change_state(False)


if __name__ == "__main__":
    app = App()
    app.mainloop()
