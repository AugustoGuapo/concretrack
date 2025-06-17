import tkinter as tk
from app.ui.controllers.operative_controller import OperativeController
from app.state.session_state import SessionState
from app.state.sample_state import SampleState
from app.ui.forms.base_view import BaseView


class SampleListFrame(BaseView):
    green = "#00FF00"
    yellow = "#FFD700"

    def __init__(self, parent, view_controller, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.configure(bg="#005970")  # Fondo oscuro azul-gris
        self.operative_controller = OperativeController()
        self.green_color = "#00FF00"
        self.yellow_color = "#FFD700"
        self.view_controller = view_controller

        # Crear el encabezado
        self.create_header()

        # Crear la lista de muestras
        self.create_sample_list()
    def create_header(self):
        """Crea el encabezado con el nombre de usuario y el botón 'Cerrar'."""
        self.header_frame = tk.Frame(self, bg="#BDE5F8", bd=1, relief=tk.RAISED)
        self.header_frame.pack(fill=tk.X, padx=10, pady=10)  # Más padding

        try:
            username = SessionState.get_user().getFullName()
        except ValueError:
            username = "Invitado"

        # Etiqueta del usuario (fuente más grande)
        user_label = tk.Label(
            self.header_frame,
            text=username,
            bg="#BDE5F8",
            fg="#005970",
            font=("Arial", 40, "bold"),  # Aumentado
        )
        user_label.pack(side=tk.LEFT, padx=20, pady=10)

        # Botón 'Cerrar' (fuente y padding mayores)
        close_button = tk.Button(
            self.header_frame,
            text="Cerrar Sesión  ➤",
            bg="#FF0000",
            fg="white",
            font=("Arial", 40, "bold"),  # Aumentado
            bd=0,
            activebackground="#CC0000",
            activeforeground="white",
            command=self.destroy,
            height=2,  # Más alto
            width=15   # Más ancho
        )
        close_button.pack(side=tk.RIGHT, padx=20, pady=10)


    def create_sample_list(self):
        """Crea la lista de muestras con interacción según el estado (verde/amarillo)."""
        self.list_frame = tk.Frame(self, bg="#E0E0E0", bd=1, relief=tk.SUNKEN)
        self.list_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Barra de desplazamiento vertical
        scrollbar = tk.Scrollbar(self.list_frame, orient=tk.VERTICAL, width=100)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Lista de muestras
        self.sample_list = tk.Listbox(
            self.list_frame,
            bg="#E0E0E0",
            fg="#005970",
            font=("Arial", 80),  # Aumentado
            selectbackground="#BDE5F8",
            selectmode=tk.SINGLE,
            yscrollcommand=scrollbar.set,
            activestyle="none",
            height=10  # Opcional: puede controlar cuántos items visibles
        )
        self.sample_list.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        scrollbar.config(command=self.sample_list.yview)

        # Datos de muestra
        self.samples = self.operative_controller.get_samples()
        self.samples_data = []

        for member in self.samples:
            index = self.sample_list.size()
            self.sample_list.insert(tk.END, f"\u25CF {member.id}")
            if member.result or member.result == 0:
                color = self.green_color
            else:
                color = self.yellow_color
            self.sample_list.itemconfig(index, foreground=color)
            self.samples_data.append({"name": member.id, "color": color})

        self.sample_list.bind("<<ListboxSelect>>", self.on_sample_select)



    def on_sample_select(self, event):
        """Maneja la selección de una muestra."""
        selected_index = self.sample_list.curselection()

        if not selected_index:
            return  # No hay selección

        sample_info = self.samples_data[selected_index[0]]

        if sample_info["color"] == self.green_color:
            # Estado verde: no hacer nada
            print(f"{sample_info['name']} está en estado verde. No se permite acción.")
            return

        elif sample_info["color"] == self.yellow_color:
            # Estado amarillo: hacer algo
            print(f"Ejecutando acción para: {sample_info['name']}")
            self.on_yellow_sample_click(sample_info["name"])


    def on_yellow_sample_click(self, sample_name):
        """
        Acción a realizar cuando se selecciona una muestra en estado amarillo.
        Aquí puedes poner lo que necesites: abrir ventana, cargar datos, etc.
        """
        for sample in self.samples:
            if sample.id == sample_name:
                SampleState.set_sample(sample)
                break
        self.view_controller.show_frame("ResultsForm")

    def on_show(self):
        """Método llamado al mostrar el frame."""
        self.header_frame.destroy()
        self.create_header()
        self.list_frame.destroy()
        self.create_sample_list()
