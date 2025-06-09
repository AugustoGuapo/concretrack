import tkinter as tk

class BaseView(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
    
    def on_show(self):
        """Method to be overridden by subclasses to define behavior when the view is shown."""
        pass