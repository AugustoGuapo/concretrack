import tkinter as tk
from tkinter import font as tkfont
from app.ui.controllers.results_controller import ResultsController 
from app.state.session_state import SessionState  
from app.state.sample_state import SampleState
from app.ui.forms.base_view import BaseView

class ResultsForm(BaseView):
    def __init__(self, parent, view_controller):
        super().__init__(parent)
        self.resultController = ResultsController()  # Aquí deberías inicializar tu controlador de resultados
        sample = SampleState.get_sample()
        self.member_id = sample.id
        self.family = sample.family_id
        self.days = 155  # Días de la muestra, puedes ajustar según tu lógica
        #self.title("Registro de Resultados")
        self.configure(bg="#eff5fb")
        self.view_controller = view_controller 
        self.username = SessionState.get_user().getFullName() if SessionState.get_user() else "Invitado"
        
        # Fuentes personalizadas (mejor legibilidad)
        self.font_header = tkfont.Font(family="Arial", size=16, weight="bold")
        self.font_body = tkfont.Font(family="Arial", size=14)
        self.font_button = tkfont.Font(family="Arial", size=12, weight="bold")
        
        self._crear_header()
        self._crear_body()
        self._crear_footer()

    def _crear_header(self):
        # Frame del header
        header = tk.Frame(self, bg="#eff5fb", height=80)
        header.pack(fill="x", side="top")
        
        # Botón de retroceso (con ícono Unicode o imagen)
        btn_back = tk.Button(
            header, text="←", font=self.font_header, bg="#eff5fb", fg="#000000", 
            borderwidth=0, command=self._volver
        )
        btn_back.pack(side="left", padx=10)
        
        # Usuario
        lbl_user = tk.Label(
            header, text=f"Usuario: {self.username}", font=self.font_header, 
            bg="#eff5fb", fg="#000000"
        )
        lbl_user.pack(side="left", padx=10)
        
        # Separador
        separator = tk.Frame(self, height=2, bg="#000000")
        separator.pack(fill="x", pady=(0, 10))

    def _crear_body(self):
        self.body = tk.Frame(self, bg="#eff5fb")
        self.body.pack(expand=True, fill="both", padx=20, pady=10)

        # Texto descriptivo
        lbl_family = tk.Label(
            self.body, 
            text=f"Registrando resultados para familia: {self.family} a los {self.days} días",
            font=self.font_body, bg="#eff5fb", fg="#000000"
        )
        lbl_family.pack(pady=(10, 10))
        
        # Frame contenedor para Entry + Botón (¡ESTE FRAME DEBE CONTENERLOS!)
        frame_entry_boton = tk.Frame(self.body, bg="#eff5fb")  # Fondo igual al body
        frame_entry_boton.pack(fill="x", pady=(0, 0))
        self.entry_valor = tk.Entry(
            frame_entry_boton,
            font=self.font_body, 
            borderwidth=2, 
            relief="solid",
            validate="key", 
            validatecommand=(self.register(self._validar_input), "%P")
        )
        self.entry_valor.pack(side="left", expand=True, fill="x", padx=(0, 10), ipady=10)
        
        btn_guardar = tk.Button(
            frame_entry_boton,
            text="GUARDAR", 
            font=self.font_button, 
            bg="#d9d9d9",
            fg="#000000",
            command=self._guardar, 
            width=10,
            height=2
        )
        btn_guardar.pack(side="right")
        
        # Asociar teclado táctil al Entry
        # Descomentar para probar el teclado táctil
        #self.entry_valor.bind("<FocusIn>", lambda e: self._abrir_teclado())

    def _crear_footer(self):
        footer = tk.Frame(self, bg="#eff5fb", height=40)
        footer.pack(fill="x", side="bottom")

    def _validar_input(self, texto_nuevo):
        """Valida que el input sea numérico (con coma opcional)."""
        if texto_nuevo == "":
            return True
        try:
            float(texto_nuevo.replace(",", "."))
            return True
        except ValueError:
            return False

    def _guardar(self):
        """Acción al presionar 'Guardar'."""
        valor = self.entry_valor.get()
        valor = float(valor)
        if valor:
            print(f"Valor guardado: {valor}")  # Reemplaza con tu lógica
            # Feedback visual (opcional)
            self.resultController.save_results(user_id = SessionState.get_user().id, member_id=self.member_id, results=valor)
            self.entry_valor.config(bg="#d4edda")  # Fondo verde claro
            self._volver()
        else:
            self.entry_valor.config(bg="#f8d7da")  # Fondo rojo claro (error)
        self._clear()

    def _volver(self):
        """Acción para el botón de retroceso."""
        SampleState.clear_sample()
        self.view_controller.show_frame("SampleListFrame")


    def on_show(self):
        """Acción al mostrar el formulario."""
        self._clear()
        self._reload()
    def _clear(self):
        """Limpia el formulario."""
        self.entry_valor.delete(0, tk.END)
        self.entry_valor.config(bg="#ffffff")

    def _reload(self):
        """Recarga el formulario si es necesario."""
        self.family = SampleState.get_sample().family_id
        self.member_id = SampleState.get_sample().id
        self.body.destroy()
        self._crear_body()
