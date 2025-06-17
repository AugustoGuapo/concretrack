import tkinter as tk
from app.ui.forms.login import App
from app.ui.forms.operative_main import SampleListFrame
from app.ui.forms.admin_view import AdminView
from app.ui.forms.results_form import ResultsForm
import time

class TerminalApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.exit_key_count = 0
        self.last_key_time = 0
        self.setup_terminal_mode()

        # Contenedor principal donde se cargarán las pantallas
        self.container = tk.Frame(self)
        self.container.pack(side="top", fill="both", expand=True)
        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_columnconfigure(0, weight=1)

        self.frame_classes = {
            "App": App,
            "SampleListFrame": SampleListFrame,
            "AdminView": AdminView,
            "ResultsForm": ResultsForm,
        }
        self.frames = {}

        self.show_frame("App")
        self.after(100, lambda: self.attributes("-fullscreen", True))
        self.mainloop()

    def show_frame(self, name):
        """Muestra una pantalla por su nombre, creándola si es necesario."""
        if name not in self.frames:
            print(f"Creando frame: {name}")
            frame_class = self.frame_classes[name]
            frame = frame_class(self.container, self)
            print(f"Frame creado: {name}")
            self.frames[name] = frame
            frame.grid(row=0, column=0, sticky="nsew")
        print(self.frames)
        self.frames[name].on_show()
        self.frames[name].tkraise()


    def setup_terminal_mode(self):
        """Configuración común para todas las pantallas."""
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
