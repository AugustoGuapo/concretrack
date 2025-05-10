import tkinter as tk
from tkinter.font import BOLD
import utils.generic as util

class MasterPanel:
    def __init__(self):
        self.ventana = tk.Tk()
        self.ventana.title("Master Panel")

        # Full Screen
        self.ventana.attributes('-fullscreen', True)

        self.ventana.config(bg='gray')
        self.ventana.resizable(width=0, height=0)

        self.ventana.mainloop()
