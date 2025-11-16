# app/ui/forms/results_form.py

import tkinter as tk
import tkinter.messagebox as messagebox
from app.ui.controllers.results_controller import ResultsController
from app.state.session_state import SessionState
from app.state.sample_state import SampleState
from app.ui.forms.base_view import BaseView

# Reutilizar estilos de AdminView (si no están definidos aquí, puedes copiarlos)
# Si no quieres depender de ESTILOS, define un diccionario local:
ESTILOS = {
    "bg_main": "#F8F9FA",
    "bg_header": "#E3F2FD",
    "fg_header_text": "#0D47A1",
    "btn_add_bg": "#4CAF50",
    "btn_add_hover": "#388E3C",
    "font_title": ("Segoe UI", 32, "bold"),
    "font_header": ("Segoe UI", 28, "bold"),
    "font_button": ("Segoe UI", 36, "bold"),
    "font_list": ("Segoe UI", 30),
    "font_form": ("Segoe UI", 28),
}

class ResultsForm(BaseView):
    def __init__(self, parent, view_controller):
        super().__init__(parent)
        self.resultController = ResultsController()
        sample = SampleState.get_sample()
        self.member_id = sample.id
        self.family = sample.family_id
        self.days = 155
        self.view_controller = view_controller
        self.username = SessionState.get_user().getFullName() if SessionState.get_user() else "Invitado"
        self.body = None  # 👈 Inicializa aquí

        self.config(bg=ESTILOS["bg_main"])
        self._crear_header()
        self._crear_body()
        self._crear_footer()

    def _crear_header(self):
        header = tk.Frame(self, bg=ESTILOS["bg_header"], height=80)
        header.pack(fill="x", side="top")
        header.pack_propagate(False)

        # Botón de retroceso
        btn_back = tk.Button(
            header,
            text="←",
            font=("Segoe UI", 28, "bold"),
            bg=ESTILOS["bg_header"],
            fg="#0D47A1",
            bd=0,
            activebackground="#BBDEFB",
            activeforeground="#0D47A1",
            command=self._volver
        )
        btn_back.pack(side="left", padx=20)

        # Usuario
        lbl_user = tk.Label(
            header,
            text=f"Usuario: {self.username}",
            font=ESTILOS["font_header"],
            bg=ESTILOS["bg_header"],
            fg=ESTILOS["fg_header_text"]
        )
        lbl_user.pack(side="left", padx=20)

        # Separador
        separator = tk.Frame(self, height=2, bg="#DDDDDD")
        separator.pack(fill="x", pady=(0, 10))

    def _crear_body(self):
        self.body = tk.Frame(self, bg=ESTILOS["bg_main"])  # 👈 self.body
        self.body.pack(expand=True, fill="both", padx=40, pady=30)

        # Guardamos el label descriptivo para actualizarlo después
        self.lbl_family = tk.Label(
            self.body,
            text=f"Registrando resultados para familia: {self.family} a los {self.days} días",
            font=("Segoe UI", 24),
            bg=ESTILOS["bg_main"],
            fg="#333333"
        )
        self.lbl_family.pack(pady=(10, 30))

        frame_entry_boton = tk.Frame(self.body, bg=ESTILOS["bg_main"])
        frame_entry_boton.pack(fill="x", pady=(0, 20))

        self.entry_valor = tk.Entry(
            frame_entry_boton,
            font=("Segoe UI", 30),
            width=30,
            bg="white",
            fg="#333333",
            relief="flat",
            highlightthickness=2,
            highlightbackground="#CCCCCC",
            highlightcolor="#4CAF50",
            bd=2,
            insertwidth=4
        )
        self.entry_valor.pack(side="left", expand=True, fill="x", padx=(0, 20), ipady=15)

        btn_guardar = BotonRedondeado(
            parent=frame_entry_boton,
            width=250,
            height=80,
            radio=40,
            texto="GUARDAR",
            color_fondo=ESTILOS["btn_add_bg"],
            color_hover=ESTILOS["btn_add_hover"],
            color_texto="white",
            font=("Segoe UI", 28, "bold"),
            comando=self._guardar
        )
        btn_guardar.pack(side="right")

        vcmd = (self.register(self._validar_input), "%P")
        self.entry_valor.config(validate="key", validatecommand=vcmd)

    def _crear_footer(self):
        footer = tk.Frame(self, bg=ESTILOS["bg_main"], height=40)
        footer.pack(fill="x", side="bottom")

    def _validar_input(self, texto_nuevo):
        if texto_nuevo == "":
            return True
        try:
            float(texto_nuevo.replace(",", "."))
            return True
        except ValueError:
            return False

    def _guardar(self):
        valor_str = self.entry_valor.get().strip()
        if not valor_str:
            messagebox.showwarning("Campo vacío", "Ingresa un valor numérico.")
            self.entry_valor.config(bg="#f8d7da")  # Rojo claro
            return

        try:
            valor = float(valor_str.replace(",", "."))
            print(f"Valor guardado: {valor}")  # Reemplaza con tu lógica real
            self.resultController.save_results(
                user_id=SessionState.get_user().id,
                member_id=self.member_id,
                results=valor
            )
            self.entry_valor.config(bg="#d4edda")  # Verde claro
            messagebox.showinfo("Éxito", "Resultado guardado correctamente")
            self._volver()
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo guardar el resultado:\n{e}")
            self.entry_valor.config(bg="#f8d7da")

    def _volver(self):
        SampleState.clear_sample()
        self.view_controller.show_frame("SampleListFrame")

    def on_show(self):
        self._clear()
        self._reload()

    def _clear(self):
        self.entry_valor.delete(0, tk.END)
        self.entry_valor.config(bg="white")

    def _reload(self):
        sample = SampleState.get_sample()
        self.family = sample.family_id
        self.member_id = sample.id
        # ✅ Actualiza solo el texto, no destruye el frame
        if hasattr(self, 'lbl_family') and self.lbl_family:
            self.lbl_family.config(text=f"Registrando resultados para familia: {self.family} a los {self.days} días")

# ==============================================================================
# Botón redondeado personalizado (reutilizable)
class BotonRedondeado(tk.Canvas):
    def __init__(self, parent, width=200, height=60, radio=25,
                 texto="Botón", color_fondo="#3A86FF", color_hover="#2E75D9",
                 color_texto="white", font=("Segoe UI", 24, "bold"), comando=None):
        super().__init__(parent, width=width, height=height, bg=parent.cget("bg"),
                         highlightthickness=0, bd=0)
        self.radio = radio
        self.color_fondo = color_fondo
        self.color_hover = color_hover
        self.comando = comando

        self.rect = self.crear_rectangulo_redondeado(0, 0, width, height, radio, fill=color_fondo)
        self.texto = self.create_text(width // 2, height // 2, text=texto, fill=color_texto, font=font)

        self.bind("<Enter>", self.on_enter)
        self.bind("<Leave>", self.on_leave)
        self.bind("<Button-1>", self.on_click)

    def crear_rectangulo_redondeado(self, x1, y1, x2, y2, r=25, **kwargs):
        points = (
            x1 + r, y1,
            x2 - r, y1,
            x2, y1,
            x2, y1 + r,
            x2, y2 - r,
            x2, y2,
            x2 - r, y2,
            x1 + r, y2,
            x1, y2,
            x1, y2 - r,
            x1, y1 + r,
            x1, y1
        )
        return self.create_polygon(points, smooth=True, **kwargs)

    def on_enter(self, event):
        self.itemconfig(self.rect, fill=self.color_hover)

    def on_leave(self, event):
        self.itemconfig(self.rect, fill=self.color_fondo)

    def on_click(self, event):
        if self.comando:
            self.comando()