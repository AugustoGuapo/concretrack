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

    def _crear_header(self):
        # Frame del header
        header = tk.Frame(self, bg="#eff5fb", height=80)
        header.pack(fill="x", side="top")

        # Botón de retroceso
        btn_back = tk.Button(
            header,
            text="←",
            font=self.font_header,
            bg="#eff5fb",
            fg="#000000",
            borderwidth=0,
            command=self._volver
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
            font=self.font_body,
            bg="#eff5fb",
            fg="#000000"
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

        # --- Nueva sección: Radiobuttons con imágenes ---
        radio_frame = tk.Frame(body, bg="#eff5fb")
        radio_frame.pack(pady=(10, 0))

        self.selected_type = tk.IntVar(value=-1)  # -1 = sin selección
        self.radio_images = []

        for idx in range(6):  # Tipos del 1 al 6
            current_dir = os.path.dirname(os.path.abspath(__file__))
            image_path = os.path.join(current_dir, "..", "images", f"Tipo{idx+1}.png")

            try:
                pil_img = Image.open(image_path)
                pil_img = pil_img.resize((100, 150), Image.Resampling.LANCZOS)  # Redimensionar
                img = ImageTk.PhotoImage(pil_img)
                self.radio_images.append(img)
            except Exception as e:
                print(f"No se pudo cargar la imagen: {image_path} - Error: {e}")
                img = None

            option_frame = tk.Frame(radio_frame, bg="#eff5fb")
            option_frame.pack(side="left", padx=10)

            rb = tk.Radiobutton(
                option_frame,
                text=f"Tipo {idx+1}",
                image=img,
                compound="top",
                variable=self.selected_type,
                value=idx,
                bg="#eff5fb",
                fg="#000000",
                selectcolor="#cccccc",
                indicatoron=False,
                width=175,
                height=225,
                font=self.font_body,
                anchor="center",
                justify="center",
                padx=5,
                pady=5
            )
            rb.pack()

    def _validar_input(self, texto_nuevo):
        if texto_nuevo == "":
            return True
        try:
            float(texto_nuevo.replace(",", "."))
            return True
        except ValueError:
            return False

    def _guardar(self):
        valor = self.entry_valor.get()
        if not valor:
            self.entry_valor.config(bg="#f8d7da")
            return

        try:
            valor = float(valor.replace(",", "."))
        except ValueError:
            self.entry_valor.config(bg="#f8d7da")
            return

        self.entry_valor.config(bg="#d4edda")
        print(f"Valor guardado: {valor}")

        selected_type = self.selected_type.get()
        if selected_type != -1:
            tipo_seleccionado = selected_type + 1  
            # VALOR OBTENIDO DE TIPO DE FRACTURA
            print(tipo_seleccionado)
            self.view_controller.show_frame("SampleListFrame")
        else:
            print("No se ha seleccionado ningún tipo.")

        try:
            self.resultController.save_results(
                user_id=SessionState.get_user().id,
                member_id=self.member_id,
                results=valor,
                type_index=tipo_seleccionado
            )
        except Exception as e:
            print("Error al guardar:", e)
            messagebox.showerror("Error", "No se pudo guardar el resultado.")
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
