import tkinter as tk
import time

class TerminalApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.exit_key_count = 0
        self.last_key_time = 0
        self.setup_terminal_mode()

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
