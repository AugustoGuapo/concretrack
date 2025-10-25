import tkinter as tk
from app.ui.controllers.operative_controller import OperativeController
from app.state.session_state import SessionState
from app.state.sample_state import SampleState
from app.ui.forms.base_view import BaseView
from tkinter import messagebox
import time

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
        self.header_frame.pack(fill=tk.X, padx=5, pady=5)

        try:
            username = SessionState.get_user().getFullName()
        except ValueError:
            username = "Invitado"

        # Etiqueta del usuario
        user_label = tk.Label(
            self.header_frame,
            text=username,
            bg="#BDE5F8",
            fg="#005970",
            font=("Arial", 20, "bold"),
        )
        user_label.pack(side=tk.LEFT, padx=10, pady=5)

        # Botón 'Cerrar'
        close_button = tk.Button(
            self.header_frame,
            text="Cerrar Sesión  ➤",
            bg="#FF0000",
            fg="white",
            font=("Arial", 20, "bold"),
            bd=0,
            activebackground="#CC0000",
            activeforeground="white",
            command=self.logout,
        )
        close_button.pack(side=tk.RIGHT, padx=10, pady=5)

    def create_sample_list(self):
        """Crea la lista de muestras con interacción según el estado (verde/amarillo)."""
        self.list_frame = tk.Frame(self, bg="#E0E0E0", bd=1, relief=tk.SUNKEN)
        self.list_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        # Barra de desplazamiento vertical
        scrollbar = tk.Scrollbar(self.list_frame, orient=tk.VERTICAL)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Lista de muestras
        self.sample_list = tk.Listbox(
            self.list_frame,
            bg="#E0E0E0",
            fg="#005970",
            font=("Arial", 36),
            selectbackground="#BDE5F8",
            selectmode=tk.SINGLE,
            yscrollcommand=scrollbar.set,
            activestyle="none"
        )
        self.sample_list.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Configurar la barra de desplazamiento
        scrollbar.config(command=self.sample_list.yview)

        # Datos de muestra: nombre y color
        self.samples = self.operative_controller.get_samples()

        # Guardamos los datos para poder accederlos por índice
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

        # Asociar evento de selección
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
    def logout(self):
        """Solicita verificación biométrica en una ventana modal antes de cerrar sesión.

        - Muestra estados claros: esperando, leyendo, huella no coincide, error.
        - Si el operario cancela, no se cierra la sesión.
        - Si alguien más pone su huella (no coincide), se permite reintentar hasta max_attempts.
        - Solo si sign_work() devuelve True se procede a cerrar sesión.
        """
        ventana = tk.Toplevel(self)
        ventana.title("Cerrar sesión - Verificación biométrica")
        ventana.transient(self)
        ventana.grab_set()
        ventana.geometry("600x220")

        texto_instruccion = tk.StringVar(ventana, value="Por favor, coloque su dedo en el lector biométrico")
        label_instr = tk.Label(ventana, textvariable=texto_instruccion, font=("Arial", 16))
        label_instr.pack(pady=20, padx=20)

        cancelled = {"v": False}
        def cancelar():
            cancelled["v"] = True
            ventana.destroy()

        btn_cancel = tk.Button(ventana, text="Cancelar", font=("Arial", 14), command=cancelar)
        btn_cancel.pack(pady=8)

        ventana.update()

        attempts = 0
        max_attempts = 5

        while attempts < max_attempts and not cancelled["v"]:
            try:
                texto_instruccion.set("Esperando huella...")
                ventana.update()
                # Llamada que intenta verificar la huella del operario actual
                isSigned = self.operative_controller.sign_work()
            except Exception:
                texto_instruccion.set("Error de lectura. Intente nuevamente.")
                ventana.update()
                time.sleep(1.2)
                attempts += 1
                continue

            if isSigned:
                texto_instruccion.set("Huella verificada. Cerrando sesión...")
                ventana.update()
                time.sleep(0.8)
                ventana.destroy()

                # Proceder con el cierre de sesión (igual que antes)
                SessionState.clear_user()
                if hasattr(self.view_controller, "show_frame"):
                    from app.ui.forms.login import App as Login
                    if "Login" not in self.view_controller.frame_classes:
                        self.view_controller.frame_classes["Login"] = Login
                    self.view_controller.show_frame("Login")
                    login_frame = self.view_controller.frames.get("Login")
                    if login_frame and hasattr(login_frame, "clear_fields"):
                        login_frame.clear_fields()
                return
            else:
                # Huella leída pero no coincide (puede ser otra persona)
                texto_instruccion.set("Huella no coincide con el usuario. Coloque su huella nuevamente o cancele.")
                ventana.update()
                attempts += 1
                time.sleep(1.2)
                # seguir reintentando hasta límite o cancelación

        # Si salimos por cancelación, simplemente no cerramos sesión
        if cancelled["v"]:
            return

        # Si agotamos intentos sin verificar la huella
        try:
            ventana.destroy()
        except Exception:
            pass

        messagebox.showerror('Error', 'La huella no coincide con el usuario logeado, intente nuevamente')
