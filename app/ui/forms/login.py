import tkinter as tk
from tkinter.font import BOLD
import utils.generic as util
from forms.master import MasterPanel
from tkinter import ttk

class App:

    def __init__(self):
        self.ventana = tk.Tk()
        self.ventana.title("Login")

        # Full Screen
        self.ventana.attributes('-fullscreen', True)

        self.ventana.config(bg='gray')
        self.ventana.resizable(width=0, height=0)

        logo = util.readImage("./images/testImg.jpeg", (400, 400))

        # Frame Logo
        frame_logo = tk.Frame(self.ventana, bg='', width=300, relief=tk.SOLID, padx=10, pady=10)
        frame_logo.pack(side="left", expand=tk.NO, fill=tk.BOTH)
        label = tk.Label(frame_logo, image=logo)
        label.place(x=0, y=0, relwidth=1, relheight=1)

        # Frame Login
        frame_form = tk.Frame(self.ventana, bg='', width=300, relief=tk.SOLID, padx=10, pady=10, background='#fcfcfc')
        frame_form.pack(side="left", expand=tk.YES, fill=tk.BOTH)

        # frame_form_top
        frame_form_top = tk.Frame(
            frame_form, height=50, bd=0, relief=tk.SOLID, bg='black')
        frame_form_top.pack(side="top", fill=tk.X)
        title = tk.Label(frame_form_top, text="Inicio de sesion", font=(
            'Times', 30), fg="#666a88", bg='#fcfcfc', pady=50)
        title.pack(expand=tk.YES, fill=tk.BOTH)
        # end frame_form_top

        # frame_form_fill
        frame_form_fill = tk.Frame(
            frame_form, height=50,  bd=0, relief=tk.SOLID, bg='#fcfcfc')
        frame_form_fill.pack(side="bottom", expand=tk.YES, fill=tk.BOTH)

        etiqueta_usuario = tk.Label(frame_form_fill, text="Usuario", font=(
            'Times', 14), fg="#666a88", bg='#fcfcfc', anchor="w")
        etiqueta_usuario.pack(fill=tk.X, padx=20, pady=5)
        self.usuario = ttk.Entry(frame_form_fill, font=('Times', 14), textvariable="hola")
        self.usuario.insert(0, "root")
        self.usuario.pack(fill=tk.X, padx=20, pady=10)

        etiqueta_password = tk.Label(frame_form_fill, text="Contraseña", font=(
            'Times', 14), fg="#666a88", bg='#fcfcfc', anchor="w")
        etiqueta_password.pack(fill=tk.X, padx=20, pady=5)
        self.password = ttk.Entry(frame_form_fill, font=('Times', 14))
        self.password.pack(fill=tk.X, padx=20, pady=10)
        self.password.config(show="*")

        # Botón de inicio de sesión
        inicio = tk.Button(frame_form_fill, text="Iniciar sesión", font=(
            'Times', 15), bg='gray', bd=0, fg="black", command=self.iniciar_sesion)
        inicio.pack(fill=tk.X, padx=20, pady=20)
        inicio.bind("<Return>", (lambda event: self.verificar()))

        self.ventana.mainloop()

    def iniciar_sesion(self):
        # Aquí se cierra la ventana actual y se abre la ventana de EvaluadorUI
        self.ventana.destroy()  # Cierra la ventana de Login
        #evaluador_ui = EvaluadorUI()  # Llama a la vista EvaluadorUI

    def verificar(self):
        # Puedes agregar la lógica de verificación aquí si es necesario
        print("Verificando...")

