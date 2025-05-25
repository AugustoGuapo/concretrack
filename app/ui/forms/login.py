import tkinter as tk
import app.ui.utils.generic as util
from tkinter import ttk
from app.ui.utils.terminal import TerminalApp
from app.ui.controllers.login_controller import LoginController
from tkinter import messagebox


class App(TerminalApp):

    def __init__(self):
        super().__init__()
        self.title("Login")
        self.controller = LoginController()

        # Full Screen
        self.attributes('-fullscreen', True)
        self.config(bg='gray')
        self.resizable(width=0, height=0)

        logo = util.readImage("app/ui/images/testImg.jpeg", (400, 400))

        # Frame Logo
        frame_logo = tk.Frame(self, bg='#D9D9D9', width=300, relief=tk.SOLID, padx=10, pady=10)
        frame_logo.pack(side="left", expand=tk.NO, fill=tk.BOTH)
        label = tk.Label(frame_logo, image=logo)
        label.place(x=0, y=0, relwidth=1, relheight=1)

        # Frame Login
        frame_form = tk.Frame(self, bg='', width=300, relief=tk.SOLID, padx=10, pady=10, background='#fcfcfc')
        frame_form.pack(side="left", expand=tk.YES, fill=tk.BOTH)

        # frame_form_top
        frame_form_top = tk.Frame(
            frame_form, height=50, bd=0, relief=tk.SOLID, bg='black')
        frame_form_top.pack(side="top", fill=tk.X)
        title = tk.Label(frame_form_top, text="Inicio de sesion", font=(
            'Times', 30), fg="#666a88", bg='#fcfcfc', pady=50)
        title.pack(expand=tk.YES, fill=tk.BOTH)
        # end frame_form_top

        # frame_form_fill - Aquí cargaremos dinámicamente
        self.frame_form_fill = tk.Frame(
            frame_form, height=50, bd=0, relief=tk.SOLID, bg='#fcfcfc')
        self.frame_form_fill.pack(side="bottom", expand=tk.YES, fill=tk.BOTH)

        # Cargar imagen de huella
        self.huella_img = util.readImage("app/ui/images/fingerPrint.png", (150, 150))  # Ajusta tamaño si es necesario

        # Botón de alternancia (en la esquina inferior derecha)
        self.boton_alternar = tk.Button(
            frame_form,
            text="Ingresar con usuario",
            font=('Times', 20, 'bold'),
            fg="black",
            bg='gray',
            bd=0,
            command=self.alternar_login
        )
        self.boton_alternar.place(relx=1.0, rely=1.0, anchor='se', x=-20, y=-20)  # Esquina inferior derecha

        # Estado actual: biometría o credenciales
        self.modo_actual = "biometrico"
        self.contenido_actual = None

        # Cargar vista inicial
        self.cargar_vista_inicial()

        self.mainloop()

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
            self.boton_alternar.config(text="Ingresar con huella")
        else:
            self.modo_actual = "biometrico"
            self.mostrar_biometria()
            self.boton_alternar.config(text="Ingresar con usuario")

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
            font=('Times', 30, 'bold'),  # Más grande y en negrita
            fg="#666a88",
            bg='#fcfcfc'
        )
        titulo.pack(pady=10)

        self.contenido_actual = frame_biometria

    def iniciar_sesion_biometrico(self):
        if self.controller.fingerPrintLogin():
            self.destroy()

    def mostrar_credenciales(self):
        """Muestra los campos de usuario y contraseña"""
        frame_credenciales = tk.Frame(self.frame_form_fill, bg='#fcfcfc')
        frame_credenciales.pack(expand=True, fill=tk.BOTH)

        # Definir una fuente más grande y en negrita
        font_estilo = ('Times', 25, 'bold')

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
            font=font_estilo,
            textvariable="hola"
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
        inicio = tk.Button(
            frame_credenciales,
            text="Iniciar sesión",
            font=font_estilo,
            bg='gray',
            bd=0,
            fg="black",
            command=self.iniciar_sesion
        )
        inicio.pack(fill=tk.X, padx=20, pady=20)
        inicio.bind("<Return>", (lambda event: self.verificar()))

        self.contenido_actual = frame_credenciales

    def iniciar_sesion(self):
        if self.controller.login(
            username=self.usuario.get(),
            password=self.password.get()
        ):
            messagebox.showinfo("Inicio de sesión", "¡Inicio de sesión exitoso!")
            self.destroy()
        else:
            messagebox.showerror("Error", "Nombre de usuario o contraseña incorrectos.")

    def verificar(self):
        print("Verificando...")