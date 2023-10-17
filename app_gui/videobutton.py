from customtkinter import CTkButton


class VideoButton(CTkButton):
    """
    Button, inherited from CTkButton, provides a pytube search result
    """
    def __init__(self, master, channel_id=None, text="", width=450,
                 height=80, font=('Arial', 12), **kwargs):
        super().__init__(master, text=text, command=self.show_id,
                         width=width, height=height, font=font, **kwargs)

        self.pressed = False
        self.channel_id = channel_id

    def configure(self, **kwargs):
        super().configure(**kwargs)

    def change_state(self):
        self.pressed = not self.pressed
        if self.pressed:
            self.configure(fg_color=('#ebe134', '#857e0b'))
        else:
            self.configure(fg_color=('#3a7ebf', '#1f538d'))

    def show_id(self):
        print(self.channel_id)


