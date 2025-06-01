import tkinter as tk
from tkinter import ttk
from app.ui.utils.terminal import TerminalApp

class SampleListFrame(TerminalApp):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.title("Sample List Frame")
        self.geometry("1024x600")
        self.resizable(False, False)
        self.configure(bg="#005970")  # Fondo oscuro azul-gris

        # Crear el encabezado
        self.create_header()

        # Crear la lista de muestras
        self.create_sample_list()

        # Crear el botón "iniciar"
        self.create_start_button()

    def create_header(self):
        """Crea el encabezado con el nombre de usuario y el botón 'Cerrar'."""
        header_frame = tk.Frame(self, bg="#BDE5F8", bd=1, relief=tk.RAISED)
        header_frame.pack(fill=tk.X, padx=5, pady=5)

        # Etiqueta del usuario
        user_label = tk.Label(
            header_frame,
            text="Usuario: Maryi 0001",
            bg="#BDE5F8",
            fg="#005970",
            font=("Arial", 12, "bold"),
        )
        user_label.pack(side=tk.LEFT, padx=10, pady=5)

        # Botón 'Cerrar'
        close_button = tk.Button(
            header_frame,
            text="Cerrar Sesión  ➤",
            bg="#FF0000",
            fg="white",
            font=("Arial", 12, "bold"),
            bd=0,
            activebackground="#CC0000",
            activeforeground="white",
            command=self.destroy,
        )
        close_button.pack(side=tk.RIGHT, padx=10, pady=5)

    def create_sample_list(self):
        """Crea la lista de muestras con interacción según el estado (verde/amarillo)."""
        list_frame = tk.Frame(self, bg="#E0E0E0", bd=1, relief=tk.SUNKEN)
        list_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        # Barra de desplazamiento vertical
        scrollbar = tk.Scrollbar(list_frame, orient=tk.VERTICAL)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Lista de muestras
        self.sample_list = tk.Listbox(
            list_frame,
            bg="#E0E0E0",
            fg="#005970",
            font=("Arial", 12),
            selectbackground="#BDE5F8",
            selectmode=tk.SINGLE,
            yscrollcommand=scrollbar.set,
            activestyle="none"
        )
        self.sample_list.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Configurar la barra de desplazamiento
        scrollbar.config(command=self.sample_list.yview)

        # Datos de muestra: nombre y color
        samples = [
            ("Muestra0102", "#00FF00"),  # Verde - inactivo
            ("Muestra0103", "#FFD700"),  # Amarillo - activo
            ("Muestra0104", "#FFD700"),
            ("Muestra0105", "#FFD700"),
        ]

        # Guardamos los datos para poder accederlos por índice
        self.samples_data = []

        for name, color in samples:
            index = self.sample_list.size()
            self.sample_list.insert(tk.END, f"\u25CF {name}")
            self.sample_list.itemconfig(index, foreground=color)
            self.samples_data.append({"name": name, "color": color})

        # Asociar evento de selección
        self.sample_list.bind("<<ListboxSelect>>", self.on_sample_select)


    def on_sample_select(self, event):
        """Maneja la selección de una muestra."""
        selected_index = self.sample_list.curselection()

        if not selected_index:
            return  # No hay selección

        sample_info = self.samples_data[selected_index[0]]

        if sample_info["color"] == "#00FF00":
            # Estado verde: no hacer nada
            print(f"{sample_info['name']} está en estado verde. No se permite acción.")
            return

        elif sample_info["color"] == "#FFD700":
            # Estado amarillo: hacer algo
            print(f"Ejecutando acción para: {sample_info['name']}")
            self.on_yellow_sample_click(sample_info["name"])


    def on_yellow_sample_click(self, sample_name):
        """
        Acción a realizar cuando se selecciona una muestra en estado amarillo.
        Aquí puedes poner lo que necesites: abrir ventana, cargar datos, etc.
        """
        print(f"[ACCION] Muestra '{sample_name}' pulsada. Aquí puedes disparar otra función.")

    def create_start_button(self):
        """Crea el botón 'iniciar'."""
        button_frame = tk.Frame(self, bg="#FFFFFF", bd=1, relief=tk.FLAT)
        button_frame.pack(fill=tk.X, padx=5, pady=5)

        start_button = tk.Button(
            button_frame,
            text="iniciar",
            bg="#00BFFF",
            fg="white",
            font=("Arial", 12, "bold"),
            bd=0,
            activebackground="#0099CC",
            activeforeground="white",
            width=10,
        )
        start_button.pack(side=tk.RIGHT, padx=10, pady=5)

if __name__ == "__main__":
    app = SampleListFrame()
    app.mainloop()