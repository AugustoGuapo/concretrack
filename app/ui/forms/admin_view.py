import tkinter as tk
from tkinter import ttk, messagebox
import os
from app.ui.utils.terminal import TerminalApp

class AdminView(TerminalApp):

    def __init__(self):
        super().__init__()

        self.title("Administración de Usuarios")

        # Full Screen
        self.attributes('-fullscreen', True)
        self.config(bg='gray')
        self.resizable(width=False, height=False)

        # ✅ NO hay frame_logo, se eliminó por completo

        # Frame principal para contenido
        self.frame_content = tk.Frame(self, bg='#fcfcfc')
        self.frame_content.pack(side="top", expand=True, fill=tk.BOTH)  # Ahora ocupa toda la pantalla

        # Frame para los botones
        button_frame = tk.Frame(self.frame_content, bg='#fcfcfc')
        button_frame.pack(pady=20)

        # Botón Agregar
        self.btn_agregar = BotonRedondeado(
            parent=button_frame,
            width=400,
            height=80,
            radio=40,
            texto="Agregar",
            color_fondo="#4CAF50",
            color_hover="#388E3C",
            color_texto="white",
            font=("Times", 30, "bold"),
            comando=self.agregar_usuario
        )
        self.btn_agregar.grid(row=0, column=0, padx=10)

        # Botón Eliminar
        self.btn_eliminar = BotonRedondeado(
            parent=button_frame,
            width=400,
            height=80,
            radio=40,
            texto="Eliminar",
            color_fondo="#F44336",
            color_hover="#D32F2F",
            color_texto="white",
            font=("Times", 30, "bold"),
            comando=self.eliminar_usuario
        )
        self.btn_eliminar.grid(row=0, column=1, padx=10)

        # Botón Editar
        self.btn_editar = BotonRedondeado(
            parent=button_frame,
            width=400,
            height=80,
            radio=40,
            texto="Editar",
            color_fondo="#FF9800",
            color_hover="#F57C00",
            color_texto="white",
            font=("Times", 30, "bold"),
            comando=self.editar_usuario
        )
        self.btn_editar.grid(row=0, column=2, padx=10)

        # Frame para la lista de usuarios
        list_frame = tk.Frame(self.frame_content, bg='#fcfcfc')
        list_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)

        # Listbox con Scrollbar
        self.listbox = tk.Listbox(
            list_frame,
            font=("Arial", 50),
            selectbackground="#4CAF50",
            selectforeground="white",
            activestyle="none",
            bd=0,
            highlightthickness=0
        )
        self.listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        scrollbar_y = tk.Scrollbar(list_frame, orient=tk.VERTICAL, command=self.listbox.yview)
        scrollbar_y.pack(side=tk.RIGHT, fill=tk.Y)

        self.listbox.config(yscrollcommand=scrollbar_y.set)

        # Datos iniciales (puedes cambiar por cargar desde JSON)
        self.usuarios = [
            {"nombre": "Lamar yi", "rol": "PM"},
            {"nombre": "El inge", "rol": "Inge"},
        ]
        self.actualizar_lista()
        self.validar_estado_botones()

        # Evitar cierre accidental
        self.protocol("WM_DELETE_WINDOW", self.do_nothing)
        self.mainloop()

    def toggle_seleccion(self, event):
        widget = event.widget
        index = widget.nearest(event.y)  # Índice del elemento bajo el clic

        if index == -1:
            return  # Fuera de rango

        if index in widget.curselection():
            # Si ya estaba seleccionado, deseleccionarlo
            widget.selection_clear(index)
            # Opcional: desactivar botones si no hay selección
            self.btn_editar.config(state=tk.DISABLED)
            self.btn_eliminar.config(state=tk.DISABLED)
        else:
            # Tkinter ya maneja la selección automática, no necesitas cambiarla
            pass

    def actualizar_lista(self):
        self.listbox.delete(0, tk.END)
        for usuario in self.usuarios:
            self.listbox.insert(tk.END, f"      {usuario['nombre']} - {usuario['rol']}      ")

    def validar_estado_botones(self):
        estado = tk.NORMAL if self.usuarios else tk.DISABLED
        self.btn_eliminar.config(state=estado)
        self.btn_editar.config(state=estado)

    def agregar_usuario(self):
        self.usuarios.append({"nombre": "Nuevo Usuario", "rol": "Sin rol"})
        self.actualizar_lista()
        self.validar_estado_botones()

    def eliminar_usuario(self):
        selected_index = self.listbox.curselection()
        if selected_index:
            index = selected_index[0]
            del self.usuarios[index]
            self.actualizar_lista()
            self.validar_estado_botones()

    def editar_usuario(self):
        selected_index = self.listbox.curselection()
        if selected_index:
            index = selected_index[0]
            nombre_actual = self.usuarios[index]["nombre"]
            rol_actual = self.usuarios[index]["rol"]

            self.show_edit_dialog(index, nombre_actual, rol_actual)

    def show_edit_dialog(self, index, nombre_actual, rol_actual):
        dialog = tk.Toplevel(self)
        dialog.title("Editar Usuario")
        dialog.geometry("400x200")
        dialog.transient(self)
        dialog.grab_set()

        # Fondo igual al del frame_content para que parezca "transparente"

        tk.Label(dialog, text="Nombre:", font=("Arial", 14)).pack(pady=5)
        entry_nombre = tk.Entry(dialog, font=("Arial", 14))
        entry_nombre.insert(0, nombre_actual)
        entry_nombre.pack()

        tk.Label(dialog, text="Rol:", font=("Arial", 14)).pack(pady=5)
        entry_rol = tk.Entry(dialog, font=("Arial", 14))
        entry_rol.insert(0, rol_actual)
        entry_rol.pack()

        def guardar():
            new_nombre = entry_nombre.get().strip()
            new_rol = entry_rol.get().strip()
            if new_nombre and new_rol:
                self.usuarios[index]["nombre"] = new_nombre
                self.usuarios[index]["rol"] = new_rol
                self.actualizar_lista()
                self.validar_estado_botones()
                dialog.destroy()

        # Botón con estilo personalizado (verde oscuro y texto blanco)
        tk.Button(
            dialog,
            text="Guardar",
            command=guardar,
            font=("Arial", 14),
            bg="#388E3C",   # Verde oscuro (similar al botón Agregar)
            relief="flat",
            padx=10,
            pady=5
        ).pack(pady=10)

    def do_nothing(self):
        pass

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
