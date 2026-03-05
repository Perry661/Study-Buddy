import tkinter as tk


class MoreMenuMixin:
    def open_more_menu(self) -> None:
        menu = tk.Menu(self, tearoff=0)
        menu.add_command(label="View finished tasks", command=self.open_finished_window)
        menu.add_separator()
        menu.add_command(label="More features coming soon", state="disabled")
        x = self.winfo_pointerx()
        y = self.winfo_pointery()
        try:
            menu.tk_popup(x, y)
        finally:
            menu.grab_release()
