import tkinter as tk
from tkinter import font as tkfont
from app.ui.utils.terminal import TerminalApp

class ResultsForm(TerminalApp):
    def __init__(self, family="Familia", days=30):
        super().__init__()
        self.family = family
        self.days = days
        self.title("Registro de Resultados")
        self.configure(bg="#eff5fb")
        
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
            header, text="Usuario: Juan Pérez", font=self.font_header, 
            bg="#eff5fb", fg="#000000"
        )
        lbl_user.pack(side="left", padx=10)
        
        # Separador
        separator = tk.Frame(self, height=2, bg="#000000")
        separator.pack(fill="x", pady=(0, 10))

    def _crear_body(self):
        body = tk.Frame(self, bg="#eff5fb")
        body.pack(expand=True, fill="both", padx=20, pady=10)
        
        # Texto descriptivo
        lbl_family = tk.Label(
            body, 
            text=f"Registrando resultados para familia: {self.family} a los {self.days} días",
            font=self.font_body, bg="#eff5fb", fg="#000000"
        )
        lbl_family.pack(pady=(10, 10))
        
        # Frame contenedor para Entry + Botón (¡ESTE FRAME DEBE CONTENERLOS!)
        frame_entry_boton = tk.Frame(body, bg="#eff5fb")  # Fondo igual al body
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
        valor = self.entry_valor.get().replace(",", ".")
        if valor:
            print(f"Valor guardado: {valor}")  # Reemplaza con tu lógica
            # Feedback visual (opcional)
            self.entry_valor.config(bg="#d4edda")  # Fondo verde claro
        else:
            self.entry_valor.config(bg="#f8d7da")  # Fondo rojo claro (error)

    def _volver(self):
        """Acción para el botón de retroceso."""
        print("Volviendo a la pantalla anterior...")
        self.destroy()  # O navegar a otra pantalla

if __name__ == "__main__":
    app = ResultsForm()
    app.mainloop()