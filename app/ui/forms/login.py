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

# 🔽 Importamos el teclado desde tu módulo
from app.ui.components.virtual_keyboard import VirtualKeyboard


# ==============================
# Botón redondeado (reutilizado)
# ==============================
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
        self.keyboard = None

        self.rect = self.crear_rectangulo_redondeado(0, 0, width, height, radio, fill=color_fondo)
        self.texto = self.create_text(width / 2, height / 2, text=texto, fill=color_texto, font=font)

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
        return self.create_polygon(points, smooth=True, outline="", **kwargs)

    def on_enter(self, event):
        self.itemconfig(self.rect, fill=self.color_hover)

    def on_leave(self, event):
        self.itemconfig(self.rect, fill=self.color_fondo)

    def on_click(self, event):
        if self.comando:
            self.comando()


# ==============================
# Vista principal de login
# ==============================
class App(BaseView):
    def __init__(self, parent, view_controller):
        super().__init__(parent)
        self.controller = LoginController()
        self.view_controller = view_controller
        self.session = SessionState()

        self.config(bg='gray')
        logo = util.readImage("app/ui/images/testImg.jpeg", (400, 400))

        # Frame Logo
        frame_logo = tk.Frame(self, bg='#D9D9D9', width=300, relief=tk.SOLID, padx=10, pady=10)
        frame_logo.pack(side="left", expand=tk.NO, fill=tk.BOTH)
        label = tk.Label(frame_logo, image=logo, bg='#D9D9D9')
        label.place(x=0, y=0, relwidth=1, relheight=1)

        # Botón Finalizar (enderezado a la derecha dentro del logo)
        self.boton_finalizar = BotonRedondeado(
            parent=frame_logo,
            width=280,
            height=60,
            radio=30,
            texto="Finalizar",
            color_fondo="#FF3B30",
            color_hover="#D6302A",
            color_texto="white",
            font=("Times", 22, "bold"),
            comando=self.confirmar_apagado
        )
        self.boton_finalizar.place(relx=1.0, rely=1.0, anchor='se', x=-10, y=-10)

        # Frame Login
        self.frame_form = tk.Frame(self, bg='#fcfcfc', width=300, relief=tk.SOLID, padx=10, pady=10)
        self.frame_form.pack(side="left", expand=tk.YES, fill=tk.BOTH)

        # Título
        frame_form_top = tk.Frame(self.frame_form, height=50, bd=0, relief=tk.SOLID, bg='black')
        frame_form_top.pack(side="top", fill=tk.X)
        title = tk.Label(
            frame_form_top,
            text="Inicio de sesion",
            font=('Times', 60, 'bold'),
            fg="#666a88",
            bg='#fcfcfc',
            pady=50
        )
        title.pack(expand=tk.YES, fill=tk.BOTH)

        # Área dinámica
        self.frame_form_fill = tk.Frame(self.frame_form, bd=0, relief=tk.SOLID, bg='#fcfcfc')
        self.frame_form_fill.pack(side="top", expand=tk.YES, fill=tk.BOTH)

        # Imagen de huella
        self.huella_img = util.readImage("app/ui/images/fingerPrint.png", (400, 400))

        # Botón alternar
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
        self.boton_alternar.place(relx=1.0, rely=1.0, anchor='se', x=-30, y=-30)

        self.modo_actual = "biometrico"
        self.contenido_actual = None
        self.keyboard = None  # ✅ ¡Esta línea es la que falta!

        self.cargar_vista_inicial()

    def cargar_vista_inicial(self):
        if self.modo_actual == "biometrico":
            self.mostrar_biometria()
        else:
            self.mostrar_credenciales()

    def alternar_login(self):
        # Ocultar teclado si existe
        if self.keyboard:
            self.keyboard.hide()

        if self.contenido_actual:
            self.contenido_actual.destroy()
            self.contenido_actual = None

        if self.modo_actual == "biometrico":
            self.modo_actual = "credenciales"
            self.mostrar_credenciales()
            self.boton_alternar.itemconfig(self.boton_alternar.texto, text="Ingresar con huella")
        else:
            self.modo_actual = "biometrico"
            self.mostrar_biometria()
            self.boton_alternar.itemconfig(self.boton_alternar.texto, text="Ingresar con usuario")

    def mostrar_biometria(self):
        frame_biometria = tk.Frame(self.frame_form_fill, bg='#fcfcfc')
        frame_biometria.pack(expand=True, fill=tk.BOTH, padx=20, pady=20)

        boton_huella = tk.Button(
            frame_biometria,
            image=self.huella_img,
            bg='#fcfcfc',
            bd=0,
            activebackground='#fcfcfc',
            command=self.iniciar_sesion_biometrico
        )
        boton_huella.image = self.huella_img
        boton_huella.pack(pady=20)

        titulo = tk.Label(
            frame_biometria,
            text="Ingrese su huella",
            font=('Times', 40, 'bold'),
            fg="#666a88",
            bg='#fcfcfc'
        )
        titulo.pack(pady=10)

        self.contenido_actual = frame_biometria

    def iniciar_sesion_biometrico(self):
        try:
            # Intentar autenticación biométrica
            if self.controller.fingerPrintLogin():
                user = self.session.get_user()
                if user.role == UserRole.OPERATIVE:
                    self.view_controller.show_frame("SampleListFrame")
                    return
                elif user.role == UserRole.ADMIN:
                    self.view_controller.show_frame("AdminView")
                    return
            else:
                # Huella no reconocida o no registrada
                messagebox.showwarning(
                    "Huella no reconocida",
                    "No se encontró una huella dactilar registrada.\n"
                    "Por favor, inténtelo nuevamente o use usuario y contraseña."
                )
                # Opcional: podrías alternar automáticamente aquí, pero mejor dar opción
                return

        except Exception as e:
            # Cualquier error de hardware, conexión, inicialización, etc.
            print(f"Error en autenticación biométrica: {e}")
            messagebox.showerror(
                "Sensor no disponible",
                "No se pudo acceder al lector de huellas.\n"
                "La autenticación por huella no está disponible en este momento.\n\n"
                "Se cambiará al modo de usuario y contraseña."
            )
            # Cambiar automáticamente al modo credenciales
            self.alternar_login()

    def mostrar_credenciales(self):
        frame_credenciales = tk.Frame(self.frame_form_fill, bg='#fcfcfc')
        frame_credenciales.pack(expand=True, fill=tk.BOTH, padx=20, pady=(20, 0))

        font_estilo = ('Times', 50, 'bold')

        # Usuario
        tk.Label(frame_credenciales, text="Usuario", font=font_estilo, fg="#666a88", bg='#fcfcfc', anchor="w").pack(fill=tk.X, padx=10, pady=5)
        self.usuario = ttk.Entry(frame_credenciales, font=font_estilo)
        self.usuario.pack(fill=tk.X, padx=10, pady=10, ipady=8)

        # Contraseña
        tk.Label(frame_credenciales, text="Contraseña", font=font_estilo, fg="#666a88", bg='#fcfcfc', anchor="w").pack(fill=tk.X, padx=10, pady=5)
        self.password = ttk.Entry(frame_credenciales, font=font_estilo, show="*")
        self.password.pack(fill=tk.X, padx=10, pady=10, ipady=8)

        # Botón Ingresar
        inicio = BotonRedondeado(
            parent=frame_credenciales,
            width=500,
            height=80,
            radio=40,
            texto="Ingresar",
            color_fondo="#673AB7",
            color_hover="#512DA8",
            color_texto="white",
            font=("Times", 30, "bold"),
            comando=self.iniciar_sesion
        )
        inicio.pack(pady=20)

        # 🔽 Crear un solo teclado (si no existe)
        if self.keyboard is None:
            self.keyboard = VirtualKeyboard(self.frame_form_fill)

        # 🔽 Vincular teclado con campos al enfocar
        self.usuario.bind("<FocusIn>", lambda e: self.keyboard.set_active_entry(self.usuario))
        self.password.bind("<FocusIn>", lambda e: self.keyboard.set_active_entry(self.password))

        # Mostrar teclado
        self.keyboard.show()

        self.contenido_actual = frame_credenciales

    def iniciar_sesion(self):
        username = self.usuario.get().strip()
        password = self.password.get().strip()

        if not username or not password:
            messagebox.showerror("Error", "Debes ingresar usuario y contraseña.")
            return

        if self.controller.login(username=username, password=password):
            user = self.session.get_user()
            SessionState.set_user(user)

            # Ocultar teclado al loguearse
            if self.keyboard:
                self.keyboard.hide()

            if user.role == UserRole.OPERATIVE:
                self.view_controller.show_frame("SampleListFrame")
            elif user.role == UserRole.ADMIN:
                self.view_controller.show_frame("AdminView")
            else:
                messagebox.showerror("Error", "Rol de usuario no válido.")
        else:
            messagebox.showerror("Error", "Usuario o contraseña incorrectos.")

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
            subprocess.run(["sudo", "shutdown", "-h", "now"], check=True)
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo apagar el dispositivo:\n{e}")