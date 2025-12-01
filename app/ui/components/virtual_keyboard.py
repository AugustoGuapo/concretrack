# app/ui/components/virtual_keyboard.py
import tkinter as tk


class VirtualKeyboard:
    def __init__(self, parent):
        """
        Crea un teclado virtual que escribe en el campo que tenga foco.
        
        Args:
            parent (tk.Frame): Frame donde se empaquetará el teclado.
        """
        self.parent = parent
        self.is_shift = False
        self.active_entry = None  # Campo activo (usuario o contraseña)

        # Frame contenedor del teclado
        self.frame = tk.Frame(parent, bg='#fcfcfc', padx=10, pady=10)
        
        # Definir filas de teclas (sin espacio)
        self.keys = [
            ['q', 'w', 'e', 'r', 't', 'y', 'u', 'i', 'o', 'p'],
            ['a', 's', 'd', 'f', 'g', 'h', 'j', 'k', 'l', '"'],
            ['⇧', 'z', 'x', 'c', 'v', 'b', 'n', 'm', ',', '.'],
            ['1', '2', '3', '4', '5', '6', '7', '8', '9', '0'],
            ['-', '<-', '⌫']  # Sin espacio
        ]

        self.create_keyboard()

    def create_keyboard(self):
        for row_index, row in enumerate(self.keys):
            row_frame = tk.Frame(self.frame, bg='#fcfcfc')
            row_frame.pack(fill=tk.X, pady=2)

            for key in row:
                btn = self.create_key_button(row_frame, key)
                if key == '<-' or key == '⌫':
                    btn.pack(side=tk.LEFT, padx=2)
                else:
                    btn.pack(side=tk.LEFT, padx=2)

    def create_key_button(self, parent, key):
        # Estilos personalizados
        if key == '⇧':
            color_fondo, color_hover = "#FF9800", "#F57C00"
        elif key in ['<-', '⌫']:
            color_fondo, color_hover = "#F44336", "#D32F2F"
        else:
            color_fondo, color_hover = "#E0E0E0", "#BDBDBD"

        btn = tk.Button(
            parent,
            text=key,
            width=4,  # Ajustado para no ocupar mucho
            height=2,
            bg=color_fondo,
            fg="black",
            font=("Times", 16, "bold"),
            relief=tk.RAISED,
            bd=0,
            activebackground=color_hover,
            command=lambda k=key: self.on_key_press(k)
        )

        # Efectos hover
        btn.bind("<Enter>", lambda e, b=btn, c=color_hover: b.config(bg=c))
        btn.bind("<Leave>", lambda e, b=btn, c=color_fondo: b.config(bg=c))

        return btn

    def on_key_press(self, key):
        if not self.active_entry:
            return  # No hay campo activo

        if key == '⇧':
            self.toggle_shift()
        elif key == '<-':
            current = self.active_entry.get()
            if current:
                self.active_entry.delete(len(current) - 1)
        elif key == '⌫':
            self.active_entry.delete(0, tk.END)
        else:
            char = key.upper() if self.is_shift else key.lower()
            self.active_entry.insert(tk.END, char)
            if self.is_shift and key.isalpha():
                self.toggle_shift()  # Auto desactivar shift tras letra

    def toggle_shift(self):
        self.is_shift = not self.is_shift

    def set_active_entry(self, entry_widget):
        """Establece qué campo recibe la entrada."""
        self.active_entry = entry_widget

    def show(self):
        self.frame.pack(fill=tk.X, side=tk.BOTTOM, pady=10)

    def hide(self):
        self.frame.pack_forget()