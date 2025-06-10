import tkinter as tk
from tkinter import font as tkfont
from tkinter import messagebox
import os

# Importaciones propias del proyecto (ajusta según tu estructura)
from app.ui.utils.terminal import TerminalApp
from app.ui.controllers.results_controller import ResultsController
from app.state.session_state import SessionState
from app.models.user import User

# Importar Pillow para redimensionar imágenes
from PIL import Image, ImageTk


class ResultsForm(TerminalApp):
    def __init__(self, member_id, family="Familia", days=30):
        super().__init__()
        self.resultController = ResultsController()
        self.member_id = member_id
        self.family = family
        self.days = days
        self.title("Registro de Resultados")
        self.configure(bg="#eff5fb")

        # Fuentes personalizadas
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
            header,
            text="Usuario: Juan Pérez",
            font=self.font_header,
            bg="#eff5fb",
            fg="#000000"
        )
        lbl_user.pack(side="left", padx=10)

        # Separador
        separator = tk.Frame(self, height=2, bg="#000000")
        separator.pack(fill="x", pady=(0, 10))

    def _crear_body(self):
        body = tk.Frame(self, bg="#eff5fb")
        body.pack(expand=True, fill="both", padx=20, pady=10)

        # --- Sección superior: Etiqueta + Entry + Botón ---
        lbl_family = tk.Label(
            body,
            text=f"Registrando resultados para familia: {self.family} a los {self.days} días",
            font=self.font_body,
            bg="#eff5fb",
            fg="#000000"
        )
        lbl_family.pack(pady=(10, 10))

        frame_entry_boton = tk.Frame(body, bg="#eff5fb")
        frame_entry_boton.pack(fill="x", pady=(0, 20))

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

    def _volver(self):
        print("Volviendo a la pantalla anterior...")
        self.destroy()


if __name__ == "__main__":
    # Simulación de usuario
    from app.models.user import User
    SessionState.set_user(User(
        id=1,
        username="root",
        passwordHash="root",
        firstName="Juan Pérez",
        lastName="Petro",
        role="admin"
    ))

    app = ResultsForm(2)
    app.mainloop()