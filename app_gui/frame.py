import customtkinter as ctk
from api.download import download_video, download_playlist
from api import YouTube
from tkinter.filedialog import askdirectory
from customtkinter import CTkScrollableFrame
from app_gui.videobutton import VideoButton
from api.search import get_playlist_videos, multithread_task
import api
from app_gui.image_from_url import load_image
from typing import List


class Frame(ctk.CTkFrame):
    def __init__(self, master, column, row, pad=0, minsize=0,
                 columnspan=1, rowspan=1, weight=1, **kwargs):
        super().__init__(master, **kwargs)

        self.grid_columnconfigure(0, weight=weight, pad=pad, minsize=minsize)
        self.grid_rowconfigure(0, minsize=minsize)
        self.grid(column=column, row=row, rowspan=rowspan,
                  columnspan=columnspan, padx=10, pady=(0, 20))

    def selected(self, *args, **kwargs):
        """function, which called when videobutton is pressed.
        should be overwritten in inherited classes"""
        raise AttributeError(f'its an abstract method for {type(self).__name__} ')

    def setup(self, *args, **kwargs):
        """function which called when user send the search request.
        should be overwritten in inherited classes"""
        raise AttributeError(f'its an abstract method for {type(self).__name__} ')

    def download_setup(self, *args, **kwargs):
        """function which when user wants to download something form youtube.
        should be overwritten in inherited classes"""
        raise AttributeError(f'its an abstract method for {type(self).__name__} ')


class TextBox(ctk.CTkTextbox):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def insert(self, index, text, tags=None):
        super().insert(index, text, tags=None)
        self.see(ctk.END)


class InfoFrame(Frame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.grid(sticky='e')
        self.grid_rowconfigure(0, weight=1)  # configure grid system
        self.grid_columnconfigure(0, weight=1, minsize=300)

        self.progress_var = ctk.IntVar(value=0)

        self.textbox = TextBox(master=self, width=500, height=125)
        self.textbox.grid(row=0, column=0)
        self.textbox.configure(state='disabled')

        self.progressbar = ctk.CTkProgressBar(self,
                                              variable=self.progress_var,
                                              orientation="horizontal")
        self.progressbar.grid(row=1, pady=(10, 10))


class VideoFrame(Frame):
    def __init__(self, *args, **kwargs):
        self.info = kwargs.pop('info_frame', None)
        self.textbox: ctk.CTkTextbox = kwargs.pop('textbox', None)

        super().__init__(*args, **kwargs)
        self.grid_rowconfigure(0, weight=1)  # configure grid system
        self.grid_columnconfigure(0, weight=1)

        self.dedicated_butt: VideoButton = None
        self.yt_id = ''

        # variables
        self.quality_var = ctk.IntVar(value=0)
        self.id_var = ctk.StringVar(value='')
        self.combobox_var = ctk.StringVar(value="")

        # ------------------------> Control Buttons section
        self.res_button = ctk.CTkButton(self, state='disabled',
                                        command=self.get_resolutions,
                                        text='available resolutions')
        self.res_button.grid(row=0, column=0, padx=(0, 30), pady=10)

        self.download_button = ctk.CTkButton(self, command=self.download_setup,
                                             text='download', state='disabled')
        self.download_button.grid(row=1, column=0, pady=10, padx=(0, 30))
        # ------------------------>

        self.combobox = ctk.CTkComboBox(self, variable=self.combobox_var,
                                        state='disabled')
        self.combobox.grid(row=0, column=1, rowspan=2)

    def get_resolutions(self):
        multithread_task(self.search)

    def selected(self, *args, **kwargs):
        self.dedicated_butt = kwargs['widget']
        if self.dedicated_butt.res:
            self.combo_on()
        else:
            self.combo_off()
        self.res_button.configure(state='normal')
        self.combobox.configure(state='normal')

    def setup(self, *args, **kwargs):
        self.res_button.configure(state='disabled')

    def search(self):
        res_list = api.search.get_res(self.dedicated_butt.yt_id)
        self.combobox.configure(values=res_list, state='normal')
        self.combobox_var.set(res_list[0])

        self.download_button.configure(state='normal')

    def combo_on(self):
        self.combobox.configure(values=self.dedicated_butt.res)
        self.combobox_var.set(value=self.dedicated_butt.res[0])

        self.download_button.configure(state='normal')

    def combo_off(self):
        self.combobox_var.set(value='')
        self.combobox.configure(values=[], state='disabled')

        self.download_button.configure(state='disabled')

    def download_setup(self, *args, **kwargs):
        path = askdirectory()  # ask the user to specify the path
        if not path:
            return None
        self.yt_id = self.dedicated_butt.yt_id
        self.info.progressbar.set(0)
        self.textbox.delete(1.0, ctk.END)

        self.textbox.configure(state='normal')
        multithread_task(download_video, path, self.yt_id, 99.9, self)


class ToplevelWindow(ctk.CTkToplevel):
    """top level window for additional functionality"""

    def __init__(self, *args, **kwargs):
        # function called by the checkbox every time a variable is changed
        check_func = kwargs.pop('check_func')
        super().__init__(*args, **kwargs)
        self.geometry("600x500")

        # configure toplevel grid
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=5)

        # create and configure checkbox that select/unselect all videos
        self.check_var = ctk.StringVar(value="off")
        self.checkbox = ctk.CTkCheckBox(self, text="select all",
                                        variable=self.check_var,
                                        onvalue="on",
                                        offvalue="off",
                                        command=check_func)
        self.checkbox.grid(row=0, column=0, sticky='w',
                           padx=(20, 20), columnspan=2)

        self.scroll_frame = ScrollFrame(self)
        self.scroll_frame.grid(row=1, padx=(20, 20), pady=(0, 10),
                               column=0, sticky='nsew', columnspan=2)


class PlaylistWindow(Frame):
    """A frame that provides functionality for selecting
     and downloading videos from the selected playlist"""

    def __init__(self, *args, **kwargs):
        self.info = kwargs.pop('info_frame', None)
        self.textbox = kwargs.pop('textbox', None)

        super().__init__(*args, **kwargs)

        self.grid(sticky='e')
        self.grid_rowconfigure(0, weight=1)  # configure grid system
        self.grid_columnconfigure(0, weight=1)

        self.combobox_var = ctk.StringVar(value="")
        # preset available resolutions
        self.res = ['720p', '480p', '360p', '240p', '144p']
        self.playlist = ''

        self.toplevel: ToplevelWindow = None
        self.download_button: ctk.CTkButton = None
        self.combobox: ctk.CTkComboBox = None
        self.videos = []
        self.yt_id = ''
        self.title = ''
        self.ids = []  # id`s of selected videos

        self.toplevel_button = ctk.CTkButton(self, command=self.open_toplevel,
                                             text='open playlist', state='normal')
        self.toplevel_button.grid(row=0, column=0, sticky='nsew',
                                  pady=10, padx=(0, 30))

    def toplevel_selected(self, widget: VideoButton):
        """
        function called every time a button in a scrollable frame is clicked.
        When clicked first time, its change button color and add button yt_id to the list,
        second time its change color back and remove corresponding yt_id from the list
        :param widget:  selected button
        """
        yt_id = widget.yt_id  # get the video id
        if widget.pressed:  # check if widget is pressed
            widget.change_state(False)
            self.ids.remove(yt_id)  # remove video id
        else:
            widget.change_state(True)
            self.ids.append(yt_id)  # add the video id to the list

        if self.ids:  # activate if at least one video is selected
            self.download_button.configure(state='normal')
        else:  # else uncheck and disable the download button
            self.toplevel.check_var.set(value='off')
            self.download_button.configure(state='disabled')

    def selected(self, *args, **kwargs):
        self.playlist = kwargs['widget'].yt_id
        self.title = kwargs['widget'].title

    def setup(self, *args, **kwargs):
        pass

    def open_toplevel(self, *args, **kwargs):
        """create and configure toplevel window for the playlist"""
        self.ids = []

        # check if toplevel already created
        if self.toplevel is None or not self.toplevel.winfo_exists():
            # create window if its None or destroyed
            self.toplevel = ToplevelWindow(self, check_func=self.checkbox_func)
            self.toplevel.grid_columnconfigure((0, 1), weight=1)

            # ------------------------> Toplevel control section
            self.download_button = ctk.CTkButton(self.toplevel,
                                                 command=self.download_setup,
                                                 text='download selected',
                                                 state='disabled')
            self.download_button.grid(row=2, column=0, pady=10, padx=(0, 30))

            self.combobox = ctk.CTkComboBox(self.toplevel, variable=self.combobox_var,
                                            values=self.res)
            self.combobox.grid(row=2, column=1)
            # ------------------------>
            # get all videos
            api.search.multithread_task(self.search_videos, pl_id=self.playlist)

        self.toplevel.focus()  # if window exists focus it
        self.setup()

    def search_videos(self, pl_id):
        self.videos = get_playlist_videos(pl_id)

        # display videos as VideoButton class in scrollable frame
        self.toplevel.scroll_frame.display_results(self.videos, self.toplevel_selected)
        self.combobox_var.set(value=self.res[0])

    def download_setup(self):
        self.info.progressbar.set(0)
        self.textbox.delete(1.0, ctk.END)
        path = askdirectory()  # ask the user to specify the path
        if not path:
            return None
        multithread_task(download_playlist, path, self)

    def checkbox_func(self):
        """a function for the checkbox to select, or vice versa
         for discarding all videos in the playlist"""
        # get all videos in scroll frame
        buttons = self.toplevel.scroll_frame.winfo_children()
        # check if checkbox is switches to 'off'
        if self.toplevel.check_var.get() == 'off':
            self.ids = []  # delete all ids
            self.download_button.configure(state='disabled')
            # unselect all buttons in scroll frame
            for button in buttons:
                button.change_state(False)
        else:  # else it switches to 'on'
            self.download_button.configure(state='normal')
            # select and highlight all buttons in scroll frame
            for button in buttons:
                self.ids.append(button.yt_id)
                button.change_state(True)


class ScrollFrame(CTkScrollableFrame):
    """Basic CTkScrollableFrame with soma addition convenient functionality"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def display_results(self, videos: List[YouTube], func):
        """
        get videos list and display all them on scroll frame
        :param videos: list of videos
        :param func: function which is attached to each button
        """
        for widget in self.winfo_children():
            widget.destroy()

        for v in videos:
            title = v.title if len(v.title) < 45 else v.title[:42] + '...'

            image = load_image(v.thumbnail)  # load video thumbnail

            button = VideoButton(master=self, text=title, yt_id=v.yt_id,
                                 image=image, anchor='w')
            button.bind('<Button-1>', lambda event, b=button: func(b))
            button.pack(padx=10, pady=10)


if __name__ == '__main__':
    app = ctk.CTk()
    frame = PlaylistWindow(app, row=0, column=0)
    app.mainloop()
