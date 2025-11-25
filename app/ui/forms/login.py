import tkinter as tk
import app.ui.utils.generic as util
from tkinter import ttk
from app.ui.controllers.login_controller import LoginController
from tkinter import messagebox
from app.state.session_state import SessionState
from app.models.user_role import UserRole
from app.ui.forms.base_view import BaseView
import os
import subprocess
from tkinter import messagebox


class App(BaseView):

    def __init__(self, parent, view_controller):
        super().__init__(parent)
        self.controller = LoginController()
        self.view_controller = view_controller
        self.session = SessionState()

        # Full Screen
        self.config(bg='gray')
        logo = util.readImage("app/ui/images/testImg.jpeg", (400, 400))

        # Frame Logo
        frame_logo = tk.Frame(self, bg='#D9D9D9', width=300, relief=tk.SOLID, padx=10, pady=10)
        frame_logo.pack(side="left", expand=tk.NO, fill=tk.BOTH)
        label = tk.Label(frame_logo, image=logo)
        label.place(x=0, y=0, relwidth=1, relheight=1)

        # Frame Login
        self.frame_form = tk.Frame(self, bg='', width=300, relief=tk.SOLID, padx=10, pady=10, background='#fcfcfc')
        self.frame_form.pack(side="left", expand=tk.YES, fill=tk.BOTH)

        # frame_form_top
        frame_form_top = tk.Frame(
            self.frame_form, height=50, bd=0, relief=tk.SOLID, bg='black')
        frame_form_top.pack(side="top", fill=tk.X)
        title = tk.Label(frame_form_top, text="Inicio de sesion", font=(
            'Times', 60, 'bold'), fg="#666a88", bg='#fcfcfc', pady=50)
        title.pack(expand=tk.YES, fill=tk.BOTH)
        # end frame_form_top

        # frame_form_fill - Aquí cargaremos dinámicamente
        self.frame_form_fill = tk.Frame(
            self.frame_form, height=50, bd=0, relief=tk.SOLID, bg='#fcfcfc')
        self.frame_form_fill.pack(side="bottom", expand=tk.YES, fill=tk.BOTH)

        # Cargar imagen de huella
        self.huella_img = util.readImage("app/ui/images/fingerPrint.png", (400, 400))  # Ajusta tamaño si es necesario

        # Estilo personalizado para el botón redondeado
        # Botón redondeado personalizado
        self.boton_alternar = BotonRedondeado(
            parent=self.frame_form,
            width=500,
            height=80,
            radio=40,
            texto="Ingresar con usuario",
            color_fondo="#3A86FF",
            color_hover="#2E75D9",
            color_texto="white",
            font=("Times", 30, "bold"),
            comando=self.alternar_login
        )

        # Posición en la esquina inferior derecha
        self.boton_alternar.place(relx=1.0, rely=1.0, anchor='se', x=-30, y=-30)

        # Posición en la esquina inferior derecha
        self.boton_alternar.place(relx=1.0, rely=1.0, anchor='se', x=-30, y=-30)

        # Botón de Finalizar (apagar dispositivo) - dentro de frame_logo
        self.boton_finalizar = BotonRedondeado(
            parent=frame_logo,  # <-- ¡Aquí cambiamos el padre!
            width=280,          # Ajustado para caber con margen
            height=60,
            radio=30,
            texto="Finalizar",
            color_fondo="#FF3B30",        # Rojo para acción crítica
            color_hover="#D6302A",
            color_texto="white",
            font=("Times", 22, "bold"),
            comando=self.confirmar_apagado
        )
        # Posicionar en esquina inferior izquierda DENTRO de frame_logo
        self.boton_finalizar.place(relx=0.0, rely=1.0, anchor='sw', x=10, y=-10)

        # Estado actual: biometría o credenciales
        self.modo_actual = "biometrico"
        self.contenido_actual = None

        # Cargar vista inicial
        self.cargar_vista_inicial()

    def cargar_vista_inicial(self):
        """Carga la vista inicial (biometría o credenciales)"""
        if self.modo_actual == "biometrico":
            self.mostrar_biometria()
        else:
            self.mostrar_credenciales()

    def alternar_login(self):
        """Alterna entre modo biometría y modo credenciales"""
        # Limpiar contenido actual
        if self.contenido_actual:
            self.contenido_actual.destroy()

        if self.modo_actual == "biometrico":
            self.modo_actual = "credenciales"
            self.mostrar_credenciales()
            self.boton_alternar.itemconfig(self.boton_alternar.texto, text="Ingresar con huella")
        else:
            self.modo_actual = "biometrico"
            self.mostrar_biometria()
            self.boton_alternar.itemconfig(self.boton_alternar.texto, text="Ingresar con usuario")

    def mostrar_biometria(self):
        """Muestra la interfaz de ingreso por huella digital"""
        frame_biometria = tk.Frame(self.frame_form_fill, bg='#fcfcfc')
        frame_biometria.pack(expand=True, fill=tk.BOTH, padx=20, pady=20)

        # Imagen de huella dactilar como botón
        boton_huella = tk.Button(
            frame_biometria,
            image=self.huella_img,
            bg='#fcfcfc',
            bd=0,
            activebackground='#fcfcfc',
            command=self.iniciar_sesion_biometrico
        )
        boton_huella.image = self.huella_img  # Mantener referencia
        boton_huella.pack(pady=20)

        # Texto instructivo
        titulo = tk.Label(
            frame_biometria,
            text="Ingrese su huella",
            font=('Times', 40, 'bold'),  # Más grande y en negrita
            fg="#666a88",
            bg='#fcfcfc'
        )
        titulo.pack(pady=10)

        self.contenido_actual = frame_biometria

    def iniciar_sesion_biometrico(self):
        if self.controller.fingerPrintLogin():
            user = self.session.get_user()
            if UserRole.OPERATIVE == user.role:
                self.view_controller.show_frame("SampleListFrame")
                return
            if UserRole.ADMIN == user.role:
                print("Usuario con rol ADMIN autenticado.")
                self.view_controller.show_frame("AdminView")
                return

    def mostrar_credenciales(self):
        """Muestra los campos de usuario y contraseña"""
        frame_credenciales = tk.Frame(self.frame_form_fill, bg='#fcfcfc')
        frame_credenciales.pack(expand=True, fill=tk.BOTH)

        # Definir una fuente más grande y en negrita
        font_estilo = ('Times', 50, 'bold')

        # Etiqueta y campo de Usuario
        etiqueta_usuario = tk.Label(
            frame_credenciales,
            text="Usuario",
            font=font_estilo,
            fg="#666a88",
            bg='#fcfcfc',
            anchor="w"
        )
        etiqueta_usuario.pack(fill=tk.X, padx=20, pady=5)

        self.usuario = ttk.Entry(
            frame_credenciales,
            font=font_estilo
        )
        self.usuario.pack(fill=tk.X, padx=20, pady=10, ipady=8)

        # Etiqueta y campo de Contraseña
        etiqueta_password = tk.Label(
            frame_credenciales,
            text="Contraseña",
            font=font_estilo,
            fg="#666a88",
            bg='#fcfcfc',
            anchor="w"
        )
        etiqueta_password.pack(fill=tk.X, padx=20, pady=5)

        self.password = ttk.Entry(
            frame_credenciales,
            font=font_estilo,
            show="*"
        )
        self.password.pack(fill=tk.X, padx=20, pady=10, ipady=8)

        # Botón de inicio de sesión
        inicio = BotonRedondeado(
            parent=frame_credenciales,  # Ahora el padre es el frame donde están los campos
            width=500,
            height=80,
            radio=40,
            texto="Ingresar",
            color_fondo="#673AB7",
            color_hover="#512DA8", 
            color_texto="white",
            font=("Times", 30, "bold"),
            comando=self.iniciar_sesion  # Asegúrate de usar el comando correcto
        )
        inicio.pack(fill=tk.X, padx=20, pady=20)  # Se empaqueta después de crearlo
        inicio.bind("<Return>", (lambda event: self.verificar()))

        self.contenido_actual = frame_credenciales

    def iniciar_sesion(self):
        username = self.usuario.get().strip()
        password = self.password.get().strip()

        if not username or not password:
            messagebox.showerror("Error", "Debes ingresar usuario y contraseña.")
            return

        if self.controller.login(username=username, password=password):
            # ✅ Guardar el usuario autenticado en SessionState
            user = self.session.get_user()

            # Si el LoginController no lo guarda automáticamente, forzamos el guardado:
            from app.state.session_state import SessionState
            SessionState.set_user(user)

            print(f"Usuario autenticado: {user.username} con rol {user.role}")

            if UserRole.OPERATIVE == user.role:
                self.view_controller.show_frame("SampleListFrame")
                return
            elif UserRole.ADMIN == user.role:
                print("Usuario con rol ADMIN autenticado.")
                self.view_controller.show_frame("AdminView")
                return
            else:
                messagebox.showinfo("Error", "El rol asignado al usuario no es válido.")
        else:
            messagebox.showerror("Error", "Nombre de usuario o contraseña incorrectos.")

    def verificar(self):
        print("Verificando...")
    
    def confirmar_apagado(self):
        respuesta = messagebox.askyesno(
            "Confirmar apagado",
            "¿Está seguro que desea apagar el dispositivo?\n\n"
            "Toda la actividad se detendrá y el sistema se cerrará."
        )
        if respuesta:
            self.apagar_dispositivo()

    def apagar_dispositivo(self):
        try:
            # Comando para apagar en Linux (Raspberry Pi)
            subprocess.run(["sudo", "shutdown", "-h", "now"], check=True)
        except subprocess.CalledProcessError as e:
            messagebox.showerror("Error", f"No se pudo apagar el dispositivo:\n{e}")
        except FileNotFoundError:
            messagebox.showerror("Error", "El comando 'shutdown' no está disponible.")


class BotonRedondeado(tk.Canvas):
    def __init__(self, parent, width=200, height=60, radio=25,
                texto="Botón", color_fondo="#3A86FF", color_hover="#2E75D9",
                color_texto="white", font=("Times", 24, "bold"), comando=None):
        super().__init__(parent, width=width, height=height, bg=parent.cget("bg"),
                        highlightthickness=0, bd=0)

        self.radio = radio
        self.color_fondo = color_fondo
        self.color_hover = color_hover
        self.comando = comando

        # Dibuja el botón redondeado
        self.rect = self.crear_rectangulo_redondeado(0, 0, width, height, radio, fill=color_fondo)
        self.texto = self.create_text(width / 2, height / 2, text=texto, fill=color_texto, font=font)

        # Efectos
        self.bind("<Enter>", self.on_enter)
        self.bind("<Leave>", self.on_leave)
        self.bind("<Button-1>", self.on_click)

    def crear_rectangulo_redondeado(self, x1, y1, x2, y2, r=25, **kwargs):
        """Dibuja un rectángulo con esquinas redondeadas"""
        points = (
            x1 + r, y1,
            x1 + r, y1,
            x2 - r, y1,
            x2 - r, y1,
            x2, y1,
            x2, y1 + r,
            x2, y1 + r,
            x2, y2 - r,
            x2, y2 - r,
            x2, y2,
            x2 - r, y2,
            x2 - r, y2,
            x1 + r, y2,
            x1 + r, y2,
            x1, y2,
            x1, y2 - r,
            x1, y2 - r,
            x1, y1 + r,
            x1, y1 + r,
            x1, y1
        )
        return self.create_polygon(points, smooth=True, outline="", **kwargs)

    def on_enter(self, event):
        self.itemconfig(self.rect, fill=self.color_hover)

    def on_leave(self, event):
        self.itemconfig(self.rect, fill=self.color_fondo)

    def on_click(self, event):
        if self.comando:
            self.comando()