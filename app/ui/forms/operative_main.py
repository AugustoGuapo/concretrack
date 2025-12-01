import tkinter as tk
import tkinter.messagebox as messagebox
from app.ui.controllers.operative_controller import OperativeController
from app.state.session_state import SessionState
from app.state.sample_state import SampleState
from app.ui.forms.base_view import BaseView
import time

# Estilos coherentes con AdminView
ESTILOS = {
    "bg_main": "#F8F9FA",
    "bg_header": "#E3F2FD",
    "fg_header_text": "#0D47A1",
    "btn_add_bg": "#4CAF50",
    "btn_add_hover": "#388E3C",
    "font_header": ("Segoe UI", 28, "bold"),
    "font_button": ("Segoe UI", 36, "bold"),
    "font_list": ("Segoe UI", 30),
    "list_bg": "white",          # ✅ Añadido
    "list_fg": "#333333",        # ✅ Añadido
}

class SampleListFrame(BaseView):
    def __init__(self, parent, view_controller, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.operative_controller = OperativeController()
        self.view_controller = view_controller
        self.green_color = "#00FF00"
        self.pending_color = "black"

        self.config(bg=ESTILOS["bg_main"])
        self.create_header()
        self.create_sample_list()

    def create_header(self):
        self.header_frame = tk.Frame(self, bg=ESTILOS["bg_header"], height=80)
        self.header_frame.pack(fill=tk.X, padx=20, pady=15)
        self.header_frame.pack_propagate(False)

        try:
            username = SessionState.get_user().getFullName()
        except Exception:
            username = "Invitado"

        user_label = tk.Label(
            self.header_frame,
            text=username,
            bg=ESTILOS["bg_header"],
            fg=ESTILOS["fg_header_text"],
            font=ESTILOS["font_header"]
        )
        user_label.pack(side=tk.LEFT, padx=20)

        close_button = tk.Button(
            self.header_frame,
            text="Cerrar Sesión  ➤",
            bg="#FF5252",
            fg="black",
            font=("Segoe UI", 28, "bold"),
            bd=0,
            activebackground="#FF1744",
            activeforeground="black",
            width=18,
            height=2,
            relief="flat",
            command=self.logout
        )
        close_button.pack(side=tk.RIGHT, padx=20)

    def create_sample_list(self):
        list_container = tk.Frame(self, bg="lightgray", padx=2, pady=2)
        list_container.pack(fill=tk.BOTH, expand=True, padx=40, pady=(10, 30))

        list_frame = tk.Frame(list_container, bg=ESTILOS["list_bg"])
        list_frame.pack(fill=tk.BOTH, expand=True)

        canvas = tk.Canvas(list_frame, bg=ESTILOS["list_bg"], highlightthickness=0)
        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=20, pady=(0, 20))

                # Scrollbar más ancho y visible para pantalla táctil
        scrollbar = tk.Scrollbar(
            list_frame,
            orient=tk.VERTICAL,
            command=canvas.yview,
            width=50,  # 👈 Ancho aumentado
            bg="#E0E0E0",  # Fondo claro
            activebackground="#CCCCCC",  # Al hacer hover
            troughcolor="#F5F5F5"  # Color del fondo del track
        )
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        canvas.config(yscrollcommand=scrollbar.set)

        self.canvas_frame = tk.Frame(canvas, bg=ESTILOS["list_bg"])
        canvas.create_window((0, 0), window=self.canvas_frame, anchor="nw")
        # ✅ Corregido: paréntesis faltante
        self.canvas_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))

        self.row_widgets = []
        self.samples = self.operative_controller.get_samples()
        self.actualizar_lista()

    def actualizar_lista(self):
        for widget in self.canvas_frame.winfo_children():
            widget.destroy()
        self.row_widgets.clear()

        for i, member in enumerate(self.samples):
            row_frame = tk.Frame(self.canvas_frame, bg=ESTILOS["list_bg"], height=80)
            row_frame.pack(fill=tk.X, padx=10, pady=5)
            row_frame.pack_propagate(False)

            color = self.green_color if member.result is not None else self.pending_color
            lbl_item = tk.Label(
                row_frame,
                text=f"● {member.id}",
                font=ESTILOS["font_list"],
                bg=ESTILOS["list_bg"],
                fg=color,
                anchor="w"
            )
            lbl_item.grid(row=0, column=0, sticky="w", padx=20)

            row_data = {"frame": row_frame, "label": lbl_item, "index": i, "member": member}
            self.row_widgets.append(row_data)

            def make_handler(idx):
                return lambda e: self.select_row(idx)
            row_frame.bind("<Button-1>", make_handler(i))
            lbl_item.bind("<Button-1>", make_handler(i))

    def select_row(self, index):
        selected = self.row_widgets[index]
        member = selected["member"]

        if member.result is not None:
            messagebox.showinfo("Información", f"La muestra {member.id} ya tiene resultado registrado.")
            return

        SampleState.set_sample(member)
        self.view_controller.show_frame("ResultsForm")

    def on_show(self):
        for w in self.header_frame.winfo_children():
            if isinstance(w, tk.Label):
                try:
                    w.config(text=SessionState.get_user().getFullName())
                except:
                    w.config(text="Invitado")
        self.samples = self.operative_controller.get_samples()
        self.actualizar_lista()

    def mostrar_indicador_carga(self, mensaje="Cargando..."):
        self.loading_frame = tk.Frame(self, bg=ESTILOS["bg_main"])
        self.loading_frame.place(relx=0.5, rely=0.5, anchor="center")
        tk.Label(
            self.loading_frame,
            text=mensaje,
            font=("Segoe UI", 24),
            bg=ESTILOS["bg_main"],
            fg="#0D47A1"
        ).pack(pady=20)
        self.update_idletasks()

    def ocultar_indicador_carga(self):
        if hasattr(self, 'loading_frame') and self.loading_frame.winfo_exists():
            self.loading_frame.destroy()

    def logout(self):
        self.mostrar_indicador_carga("Verificando huella...")
        self.after(200, self._logout_with_biometric)

    def _logout_with_biometric(self):
        self.ocultar_indicador_carga()
        ventana = tk.Toplevel(self)
        ventana.title("Cerrar sesión - Verificación biométrica")
        ventana.transient(self.winfo_toplevel())  # ✅ Correcto y reconocido por Pylance
        ventana.grab_set()
        ventana.geometry("600x220")

        texto_instruccion = tk.StringVar(ventana, value="Por favor, coloque su dedo en el lector biométrico")
        label_instr = tk.Label(ventana, textvariable=texto_instruccion, font=("Segoe UI", 16))
        label_instr.pack(pady=20, padx=20)

        cancelled = {"v": False}
        def cancelar():
            cancelled["v"] = True
            ventana.destroy()

        btn_cancel = tk.Button(ventana, text="Cancelar", font=("Segoe UI", 14), command=cancelar)
        btn_cancel.pack(pady=8)

        ventana.update()
        attempts = 0
        max_attempts = 5

        while attempts < max_attempts and not cancelled["v"]:
            try:
                texto_instruccion.set("Esperando huella...")
                ventana.update()
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
                texto_instruccion.set("Huella no coincide. Intente nuevamente.")
                ventana.update()
                attempts += 1
                time.sleep(1.2)

        if not cancelled["v"]:
            try:
                ventana.destroy()
            except Exception:
                pass
            messagebox.showerror('Error', 'La huella no coincide con el usuario logeado.')