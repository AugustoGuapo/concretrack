import tkinter as tk

elements = [
    {"name": "Trabajos 1"},
    {"name": "Trabajos 2"},
    {"name": "Trabajos 3"},
    {"name": "Trabajos 4"},
    {"name": "Trabajos 5"},
    {"name": "Trabajos 6"},
    {"name": "Trabajos 7"},
    {"name": "Trabajos 8"},
    {"name": "Trabajos 9"},
    {"name": "Trabajos 10"},
]

class EvaluadorUI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Evaluador")
        self.root.attributes('-fullscreen', True)
        self.root.config(bg="#fcfcfc")

        self.selected_index = None

        main_frame = tk.Frame(self.root, bg="#fcfcfc")
        main_frame.pack(fill=tk.BOTH, expand=True)

        list_frame = tk.Frame(main_frame, bg="#fcfcfc")
        list_frame.pack(fill=tk.BOTH, expand=True, padx=40, pady=80)

        self.scrollbar = tk.Scrollbar(list_frame)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.listbox = tk.Listbox(
            list_frame,
            font=("Arial", 40),
            yscrollcommand=self.scrollbar.set,
            selectmode=tk.SINGLE,
            activestyle='none'
        )
        self.listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.scrollbar.config(command=self.listbox.yview)

        self.listbox.bind('<<ListboxSelect>>', self.on_select)

        bottom_frame = tk.Frame(main_frame, bg="#fcfcfc")
        bottom_frame.pack(fill=tk.X, side=tk.BOTTOM, padx=40, pady=40)

        btn_logout = tk.Button(
            bottom_frame, text="Cerrar sesión", command=self.cerrar_sesion,
            font=("Arial", 14), bg="red", fg="black", padx=20, pady=10
        )
        btn_logout.pack(side=tk.LEFT)

        self.btn_evaluar = tk.Button(
            bottom_frame, text="Evaluar", command=self.evaluar,
            font=("Arial", 14), bg="green", fg="black", padx=20, pady=10,
            state=tk.DISABLED
        )
        self.btn_evaluar.pack(side=tk.RIGHT)

        # Simular carga de elementos después de 5 segundos (5000 ms)
        self.root.after(5000, self.cargar_elementos)

        self.root.mainloop()

    def cargar_elementos(self):
        self.listbox.delete(0, tk.END)
        padding = "    "
        for item in elements:
            self.listbox.insert(tk.END, padding + item["name"])

    def on_select(self, event):
        selection = self.listbox.curselection()
        if selection:
            if self.selected_index == selection[0]:
                self.listbox.selection_clear(self.selected_index)
                self.selected_index = None
                self.btn_evaluar.config(state=tk.DISABLED)
            else:
                self.selected_index = selection[0]
                self.btn_evaluar.config(state=tk.NORMAL)
        else:
            self.selected_index = None
            self.btn_evaluar.config(state=tk.DISABLED)

    def cerrar_sesion(self):
        print("Sesión cerrada")
        self.root.destroy()

    def evaluar(self):
        if self.selected_index is not None:
            item = self.listbox.get(self.selected_index).strip()
            print(f"Evaluando: {item}")
