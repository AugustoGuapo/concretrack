import tkinter as tk
from tkinter import ttk
from app.ui.forms.login import App
from app.ui.forms.operative_main import SampleListFrame
import time

class TerminalApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.exit_key_count = 0
        self.last_key_time = 0
        self.setup_terminal_mode()

        # Contenedor principal donde se cargarán las pantallas
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        # Diccionario para guardar las pantallas
        self.frames = {}

        # Añadimos todas las pantallas al diccionario
        for F in (App, SampleListFrame):
            frame = F(container)
            self.frames[F.__name__] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        # Mostrar la primera pantalla (Login)
        self.show_frame("SampleListFrame")
        self.mainloop()

    def show_frame(self, name):
        """Muestra una pantalla por su nombre"""
        frame = self.frames[name]
        frame.tkraise()

    def setup_terminal_mode(self):
        """Configuración común para todas las pantallas."""
        self.attributes("-fullscreen", True)
        self.bind("<Escape>", lambda e: None)
        self.bind("<Alt-F4>", lambda e: None)
        self.protocol("WM_DELETE_WINDOW", self._disable_close)

        # Vincula la tecla "x"
        self.bind("<Key>", self._on_key_press)

    def _disable_close(self):
        # Desactiva cierre por interfaz
        pass

    def _on_key_press(self, event):
        if event.keysym.lower() == 'x':
            current_time = time.time()
            # Si pasó más de 2 segundos desde la última X, reinicia
            if current_time - self.last_key_time > 2:
                self.exit_key_count = 0
            self.last_key_time = current_time

            self.exit_key_count += 1
            print(f"Tecla X presionada ({self.exit_key_count}/3)")

            if self.exit_key_count >= 3:
                self.destroy()
