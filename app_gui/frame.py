import customtkinter as ctk
from api.download import video_res
from app_gui.videobutton import VideoButton
from tkinter.filedialog import askdirectory
from api.download import download_video


class Frame(ctk.CTkFrame):
    def __init__(self, master, column, row, pad=0, minsize=0,
                 columnspan=1, rowspan=1, weight=1, **kwargs):
        super().__init__(master, **kwargs)

        self.grid_columnconfigure(0, weight=weight, pad=pad, minsize=minsize)
        self.grid_rowconfigure(0, minsize=minsize)
        self.grid(column=column, row=row, rowspan=rowspan,
                  columnspan=columnspan, padx=10, pady=(0, 20))

    def selected(self, *args, **kwargs):
        raise AttributeError(f'its an abstract method for {type(self).__name__} ')

    def search(self, *args, **kwargs):
        raise AttributeError(f'its an abstract method for {type(self).__name__} ')

    def download(self, *args, **kwargs):
        raise AttributeError(f'its an abstract method for {type(self).__name__} ')


class InfoFrame(Frame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.grid(sticky='e')
        self.grid_rowconfigure(0, weight=1)  # configure grid system
        self.grid_columnconfigure(0, weight=1, minsize=300)

        self.textbox = ctk.CTkTextbox(master=self, width=500, height=125)
        self.textbox.grid(row=0, column=0)
        self.textbox.configure(state='disabled')

        self.progressbar = ctk.CTkProgressBar(self, orientation="horizontal")
        self.progressbar.grid(row=1, pady=(10, 10))

    def clear_textbox(self):
        self.textbox.delete('1.0', 'end')


class VideoControlFrame(Frame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.grid_rowconfigure(0, weight=1)  # configure grid system
        self.grid_columnconfigure(0, weight=1)

        self.dedicated_butt: VideoButton = None
        self.textbox: ctk.CTkTextbox = None

        # variables
        self.quality_var = ctk.IntVar(value=0)
        self.id_var = ctk.StringVar(value='')
        self.combobox_var = ctk.StringVar(value="")

        # ------------------------> Control Buttons section
        self.res_button = ctk.CTkButton(self, state='disabled',
                                        command=self.get_resolutions,
                                        text='available resolutions')
        self.res_button.grid(row=0, column=0, padx=(0, 30), pady=10)

        self.download_button = ctk.CTkButton(self, command=self.download,
                                             text='download', state='disabled')
        self.download_button.grid(row=1, column=0, pady=10, padx=(0, 30))
        # ------------------------>

        self.combobox = ctk.CTkComboBox(self, variable=self.combobox_var,
                                        state='disabled')
        self.combobox.grid(row=0, column=1, rowspan=2)

    def get_resolutions(self):
        button = self.dedicated_butt

        button.res = video_res(button.yt_id, button)

        self.combobox.configure(values=button.res, state='normal')
        self.combobox_var.set(button.res[0])

        self.download_button.configure(state='normal')

    def selected(self, *args, **kwargs):
        self.dedicated_butt = kwargs['widget']
        if self.dedicated_butt.res:
            self.combo_on()
        else:
            self.combo_off()
        self.res_button.configure(state='normal')
        self.combobox.configure(state='normal')

    def search(self, *args, **kwargs):
        self.res_button.configure(state='disabled')

    def combo_on(self):
        self.combobox.configure(values=self.dedicated_butt.res)
        self.combobox_var.set(value=self.dedicated_butt.res[0])

        self.download_button.configure(state='normal')

    def combo_off(self):
        self.combobox_var.set(value='')
        self.combobox.configure(values=[], state='disabled')

        self.download_button.configure(state='disabled')

    def download(self, *args, **kwargs):
        path = askdirectory()  # ask the user to specify the path

        self.textbox.configure(state='normal')
        download_video(path=path,
                       yt_obj=self.dedicated_butt.Youtube,
                       textbox=self.textbox,
                       quality=self.combobox_var.get())
        self.textbox.configure(state='disabled')


class PlaylistFrame(Frame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.grid_rowconfigure(0, weight=1)  # configure grid system
        self.grid_columnconfigure(0, weight=1)

        self.dedicated_butt: VideoButton = None
        self.textbox: ctk.CTkTextbox = None
        self.toplevel: ctk.CTkToplevel = None

        self.download_button = ctk.CTkButton(self, command=self.download,
                                             text='download', state='normal')
        self.download_button.grid(row=1, column=0, pady=10, padx=(0, 30))

    def download(self, *args, **kwargs):
        self.open_toplevel()

    def selected(self, *args, **kwargs):
        self.dedicated_butt = kwargs['widget']
        self.download_button.configure(state='normal')

    def search(self, *args, **kwargs):
        pass

    def open_toplevel(self):
        if self.toplevel is None or not self.toplevel.winfo_exists():
            self.toplevel = ctk.CTkToplevel()  # create window if its None or destroyed
        else:
            self.toplevel.focus()  # if window exists focus it


if __name__ == '__main__':
    app = ctk.CTk()
    frame = PlaylistFrame(app, row=0, column=0)
    app.mainloop()
