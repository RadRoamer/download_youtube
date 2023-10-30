import customtkinter as ctk
from api.download import video_res
from app_gui.videobutton import VideoButton


class Frame(ctk.CTkFrame):
    def __init__(self, master, column, row,
                 columnspan=1, rowspan=1, weight=1, **kwargs):
        super().__init__(master, **kwargs)

        self.grid_columnconfigure(0, weight=weight)
        self.grid(column=column, row=row, rowspan=rowspan,
                  columnspan=columnspan, padx=10, pady=(0, 20))


class InfoFrame(Frame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.grid_rowconfigure(0, weight=1)  # configure grid system
        self.grid_columnconfigure(0, weight=1)

        self.textbox = ctk.CTkTextbox(master=self, width=500, height=125)
        self.textbox.grid(row=0, column=0)
        self.textbox.configure(state='disabled')

        self.progressbar = ctk.CTkProgressBar(self, orientation="horizontal")
        self.progressbar.grid(row=1, pady=(10, 10))

    def logging(self, *args):
        text = args[0]
        self.textbox.insert('1.0', text)
        print(*args)

    def clear_textbox(self):
        self.textbox.delete('1.0', 'end')


class ControlFrame(Frame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.grid_rowconfigure(0, weight=1)  # configure grid system
        self.grid_columnconfigure(0, weight=1)

        self.selected: VideoButton = None

        # variables
        self.quality_var = ctk.IntVar(value=0)
        self.id_var = ctk.StringVar(value='')
        self.combobox_var = ctk.StringVar(value="")

        self.res_button = ctk.CTkButton(self, state='disabled',
                                        command=self.get_resolutions,
                                        text='available resolutions')
        self.res_button.grid(row=0, column=0, padx=(0, 30), pady=10)

        self.download_button = ctk.CTkButton(self,
                                             text='download',
                                             state='disabled')
        self.download_button.grid(row=1, column=0, pady=10, padx=(0, 30))

        self.combobox = ctk.CTkComboBox(self, variable=self.combobox_var,
                                        state='disabled')
        self.combobox.grid(row=0, column=1, rowspan=2)

    def get_resolutions(self):
        button = self.selected

        button.res = video_res(button.yt_id, button)

        self.combobox.configure(values=button.res, state='normal')
        self.combobox_var.set(button.res[0])

        self.download_button.configure(state='normal')

    def combo_on(self, button: VideoButton):
        self.combobox.configure(values=button.res)
        self.combobox_var.set(value=button.res[0])

        self.download_button.configure(state='normal')

    def combo_off(self, button: VideoButton):
        self.combobox_var.set(value='')
        self.combobox.configure(values=[], state='disabled')

        self.download_button.configure(state='disabled')


if __name__ == '__main__':
    pass
