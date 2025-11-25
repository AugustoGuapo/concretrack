# app/ui/forms/results_form.py

import tkinter as tk
import tkinter.messagebox as messagebox
from app.ui.controllers.results_controller import ResultsController
from app.state.session_state import SessionState
from app.state.sample_state import SampleState
from app.ui.forms.base_view import BaseView
import os
from PIL import Image, ImageTk, ImageDraw, ImageFont
from PIL.Image import Resampling

# Estilos coherentes con AdminView
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
        self.days = sample.fracture_days
        self.view_controller = view_controller
        self.username = SessionState.get_user().getFullName() if SessionState.get_user() else "Invitado"
        self.body = None
        self.selected_type = None  # Guarda el tipo seleccionado

        self.config(bg=ESTILOS["bg_main"])
        self._crear_header()
        self._crear_body()
        self._crear_footer()

    def _crear_header(self):
        header = tk.Frame(self, bg=ESTILOS["bg_header"], height=80)
        header.pack(fill="x", side="top")
        header.pack_propagate(False)

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

        lbl_user = tk.Label(
            header,
            text=f"Usuario: {self.username}",
            font=ESTILOS["font_header"],
            bg=ESTILOS["bg_header"],
            fg=ESTILOS["fg_header_text"]
        )
        lbl_user.pack(side="left", padx=20)

        separator = tk.Frame(self, height=2, bg="#DDDDDD")
        separator.pack(fill="x", pady=(0, 10))

    def _crear_body(self):
        # Frame contenedor principal con scroll
        container = tk.Frame(self, bg=ESTILOS["bg_main"])
        container.pack(expand=True, fill="both", padx=40, pady=(0, 20))

        # Canvas con scroll
        canvas = tk.Canvas(container, bg=ESTILOS["bg_main"], highlightthickness=0)
        scrollbar = tk.Scrollbar(container, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg=ESTILOS["bg_main"])

        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # Texto descriptivo
        lbl_family = tk.Label(
            scrollable_frame,
            text=f"Registrando resultados para familia: {self.resultController.getFamilyNameById(self.family)} a los {self.days} días",
            font=("Segoe UI", 24),
            bg=ESTILOS["bg_main"],
            fg="#333333"
        )
        lbl_family.pack(pady=(30, 30))

        # Frame principal (teclado + tipos)
        main_frame = tk.Frame(scrollable_frame, bg=ESTILOS["bg_main"])
        main_frame.pack(fill="x", pady=(0, 20))

        main_frame.grid_columnconfigure(0, weight=1)
        main_frame.grid_columnconfigure(1, weight=1)

        # Teclado numérico (izquierda)
        keypad_frame = tk.Frame(main_frame, bg=ESTILOS["bg_main"])
        keypad_frame.grid(row=0, column=0, sticky="nsew", padx=(0, 20))

        entry_valor = tk.Entry(
            keypad_frame,
            font=("Segoe UI", 30),
            width=20,
            bg="#000000",
            fg="#FFFFFF",
            relief="flat",
            highlightthickness=2,
            highlightbackground="#444444",
            highlightcolor="#4CAF50",
            bd=2,
            insertbackground="#FFFFFF",
            state="readonly"
        )
        entry_valor.grid(row=0, column=0, columnspan=3, padx=5, pady=(0, 10), ipady=15, sticky="ew")

        for col in range(3):
            keypad_frame.grid_columnconfigure(col, weight=1)

        buttons = [
            ['7', '8', '9'],
            ['4', '5', '6'],
            ['1', '2', '3'],
            ['.', '0', '←']
        ]

        for i, row in enumerate(buttons):
            for j, text in enumerate(row):
                btn = tk.Button(
                    keypad_frame,
                    text=text,
                    font=("Segoe UI", 32, "bold"),
                    bg="#333333",
                    fg="#FFFFFF",
                    width=4,
                    height=2,
                    relief="raised",
                    bd=2,
                    command=lambda t=text: self._add_to_entry(t)
                )
                btn.grid(row=i+1, column=j, padx=5, pady=5, sticky="nsew")

        # Tipos de fractura (derecha) - en cuadrícula 2x3
        types_frame = tk.Frame(main_frame, bg=ESTILOS["bg_main"])
        types_frame.grid(row=0, column=1, sticky="nsew", padx=(20, 0))

        # Título con grid
        tk.Label(
            types_frame,
            text="Tipo de Fractura:",
            font=("Segoe UI", 24, "bold"),
            bg=ESTILOS["bg_main"],
            fg="#333333"
        ).grid(row=0, column=0, columnspan=2, pady=(0, 10))

        # Cargar imágenes
        self.type_images = []
        BASE_DIR = os.path.dirname(os.path.abspath(__file__))
        IMG_DIR = os.path.join(BASE_DIR, "..", "images")

        for i in range(1, 7):
            try:
                img_path = os.path.join(IMG_DIR, f"Tipo{i}.png")
                img = Image.open(img_path)
                if hasattr(Image, 'Resampling'):
                    img = img.resize((100, 100), Resampling.BICUBIC)
                #else:
                #    img = img.resize((100, 100), Image.ANTIALIAS)
                photo = ImageTk.PhotoImage(img)
                self.type_images.append(photo)
            except Exception as e:
                print(f"No se pudo cargar {img_path}: {e}")
                img = Image.new("RGB", (100, 100), "white")
                d = ImageDraw.Draw(img)
                d.text((5, 20), "Sin Imagen", fill="black")
                photo = ImageTk.PhotoImage(img)
                self.type_images.append(photo)

        # Botones en cuadrícula 2x3
        self.type_buttons = []
        tipos = ["Tipo 1", "Tipo 2", "Tipo 3", "Tipo 4", "Tipo 5", "Tipo 6"]

        for i, tipo in enumerate(tipos):
            row = (i // 2) + 1  # +1 porque el título está en row=0
            col = i % 2

            btn = tk.Button(
                types_frame,
                text=tipo,
                image=self.type_images[i],
                compound="top",
                font=("Segoe UI", 20, "bold"),
                bg="#E0E0E0",
                fg="#000000",
                width=150,
                height=150,
                relief="raised",
                bd=2,
                command=lambda t=tipo: self._select_type(t)
            )
            btn.grid(row=row, column=col, padx=10, pady=10, sticky="nsew")
            self.type_buttons.append(btn)

        # Guardar referencia
        self.entry_valor = entry_valor
        self.lbl_family = lbl_family

        # Botón Guardar (fuera del scroll, fijo en la parte inferior)
        footer = tk.Frame(self, bg=ESTILOS["bg_main"], height=100)
        footer.pack(fill="x", side="bottom", pady=(0, 20))

        btn_guardar = BotonRedondeado(
            parent=footer,
            width=400,
            height=80,
            radio=40,
            texto="GUARDAR",
            color_fondo=ESTILOS["btn_add_bg"],
            color_hover=ESTILOS["btn_add_hover"],
            color_texto="white",
            font=("Segoe UI", 32, "bold"),
            comando=self._guardar
        )
        btn_guardar.pack(pady=10)

    def _crear_footer(self):
        footer = tk.Frame(self, bg=ESTILOS["bg_main"], height=40)
        footer.pack(fill="x", side="bottom")

    def _add_to_entry(self, char):
        """Añade o borra caracteres en el Entry."""
        current = self.entry_valor.get()
        if char == '←':
            new_text = current[:-1]
        elif char == '.':
            if '.' not in current:
                new_text = current + '.'
            else:
                return
        else:
            new_text = current + char

        if new_text == "" or self._validar_input(new_text):
            self.entry_valor.config(state="normal")
            self.entry_valor.delete(0, tk.END)
            self.entry_valor.insert(0, new_text)
            self.entry_valor.config(state="readonly")

    def _select_type(self, tipo):
        """Selecciona un tipo de fractura (solo uno)."""
        self.selected_type = tipo
        # Resaltar el botón seleccionado
        for btn in self.type_buttons:
            if btn.cget("text") == tipo:
                btn.config(bg="#4CAF50", fg="white")
            else:
                btn.config(bg="#E0E0E0", fg="#000000")

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
            self.entry_valor.config(bg="#f8d7da")
            return

        if not self.selected_type:
            messagebox.showwarning("Tipo no seleccionado", "Por favor, selecciona un tipo de fractura.")
            return

        try:
            valor = float(valor_str.replace(",", "."))
            print(f"Valor guardado: {valor}, Tipo: {self.selected_type}")
            self.resultController.save_results(
                user_id=SessionState.get_user().id,
                member_id=self.member_id,
                results=valor,
                fracture_type=self.selected_type
            )
            self.entry_valor.config(bg="#d4edda")
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
        self.entry_valor.config(state="normal", bg="#000000")
        self.entry_valor.delete(0, tk.END)
        self.entry_valor.config(state="readonly", bg="#000000")
        # Deseleccionar tipo
        self.selected_type = None
        for btn in self.type_buttons:
            btn.config(bg="#E0E0E0", fg="#000000")

    def _reload(self):
        sample = SampleState.get_sample()
        self.family = sample.family_id
        self.member_id = sample.id
        if hasattr(self, 'lbl_family') and self.lbl_family:
            self.lbl_family.config(
                text=f"Registrando resultados para familia: {self.resultController.getFamilyNameById(self.family)} a los {self.days} días"
            )

# ==============================================================================
# Botón redondeado personalizado
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