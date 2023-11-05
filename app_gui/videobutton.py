from customtkinter import CTkButton, CTk


class VideoButton(CTkButton):
    """
    Button, inherited from CTkButton, provides a youtube data api search result
    """

    def __init__(self, master, yt_id=None, text="", width=450,
                 height=80, font=('Arial', 12), **kwargs):
        super().__init__(master, text=text,
                         width=width, height=height, font=font, **kwargs)

        self.pressed = False
        self.yt_id = yt_id
        self.title = text
        self.res = None
        self.Youtube = None

    def configure(self, **kwargs):
        super().configure(**kwargs)

    def change_state(self, is_pressed: bool):
        if is_pressed:
            self.pressed = True
            self.configure(fg_color=('#ebe134', '#028f8e'),
                           hover_color=('#8d871f', '#015555'))
        else:
            self.pressed = False
            self.configure(fg_color=('#3a7ebf', '#1f538d'),
                           hover_color=('#325882', '#14375e'))


if __name__ == '__main__':
    window = CTk()
    window.mainloop()
