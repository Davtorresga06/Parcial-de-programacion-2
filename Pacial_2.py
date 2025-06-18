import tkinter as tk
from tkinter import messagebox, ttk, simpledialog
import firebase_admin
from firebase_admin import credentials, db

# --------- CONEXIÓN A FIREBASE ---------
cred = credentials.Certificate("C:/Users/ESTUDIANTES/Desktop/parcial-de-programacion-2-firebase-adminsdk-fbsvc-bec9c9e7fc.json")
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://parcial-de-programacion-2-default-rtdb.firebaseio.com/'
})

# --------- CATEGORÍAS CON EMOJIS ---------
CATEGORIAS = [
    "🧪 Ciencia",
    "🎨 Arte",
    "📖 Juvenil",
    "📜 Historia",
    "💻 Tecnología"
]

class BibliotecaApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Gestor de Biblioteca con Firebase")

        # --------- LOGIN (simpledialog) ---------
        self.usuario = simpledialog.askstring("Inicio de sesión", "Ingresa tu correo:")
        if not self.usuario:
            messagebox.showerror("Error", "Debes ingresar tu correo para continuar.")
            root.destroy()
            return

        self.crear_widgets()
        self.cargar_libros_desde_firebase()

    def crear_widgets(self):
        # --------- FRAME DE REGISTRO (LabelFrame) ---------
        frame_registro = tk.LabelFrame(self.root, text="Registrar Libro")
        frame_registro.grid(row=0, column=0, padx=10, pady=5)

        # --------- ENTRADA DE TÍTULO (Label + Entry) ---------
        tk.Label(frame_registro, text="Título:").grid(row=0, column=0)
        self.entry_titulo = tk.Entry(frame_registro)  # Widget Entry
        self.entry_titulo.grid(row=0, column=1)

        # --------- ENTRADA DE AUTOR (Label + Entry) ---------
        tk.Label(frame_registro, text="Autor:").grid(row=1, column=0)
        self.entry_autor = tk.Entry(frame_registro)  # Widget Entry
        self.entry_autor.grid(row=1, column=1)

        # --------- CATEGORÍA (Label + Combobox) ---------
        tk.Label(frame_registro, text="Categoría:").grid(row=2, column=0)
        self.combo_categoria = ttk.Combobox(frame_registro, values=CATEGORIAS, state="readonly")  # Widget Combobox
        self.combo_categoria.grid(row=2, column=1)
        self.combo_categoria.current(0)

        # --------- BOTÓN DE REGISTRO (Button) ---------
        tk.Button(frame_registro, text="Agregar Libro", command=self.registrar_libro).grid(row=3, column=0, columnspan=2, pady=5)

        # --------- TABLA DE LIBROS (Treeview) ---------
        self.lista_libros = ttk.Treeview(self.root, columns=("Autor", "Categoría", "Disponible", "Prestado a"), show="headings")
        self.lista_libros.grid(row=1, column=0, padx=10, pady=10)
        for col in self.lista_libros["columns"]:
            self.lista_libros.heading(col, text=col)

        # --------- BOTONES DE ACCIÓN (Frame + Buttons) ---------
        frame_botones = tk.Frame(self.root)  # Widget Frame
        frame_botones.grid(row=2, column=0, pady=5)

        tk.Button(frame_botones, text="Marcar como Prestado", command=lambda: self.actualizar_estado(False)).pack(side="left", padx=5)
        tk.Button(frame_botones, text="Marcar como Devuelto", command=lambda: self.actualizar_estado(True)).pack(side="left", padx=5)

        # --------- ETIQUETA DEL USUARIO (Label) ---------
        self.etiqueta_usuario = tk.Label(self.root, text=f"Usuario actual: {self.usuario}", fg="blue")
        self.etiqueta_usuario.grid(row=3, column=0, pady=5)

    def registrar_libro(self):
        # Toma los datos de los campos
        titulo = self.entry_titulo.get().strip()
        autor = self.entry_autor.get().strip()
        categoria = self.combo_categoria.get()

        # Verifica que los campos estén llenos
        if not titulo or not autor:
            messagebox.showwarning("Campos vacíos", "Completa todos los campos.")
            return

        # Crea un diccionario con los datos del libro
        nuevo_libro = {
            "titulo": titulo,
            "autor": autor,
            "categoria": categoria,
            "disponible": True
        }

        # Guarda el libro en Firebase con el título como ID
        db.reference(f"libros/{titulo}").set(nuevo_libro)

        # Limpia los campos y recarga la lista
        self.entry_titulo.delete(0, tk.END)
        self.entry_autor.delete(0, tk.END)
        self.cargar_libros_desde_firebase()

    def cargar_libros_desde_firebase(self):
        # Trae los libros desde Firebase
        libros = db.reference("libros").get()
        self.lista_libros.delete(*self.lista_libros.get_children())

        # Muestra cada libro en la tabla
        if libros:
            for titulo, datos in libros.items():
                disponible = "Sí" if datos["disponible"] else "No"
                prestado_a = datos.get("prestado_a", "-")
                self.lista_libros.insert("", tk.END, iid=titulo, values=(
                    datos["autor"], datos["categoria"], disponible, prestado_a
                ))

    def actualizar_estado(self, disponible):
        # Verifica que se haya seleccionado un libro
        seleccionado = self.lista_libros.focus()
        if not seleccionado:
            messagebox.showinfo("Selecciona un libro", "Debes seleccionar un libro primero.")
            return

        # Actualiza el estado en Firebase
        ref = db.reference(f"libros/{seleccionado}")
        ref.update({"disponible": disponible})

        # Si está prestado, guarda el correo del usuario
        if not disponible:
            ref.update({"prestado_a": self.usuario})
        else:
            ref.child("prestado_a").delete()

        self.cargar_libros_desde_firebase()

# Incicio de la interfaz para registro de los libos
if __name__ == "__main__":
    root = tk.Tk()                 # Crea la ventana
    app = BibliotecaApp(root)      # Crea la app en esa ventana
    root.mainloop()                # Mantiene la ventana abierta

