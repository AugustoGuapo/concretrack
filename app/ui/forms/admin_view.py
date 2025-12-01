# app/ui/forms/admin_view.py

import tkinter as tk
import tkinter.messagebox as messagebox  # ✅ Corregido: message**box**, no message**obby**
from app.ui.controllers.admin_controller import AdminController
from app.ui.forms.base_view import BaseView
from app.models.user_role import UserRole
from app.state.session_state import SessionState
import time

# 🔽 Importamos el teclado virtual
from app.ui.components.virtual_keyboard import VirtualKeyboard


# ----------------- Estilos globales -----------------
ESTILOS = {
    "bg_main": "#F8F9FA",
    "bg_header": "#E3F2FD",
    "fg_header_text": "#0D47A1",
    "btn_add_bg": "#4CAF50",
    "btn_add_hover": "#388E3C",
    "btn_edit_bg": "#FF9800",
    "btn_edit_hover": "#F57C00",
    "btn_del_bg": "#F44336",
    "btn_del_hover": "#D32F2F",
    "list_bg": "white",
    "list_fg": "#333333",
    "list_select_bg": "#2196F3",
    "list_select_fg": "white",
    "font_title": ("Segoe UI", 32, "bold"),
    "font_header": ("Segoe UI", 28, "bold"),
    "font_button": ("Segoe UI", 36, "bold"),
    "font_list": ("Segoe UI", 30),
    "font_form": ("Segoe UI", 28),
}


class AdminView(BaseView):
    def __init__(self, parent, view_controller):
        super().__init__(parent)
        self.admin_controller = AdminController()
        self.view_controller = view_controller
        self.role_dict = {
            "admin": "Administrador",
            "operative": "Operario"
        }
        self.row_widgets = []
        self.virtual_keyboard = None  # ←←← Teclado virtual (solo en formularios)

        self.config(bg=ESTILOS["bg_main"])
        self.create_header()

        self.frame_content = tk.Frame(self, bg=ESTILOS["bg_main"])
        self.frame_content.pack(side="top", expand=True, fill=tk.BOTH, pady=(10, 0))

        self.create_buttons()
        self.create_user_list()

    def create_header(self):
        self.header_frame = tk.Frame(self, bg=ESTILOS["bg_header"], height=80)
        self.header_frame.pack(fill=tk.X, padx=20, pady=15)
        self.header_frame.pack_propagate(False)

        try:
            username = SessionState.get_user().getFullName()
        except Exception:
            username = "Invitado"

        user_label = tk.Label(
            self.header_frame,
            text=username,
            bg=ESTILOS["bg_header"],
            fg=ESTILOS["fg_header_text"],
            font=ESTILOS["font_header"]
        )
        user_label.pack(side=tk.LEFT, padx=20)

        close_button = tk.Button(
            self.header_frame,
            text="Cerrar Sesión  ➤",
            bg="#FF5252",
            fg="black",
            font=("Segoe UI", 28, "bold"),
            bd=0,
            activebackground="#FF1744",
            activeforeground="black",
            width=18,
            height=2,
            relief="flat",
            command=self.logout
        )
        close_button.pack(side=tk.RIGHT, padx=20)

    def create_buttons(self):
        button_frame = tk.Frame(self.frame_content, bg=ESTILOS["bg_main"])
        button_frame.pack(pady=30)

        self.btn_agregar = BotonRedondeado(
            parent=button_frame,
            width=480,
            height=100,
            radio=50,
            texto="Agregar",
            color_fondo=ESTILOS["btn_add_bg"],
            color_hover=ESTILOS["btn_add_hover"],
            color_texto="white",
            font=ESTILOS["font_button"],
            comando=self.agregar_usuario
        )
        self.btn_agregar.grid(row=0, column=0, padx=25)

        self.btn_eliminar = BotonRedondeado(
            parent=button_frame,
            width=480,
            height=100,
            radio=50,
            texto="Eliminar",
            color_fondo=ESTILOS["btn_del_bg"],
            color_hover=ESTILOS["btn_del_hover"],
            color_texto="white",
            font=ESTILOS["font_button"],
            comando=self.eliminar_usuario
        )
        self.btn_eliminar.grid(row=0, column=1, padx=25)

        self.btn_editar = BotonRedondeado(
            parent=button_frame,
            width=480,
            height=100,
            radio=50,
            texto="Editar",
            color_fondo=ESTILOS["btn_edit_bg"],
            color_hover=ESTILOS["btn_edit_hover"],
            color_texto="white",
            font=ESTILOS["font_button"],
            comando=self.editar_usuario
        )
        self.btn_editar.grid(row=0, column=2, padx=25)

    def create_user_list(self):
        list_frame = tk.Frame(self.frame_content, bg=ESTILOS["bg_main"])
        list_frame.pack(fill="x", padx=40, pady=(20, 30))

        separator = tk.Frame(list_frame, bg="#DDDDDD", height=2)
        separator.pack(fill="x", pady=(0, 10))

        self.rows_container = tk.Frame(list_frame, bg=ESTILOS["bg_main"])
        self.rows_container.pack(fill="x")

        self.usuarios = self.admin_controller.get_all_users()
        self.actualizar_lista()
        self.validar_estado_botones()

    def actualizar_lista(self):
        for widget in self.rows_container.winfo_children():
            widget.destroy()
        self.row_widgets.clear()

        if not self.usuarios:
            tk.Label(
                self.rows_container,
                text="No hay usuarios registrados.",
                font=("Segoe UI", 24),
                bg=ESTILOS["bg_main"],
                fg="#999999"
            ).pack(pady=50)
            return

        nombres = [u.get('nombre', '') for u in self.usuarios]
        roles = [self.role_dict.get(u.get('rol', ''), "Desconocido") for u in self.usuarios]
        usuariosnames = [u.get('username', '') for u in self.usuarios]

        w1 = max(20, max([len(s) for s in nombres], default=20))
        w2 = max(15, max([len(s) for s in roles], default=15))
        w3 = max(15, max([len(s) for s in usuariosnames], default=15))

        for i, (usuario, rol_texto) in enumerate(zip(self.usuarios, roles)):
            nombre = usuario.get('nombre', '')
            rol = rol_texto
            username = usuario.get('username', '')

            row_frame = tk.Frame(
                self.rows_container,
                bg=ESTILOS["bg_main"],
                height=80
            )
            row_frame.pack(fill="x", pady=5)
            row_frame.pack_propagate(False)

            lbl_nombre = tk.Label(
                row_frame,
                text=nombre.ljust(w1),
                font=ESTILOS["font_list"],
                bg=ESTILOS["bg_main"],
                fg=ESTILOS["list_fg"],
                anchor="w"
            )
            lbl_nombre.place(x=0, rely=0.5, anchor="w")

            lbl_rol = tk.Label(
                row_frame,
                text=rol.ljust(w2),
                font=ESTILOS["font_list"],
                bg=ESTILOS["bg_main"],
                fg=ESTILOS["list_fg"],
                anchor="center"
            )
            lbl_rol.place(relx=0.5, rely=0.5, anchor="center")

            lbl_username = tk.Label(
                row_frame,
                text=username.ljust(w3),
                font=ESTILOS["font_list"],
                bg=ESTILOS["bg_main"],
                fg=ESTILOS["list_fg"],
                anchor="e"
            )
            lbl_username.place(relx=1.0, rely=0.5, anchor="e")

            row_data = {
                "frame": row_frame,
                "nombre": lbl_nombre,
                "rol": lbl_rol,
                "username": lbl_username,
                "index": i
            }
            self.row_widgets.append(row_data)

            def make_handler(idx):
                return lambda e: self.select_row(idx)
            row_frame.bind("<Button-1>", make_handler(i))

    def select_row(self, index):
        if hasattr(self, 'selected_index') and self.selected_index == index:
            for data in self.row_widgets:
                data["frame"].config(bg=ESTILOS["bg_main"])
                data["nombre"].config(bg=ESTILOS["bg_main"], fg=ESTILOS["list_fg"])
                data["rol"].config(bg=ESTILOS["bg_main"], fg=ESTILOS["list_fg"])
                data["username"].config(bg=ESTILOS["bg_main"], fg=ESTILOS["list_fg"])
            delattr(self, 'selected_index')
            self.btn_editar.config(state=tk.DISABLED)
            self.btn_eliminar.config(state=tk.DISABLED)
        else:
            for data in self.row_widgets:
                data["frame"].config(bg=ESTILOS["bg_main"])
                data["nombre"].config(bg=ESTILOS["bg_main"], fg=ESTILOS["list_fg"])
                data["rol"].config(bg=ESTILOS["bg_main"], fg=ESTILOS["list_fg"])
                data["username"].config(bg=ESTILOS["bg_main"], fg=ESTILOS["list_fg"])

            selected = self.row_widgets[index]
            selected["frame"].config(bg=ESTILOS["list_select_bg"])
            selected["nombre"].config(bg=ESTILOS["list_select_bg"], fg=ESTILOS["list_select_fg"])
            selected["rol"].config(bg=ESTILOS["list_select_bg"], fg=ESTILOS["list_select_fg"])
            selected["username"].config(bg=ESTILOS["list_select_bg"], fg=ESTILOS["list_select_fg"])

            self.selected_index = index
            self.btn_editar.config(state=tk.NORMAL)
            self.btn_eliminar.config(state=tk.NORMAL)

    def validar_estado_botones(self):
        estado_base = tk.NORMAL if self.usuarios else tk.DISABLED
        self.btn_eliminar.config(state=estado_base)
        self.btn_editar.config(state=estado_base)
        if not hasattr(self, 'selected_index'):
            self.btn_editar.config(state=tk.DISABLED)
            self.btn_eliminar.config(state=tk.DISABLED)

    def logout(self):
        SessionState.clear_user()
        if hasattr(self.view_controller, "show_frame"):
            from app.ui.forms.login import App as Login
            if "Login" not in self.view_controller.frame_classes:
                self.view_controller.frame_classes["Login"] = Login
            self.view_controller.show_frame("Login")
            login_frame = self.view_controller.frames.get("Login")
            if login_frame and hasattr(login_frame, "clear_fields"):
                login_frame.clear_fields()

    def agregar_usuario(self):
        self.mostrar_ventana_emergente()

    def eliminar_usuario(self):
        if not hasattr(self, 'selected_index'):
            return
        index = self.selected_index
        user = self.usuarios[index]
        if messagebox.askyesno("Confirmar", f"¿Eliminar a {user['nombre']}?") and \
           messagebox.askyesno("¡Atención!", "Esta acción es irreversible. ¿Continuar?"):
            self.admin_controller.delete_user_logically(user["id"])
            self.usuarios = self.admin_controller.get_all_users()
            self.actualizar_lista()
            self.validar_estado_botones()
            if hasattr(self, 'selected_index'):
                delattr(self, 'selected_index')

    def editar_usuario(self):
        if not hasattr(self, 'selected_index'):
            return
        index = self.selected_index
        user = self.usuarios[index]
        self.show_edit_dialog(index, user["nombre"], user["rol"], user["username"])

    def volver_a_lista(self):
        if self.virtual_keyboard:
            self.virtual_keyboard.hide()

        for widget in self.frame_content.winfo_children():
            widget.destroy()
        self.create_buttons()
        self.create_user_list()

    def on_show(self):
        for w in self.header_frame.winfo_children():
            if isinstance(w, tk.Label):
                try:
                    w.config(text=SessionState.get_user().getFullName())
                except:
                    w.config(text="Invitado")
        self.volver_a_lista()

    # --- Formulario: Registrar ---
    def mostrar_ventana_emergente(self):
        for widget in self.frame_content.winfo_children():
            widget.destroy()

        form_frame = tk.Frame(self.frame_content, bg="white")
        form_frame.pack(fill="both", expand=True, padx=40, pady=30)

        fuente = ESTILOS["font_form"]
        ancho_entry = 35
        pady_campo = 25

        tk.Label(form_frame, text="Registrar nuevo usuario", font=ESTILOS["font_title"], bg="white").pack(pady=30)

        tk.Label(form_frame, text="Nombre", font=fuente, bg="white").pack(pady=(pady_campo, 5))
        entry_nombre = tk.Entry(form_frame, font=fuente, width=ancho_entry)
        entry_nombre.pack()

        tk.Label(form_frame, text="Apellido", font=fuente, bg="white").pack(pady=(pady_campo, 5))
        entry_apellido = tk.Entry(form_frame, font=fuente, width=ancho_entry)
        entry_apellido.pack()

        tk.Label(form_frame, text="Contraseña", font=fuente, bg="white").pack(pady=(pady_campo, 5))
        entry_contrasena = tk.Entry(form_frame, show="*", font=fuente, width=ancho_entry)
        entry_contrasena.pack()

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

        def guardar_usuario():
            nombre = entry_nombre.get().strip()
            apellido = entry_apellido.get().strip()
            contrasena = entry_contrasena.get().strip()
            rol_texto = rol_var.get().strip()
            rol = opciones_rol_enum.get(rol_texto, None)

            if not nombre or not apellido or not contrasena or rol is None:
                messagebox.showerror("Error", "Completa todos los campos correctamente.")
                return

            fingerprint_id = self.mostrar_ventana_biometrica()
            if fingerprint_id is None or (isinstance(fingerprint_id, int) and fingerprint_id < 0):
                messagebox.showerror("Error", "No se pudo obtener la huella. Registro cancelado.")
                return

            try:
                self.admin_controller.create_user(
                    firstName=nombre,
                    lastName=apellido,
                    password=contrasena,
                    role=rol,
                    fingerprintId=fingerprint_id
                )
                messagebox.showinfo("Éxito", f"Usuario registrado correctamente (huella #{fingerprint_id})")
                self.volver_a_lista()
            except Exception as e:
                messagebox.showerror("Error", f"No se pudo registrar el usuario:\n{e}")

        # Botones
        button_frame = tk.Frame(form_frame, bg="white")
        button_frame.pack(pady=30)

        tk.Button(
            button_frame,
            text="Guardar Usuario",
            font=("Segoe UI", 30, "bold"),
            bg=ESTILOS["btn_add_bg"],
            fg="white",
            height=2,
            width=25,
            relief="flat",
            command=guardar_usuario
        ).pack(pady=10)

        tk.Button(
            button_frame,
            text="Volver",
            font=("Segoe UI", 26),
            bg=ESTILOS["btn_del_bg"],
            fg="white",
            height=2,
            width=25,
            relief="flat",
            command=self.volver_a_lista
        ).pack(pady=10)

        # ←←← Teclado virtual
        if self.virtual_keyboard is None:
            self.virtual_keyboard = VirtualKeyboard(self.frame_content)
        self.virtual_keyboard.show()

        # ←←← Vinculación SEGURA a los campos
        if self.virtual_keyboard:
            for entry in [entry_nombre, entry_apellido, entry_contrasena]:
                entry.bind("<FocusIn>", lambda e, ent=entry: self.virtual_keyboard and self.virtual_keyboard.set_active_entry(ent))

    def mostrar_ventana_biometrica(self) -> int:
        ventana = tk.Toplevel(self)
        ventana.title("Captura de huella")
        ventana.transient(self.winfo_toplevel())
        ventana.grab_set()
        ventana.geometry("800x300")

        texto_instruccion = tk.StringVar(ventana, value="Por favor, coloque su dedo en el lector biométrico")
        label_instr = tk.Label(ventana, textvariable=texto_instruccion, font=("Segoe UI", 24))
        label_instr.pack(pady=30, padx=30)

        def cancelar():
            ventana.destroy()

        btn_cancel = tk.Button(ventana, text="Cancelar", font=("Segoe UI", 20), command=cancelar)
        btn_cancel.pack(pady=20)

        ventana.update()
        fingerprintId = None

        while True:
            try:
                texto_instruccion.set("Esperando huella...")
                ventana.update()
                isAble = self.admin_controller.capture_fingerprint()
            except Exception as e:
                texto_instruccion.set("Huella registrada con otro usuario o error. Use otra huella.")
                print(e)
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
                    messagebox.showinfo("Información", "Huella previamente registrada, utilice otra")
                    ventana.destroy()
                    return None

                texto_instruccion.set("Coloque su dedo nuevamente para finalizar registro...")
                ventana.update()
                fingerprintId = self.admin_controller.match_and_store_fp()
            except Exception as e:
                texto_instruccion.set("Error al registrar huella, intente nuevamente")
                ventana.update()
                time.sleep(1.5)
                continue

            break

        texto_instruccion.set("Usuario registrado exitosamente")
        ventana.destroy()
        print(f'huella registrada #{fingerprintId}')
        return fingerprintId

    # --- Formulario: Editar ---
    def show_edit_dialog(self, index, nombre_actual, rol_actual, username_actual):
        for widget in self.frame_content.winfo_children():
            widget.destroy()

        tk.Label(self.frame_content, text="Editar Usuario", font=ESTILOS["font_title"], bg=ESTILOS["bg_main"]).pack(pady=20)

        form_frame = tk.Frame(self.frame_content, bg=ESTILOS["bg_main"])
        form_frame.pack(pady=30)

        partes = nombre_actual.split(" ", 1)
        first_name_default = partes[0]
        last_name_default = partes[1] if len(partes) > 1 else ""

        tk.Label(form_frame, text="Nombre:", font=ESTILOS["font_form"], bg=ESTILOS["bg_main"]).grid(row=0, column=0, sticky="e", padx=20, pady=10)
        entry_first_name = tk.Entry(form_frame, font=ESTILOS["font_form"])
        entry_first_name.insert(0, first_name_default)
        entry_first_name.grid(row=0, column=1, padx=20, pady=10)

        tk.Label(form_frame, text="Apellido:", font=ESTILOS["font_form"], bg=ESTILOS["bg_main"]).grid(row=1, column=0, sticky="e", padx=20, pady=10)
        entry_last_name = tk.Entry(form_frame, font=ESTILOS["font_form"])
        entry_last_name.insert(0, last_name_default)
        entry_last_name.grid(row=1, column=1, padx=20, pady=10)

        tk.Label(form_frame, text="Rol", font=ESTILOS["font_form"], bg=ESTILOS["bg_main"]).grid(row=2, column=0, sticky='e', padx=20, pady=10)
        rol_var = tk.StringVar(form_frame)
        rol_var.set("Seleccionar rol")

        opciones_rol = ["Administrador", "Operario"]
        opciones_rol_enum = {
            "Administrador": UserRole.ADMIN,
            "Operario": UserRole.OPERATIVE
        }

        menu_rol = tk.OptionMenu(form_frame, rol_var, *opciones_rol)
        menu_rol.config(font=ESTILOS["font_form"])
        menu_rol.grid(row=2, column=1, padx=20, pady=10)

        tk.Label(form_frame, text="Usuario:", font=ESTILOS["font_form"], bg=ESTILOS["bg_main"]).grid(row=3, column=0, sticky="e", padx=20, pady=10)
        entry_username = tk.Entry(form_frame, font=ESTILOS["font_form"])
        entry_username.insert(0, username_actual)
        entry_username.grid(row=3, column=1, padx=20, pady=10)

        tk.Label(form_frame, text="Nueva Clave (opcional):", font=ESTILOS["font_form"], bg=ESTILOS["bg_main"]).grid(row=4, column=0, sticky="e", padx=20, pady=10)
        entry_password = tk.Entry(form_frame, font=ESTILOS["font_form"], show="*")
        entry_password.grid(row=4, column=1, padx=20, pady=10)

        button_frame = tk.Frame(self.frame_content, bg=ESTILOS["bg_main"])
        button_frame.pack(pady=30)

        def guardar():
            first_name = entry_first_name.get().strip()
            last_name = entry_last_name.get().strip()
            new_rol = opciones_rol_enum[rol_var.get()]
            new_username = entry_username.get().strip()
            new_password = entry_password.get().strip()

            if not first_name or not new_rol or not new_username:
                messagebox.showwarning("Campos vacíos", "Nombre, rol y usuario son obligatorios.")
                return

            user_id = self.usuarios[index]["id"]
            self.admin_controller.update_user(user_id, first_name, last_name, new_rol, new_username, new_password if new_password else None)

            self.volver_a_lista()

        BotonRedondeado(
            parent=button_frame,
            width=300,
            height=90,
            radio=40,
            texto="Guardar Cambios",
            color_fondo=ESTILOS["btn_add_bg"],
            color_hover=ESTILOS["btn_add_hover"],
            color_texto="white",
            font=("Segoe UI", 32, "bold"),
            comando=guardar
        ).grid(row=0, column=0, padx=20)

        BotonRedondeado(
            parent=button_frame,
            width=300,
            height=90,
            radio=40,
            texto="Volver",
            color_fondo="#9E9E9E",
            color_hover="#757575",
            color_texto="white",
            font=("Segoe UI", 32, "bold"),
            comando=self.volver_a_lista
        ).grid(row=0, column=1, padx=20)

        # ←←← Teclado virtual en edición
        if self.virtual_keyboard is None:
            self.virtual_keyboard = VirtualKeyboard(self.frame_content)
        self.virtual_keyboard.show()

        # ←←← Vinculación SEGURA a los campos
        if self.virtual_keyboard:
            for entry in [entry_first_name, entry_last_name, entry_username, entry_password]:
                entry.bind("<FocusIn>", lambda e, ent=entry: self.virtual_keyboard and self.virtual_keyboard.set_active_entry(ent))


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