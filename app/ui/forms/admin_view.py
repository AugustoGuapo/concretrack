import tkinter as tk
from tkinter import ttk
from app.ui.controllers.admin_controller import AdminController
from app.ui.forms.base_view import BaseView
from app.models.user_role import UserRole
from PIL import Image, ImageTk
from app.ui.forms.login import BotonRedondeado
from app.ui.utils.generic import readImage
from app.state.session_state import SessionState  # Import necesario para logout
import time
import tkinter.messagebox
from tkinter import messagebox

class AdminView(BaseView):
    def __init__(self, parent, view_controller):
        super().__init__(parent)
        self.admin_controller = AdminController()
        self.view_controller = view_controller

        # Configuración principal
        self.config(bg='gray')

        # Crear encabezado con usuario y botón de cerrar sesión
        self.create_header()

        # Frame principal para contenido
        self.frame_content = tk.Frame(self, bg='#fcfcfc')
        self.frame_content.pack(side="top", expand=True, fill=tk.BOTH, pady=(10, 0))  # Dejamos espacio para el header

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
        self.usuarios = self.admin_controller.get_all_users()

        self.actualizar_lista()
        self.validar_estado_botones()

        # Vincular evento de selección/deselección
        self.listbox.bind("<Button-1>", self.toggle_seleccion)

    def create_header(self):
        """Crea el encabezado con nombre de usuario y botón de cierre de sesión."""
        self.header_frame = tk.Frame(self, bg="#BDE5F8", bd=1, relief=tk.RAISED)
        self.header_frame.pack(fill=tk.X, padx=5, pady=5)

        try:
            username = SessionState.get_user().getFullName()
        except Exception:
            username = "Invitado"

        user_label = tk.Label(
            self.header_frame, text=username, bg="#BDE5F8",
            fg="#005970", font=("Arial", 20, "bold")
        )
        user_label.pack(side=tk.LEFT, padx=10, pady=5)

        close_button = tk.Button(
            self.header_frame, text="Cerrar Sesión  ➤", bg="#FF0000",
            fg="white", font=("Arial", 20, "bold"), bd=0,
            activebackground="#CC0000", activeforeground="white",
            command=self.logout
        )
        close_button.pack(side=tk.RIGHT, padx=10, pady=5)

    def logout(self):
        """Cierra sesión y redirige al Login."""
        SessionState.clear_user()
        if hasattr(self.view_controller, "show_frame"):
            from app.ui.forms.login import App as Login
            if "Login" not in self.view_controller.frame_classes:
                self.view_controller.frame_classes["Login"] = Login
            self.view_controller.show_frame("Login")
            login_frame = self.view_controller.frames.get("Login")
            if login_frame and hasattr(login_frame, "clear_fields"):
                login_frame.clear_fields()

    def toggle_seleccion(self, event):
        """Permite seleccionar o deseleccionar un elemento en la lista."""
        widget = event.widget
        index = widget.nearest(event.y)  # Índice del elemento bajo el clic
        if index == -1:
            return  # Fuera de rango
        if index in widget.curselection():
            # Si ya estaba seleccionado, deseleccionarlo
            widget.selection_clear(index)
            # Desactivar botones si no hay selección
            self.btn_editar.config(state=tk.DISABLED)
            self.btn_eliminar.config(state=tk.DISABLED)
        else:
            # Tkinter ya maneja la selección automática
            pass

    def actualizar_lista(self):
        """Actualiza la lista de usuarios mostrada."""
        self.listbox.delete(0, tk.END)
        for usuario in self.usuarios:
            self.listbox.insert(tk.END, f"      {usuario['nombre']} - {usuario['rol']}      ")

    def validar_estado_botones(self):
        """Habilita o deshabilita botones según si hay usuarios disponibles."""
        estado = tk.NORMAL if self.usuarios else tk.DISABLED
        self.btn_eliminar.config(state=estado)
        self.btn_editar.config(state=estado)

    def mostrar_ventana_emergente(self):
        """Muestra un formulario dentro del mismo frame (no ventana separada)."""
        # Limpiar contenido actual
        for widget in self.frame_content.winfo_children():
            widget.destroy()

        form_frame = tk.Frame(self.frame_content, bg="white")
        form_frame.pack(fill="both", expand=True)

        fuente = ("Arial", 20)
        ancho_entry = 30
        pady_campo = 20

        # Título
        tk.Label(form_frame, text="Registrar nuevo usuario", font=("Arial", 28, "bold"), bg="white").pack(pady=20)

        # Nombre
        tk.Label(form_frame, text="Nombre", font=fuente, bg="white").pack(pady=(pady_campo, 5))
        entry_nombre = tk.Entry(form_frame, font=fuente, width=ancho_entry)
        entry_nombre.pack()

        # Apellido
        tk.Label(form_frame, text="Apellido", font=fuente, bg="white").pack(pady=(pady_campo, 5))
        entry_apellido = tk.Entry(form_frame, font=fuente, width=ancho_entry)
        entry_apellido.pack()

        # Contraseña
        tk.Label(form_frame, text="Contraseña", font=fuente, bg="white").pack(pady=(pady_campo, 5))
        entry_contrasena = tk.Entry(form_frame, show="*", font=fuente, width=ancho_entry)
        entry_contrasena.pack()

        # Rol
        tk.Label(form_frame, text="Rol", font=fuente, bg="white").pack(pady=(pady_campo, 5))
        rol_var = tk.StringVar(form_frame)
        rol_var.set("Seleccionar rol")

        opciones_rol = ["Administrador", "Operario"]
        opciones_rol_enum = {
            "Administrador": UserRole.ADMIN,
            "Operario": UserRole.OPERATIVE
        }

        menu_rol = tk.OptionMenu(form_frame, rol_var, *opciones_rol)
        menu_rol.config(font=fuente, width=ancho_entry)
        menu_rol.pack()

        # Guardar usuario
        def guardar_usuario():
            nombre = entry_nombre.get().strip()
            apellido = entry_apellido.get().strip()
            contrasena = entry_contrasena.get().strip()
            rol_texto = rol_var.get().strip()
            rol = opciones_rol_enum.get(rol_texto, None)

            if not nombre or not apellido or not contrasena or rol is None:
                messagebox.showerror("Error", "Completa todos los campos correctamente.")
                return

            # Primero capturamos la huella y obtenemos su id
            fingerprint_id = self.mostrar_ventana_biometrica()
            if fingerprint_id is None or (isinstance(fingerprint_id, int) and fingerprint_id < 0):
                messagebox.showerror("Error", "No se pudo obtener la huella. Registro cancelado.")
                return

            try:
                # Si el controlador acepta fingerprint_id se lo pasamos como kwarg.
                # Si no, quitar el argumento y adaptar según la firma de AdminController.
                self.admin_controller.create_user(
                    firstName=nombre,
                    lastName=apellido,
                    password=contrasena,
                    role=rol,
                    fingerprintId=fingerprint_id
                )
                messagebox.showinfo("Éxito", f"Usuario registrado correctamente (huella #{fingerprint_id})")
                self.usuarios = self.admin_controller.get_all_users()
                self.volver_a_lista()
            except Exception as e:
                messagebox.showerror("Error", f"No se pudo registrar el usuario:\n{e}")

        # Botones
        tk.Button(
            form_frame,
            text="Guardar Usuario",
            font=("Arial", 22, "bold"),
            bg="#4CAF50",
            fg="white",
            height=2,
            width=20,
            relief="flat",
            command=guardar_usuario
        ).pack(pady=40)

        tk.Button(
            form_frame,
            text="Volver",
            font=("Arial", 18),
            bg="#D32F2F",
            fg="white",
            height=2,
            width=20,
            relief="flat",
            command=self.volver_a_lista
        ).pack(pady=10)
                # Botones


        

    def mostrar_ventana_biometrica(self) -> int:

        # Creamos una ventana modal para mostrar instrucciones durante la captura
        ventana = tk.Toplevel(self)
        ventana.title("Captura de huella")
        ventana.transient(self)
        ventana.grab_set()
        ventana.geometry("600x200")

        texto_instruccion = tk.StringVar(ventana, value="Por favor, coloque su dedo en el lector biométrico")
        label_instr = tk.Label(ventana, textvariable=texto_instruccion, font=("Arial", 18))
        label_instr.pack(pady=20, padx=20)

        # Botón cancelar por si se desea abortar
        def cancelar():
            ventana.destroy()

        btn_cancel = tk.Button(ventana, text="Cancelar", font=("Arial", 14), command=cancelar)
        btn_cancel.pack(pady=10)

        ventana.update()

        fingerprintId = None

        while True:
            try:
                texto_instruccion.set("Esperando huella...")
                ventana.update()
                # Llamada al controlador para iniciar captura (puede bloquear o lanzar excepción)
                isAble = self.admin_controller.capture_fingerprint()
            except Exception as e:
                texto_instruccion.set("Huella registrada con otro usuario o error. Use otra huella.")
                ventana.update()
                time.sleep(1.5)
                ventana.destroy()
                return None

            try:
                texto_instruccion.set("Leyendo huella...")
                ventana.update()
                time.sleep(1.0)

                texto_instruccion.set("Huella capturada, procesando...")
                ventana.update()
                time.sleep(1.0)

                if not isAble:
                    # Huella previamente registrada
                    messagebox.showinfo("Información", "Huella previamente registrada, utilice otra")
                    ventana.destroy()
                    return None

                texto_instruccion.set("Coloque su dedo nuevamente para finalizar registro...")
                ventana.update()
                # match_and_store_fp debería devolver el id de la huella almacenada
                fingerprintId = self.admin_controller.match_and_store_fp()
            except Exception as e:
                texto_instruccion.set("Error al registrar huella, intente nuevamente")
                ventana.update()
                time.sleep(1.5)
                # Reintentar: continuar el while
                continue

            break

        texto_instruccion.set("Usuario registrado exitosamente")
        ventana.destroy()
        print(f'huella registrada #{fingerprintId}')
        return fingerprintId

    def agregar_usuario(self):
        self.mostrar_ventana_emergente()
    
    def eliminar_usuario(self):
        selected_index = self.listbox.curselection()
        if selected_index:
            index = selected_index[0]
            user_id = self.usuarios[index]["id"]
            print(self.usuarios[index])
            answer = messagebox.askyesno("PRECAUCIÓN", f"Va a eliminar al usuario {self.usuarios[index]['nombre']} ¿está seguro?")
            if not answer:
                return
            else:
                second_answer = messagebox.askyesno("¿ESTÁS SEGURO?", "El eliminado de un usuario es una acción sin retorno, ¿está seguro de continuar?")
                if not second_answer:
                    return
            self.admin_controller.delete_user_logically(user_id)
            self.usuarios = self.admin_controller.get_all_users()
            self.actualizar_lista()
            self.validar_estado_botones()


    def editar_usuario(self):
        selected_index = self.listbox.curselection()
        if selected_index:
            index = selected_index[0]
            nombre_actual = self.usuarios[index]["nombre"]
            rol_actual = self.usuarios[index]["rol"]
            username_actual = self.usuarios[index]["username"]
            self.show_edit_dialog(index, nombre_actual, rol_actual, username_actual)


    def show_edit_dialog(self, index, nombre_actual, rol_actual, username_actual):
        # Limpiamos el contenido actual
        for widget in self.frame_content.winfo_children():
            widget.destroy()

        tk.Label(self.frame_content, text="Editar Usuario", font=("Arial", 24, "bold"), bg="#fcfcfc").pack(pady=10)

        form_frame = tk.Frame(self.frame_content, bg="#fcfcfc")
        form_frame.pack(pady=20)

        # Separar nombre en nombre y apellido (si quieres mantener un único campo puedes adaptarlo)
        partes = nombre_actual.split(" ", 1)
        first_name_default = partes[0]
        last_name_default = partes[1] if len(partes) > 1 else ""

        # Campos de edición: Nombre (first), Apellido (last), Rol, Usuario, Nueva Clave
        tk.Label(form_frame, text="Nombre:", font=("Arial", 16), bg="#fcfcfc").grid(row=0, column=0, sticky="e", padx=10, pady=5)
        entry_first_name = tk.Entry(form_frame, font=("Arial", 16))
        entry_first_name.insert(0, first_name_default)
        entry_first_name.grid(row=0, column=1, padx=10, pady=5)

        tk.Label(form_frame, text="Apellido:", font=("Arial", 16), bg="#fcfcfc").grid(row=1, column=0, sticky="e", padx=10, pady=5)
        entry_last_name = tk.Entry(form_frame, font=("Arial", 16))
        entry_last_name.insert(0, last_name_default)
        entry_last_name.grid(row=1, column=1, padx=10, pady=5)

                # Rol
        tk.Label(form_frame, text="Rol", font=("Arial", 16), bg="white").grid(row=2, column=0, sticky='e', padx=10, pady=5)
        rol_var = tk.StringVar(form_frame)
        rol_var.set("Seleccionar rol")

        opciones_rol = ["Administrador", "Operario"]
        opciones_rol_enum = {
            "Administrador": UserRole.ADMIN,
            "Operario": UserRole.OPERATIVE
        }

        menu_rol = tk.OptionMenu(form_frame, rol_var, *opciones_rol)
        menu_rol.config(font=("Arial", 16))
        menu_rol.grid(row=2, column=1, padx=10, pady=5)

        tk.Label(form_frame, text="Usuario:", font=("Arial", 16), bg="#fcfcfc").grid(row=3, column=0, sticky="e", padx=10, pady=5)
        entry_username = tk.Entry(form_frame, font=("Arial", 16))
        entry_username.insert(0, username_actual)
        entry_username.grid(row=3, column=1, padx=10, pady=5)

        tk.Label(form_frame, text="Nueva Clave (opcional):", font=("Arial", 16), bg="#fcfcfc").grid(row=4, column=0, sticky="e", padx=10, pady=5)
        entry_password = tk.Entry(form_frame, font=("Arial", 16), show="*")
        entry_password.grid(row=4, column=1, padx=10, pady=5)

        # Botones de acción
        button_frame = tk.Frame(self.frame_content, bg="#fcfcfc")
        button_frame.pack(pady=20)

        def guardar():
            first_name = entry_first_name.get().strip()
            last_name = entry_last_name.get().strip()
            new_rol = opciones_rol_enum[rol_var.get()]
            new_username = entry_username.get().strip()
            new_password = entry_password.get().strip()

            if not first_name or not new_rol or not new_username:
                tk.messagebox.showwarning("Campos vacíos", "Nombre, rol y usuario son obligatorios.")
                return

            user_id = self.usuarios[index]["id"]

            # Llamamos a AdminController.update_user con la firma correcta:
            # update_user(user_id, first_name, last_name, role, username=None, password=None)
            # Convertimos rol si el usuario escribe "Administrador"/"Operario" a los enums si quieres:
            rol_param = new_rol

            # Llamada final (password en texto plano; AdminController se encargará de hashearlo)
            self.admin_controller.update_user(user_id, first_name, last_name, rol_param, new_username, new_password if new_password else None)

            # Refrescar lista y volver
            self.usuarios = self.admin_controller.get_all_users()
            self.volver_a_lista()

        # Botón Guardar
        BotonRedondeado(
            parent=button_frame,
            width=250,
            height=70,
            radio=30,
            texto="Guardar Cambios",
            color_fondo="#4CAF50",
            color_hover="#388E3C",
            color_texto="white",
            font=("Times", 24, "bold"),
            comando=guardar
        ).grid(row=0, column=0, padx=10)

        # Botón Volver
        BotonRedondeado(
            parent=button_frame,
            width=250,
            height=70,
            radio=30,
            texto="Volver",
            color_fondo="#9E9E9E",
            color_hover="#757575",
            color_texto="white",
            font=("Times", 24, "bold"),
            comando=self.volver_a_lista
        ).grid(row=0, column=1, padx=10)


    def volver_a_lista(self):
        """Restaura la vista principal (lista de usuarios) sin reiniciar toda la clase."""
        # Limpiar el contenido actual
        for widget in self.frame_content.winfo_children():
            widget.destroy()

        # Volver a crear la barra de botones + lista (misma estructura que en __init__)
        button_frame = tk.Frame(self.frame_content, bg='#fcfcfc')
        button_frame.pack(pady=20)

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

        # Volver a crear la lista de usuarios
        list_frame = tk.Frame(self.frame_content, bg='#fcfcfc')
        list_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)

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

        # Recargar usuarios
        self.usuarios = self.admin_controller.get_all_users()
        self.actualizar_lista()
        self.validar_estado_botones()

        self.listbox.bind("<Button-1>", self.toggle_seleccion)

    def on_show(self):
        for widget in self.header_frame.winfo_children():
            if isinstance(widget, tk.Label):
                widget.config(text=SessionState.get_user().getFullName())
        self.volver_a_lista()
        
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