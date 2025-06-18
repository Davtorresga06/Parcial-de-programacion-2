# --------- IMPORTACIÓN DE LIBRERÍAS ---------
import tkinter as tk  # Librería para interfaces gráficas
from tkinter import messagebox, ttk, simpledialog  # Widgets y diálogos
import firebase_admin  # Librería para Firebase
from firebase_admin import credentials, db  # Manejo de credenciales y base de datos
import uuid  # Generación de identificadores únicos

# --------- CONEXIÓN A FIREBASE ---------
cred = credentials.Certificate("C:/Users/ESTUDIANTES/Desktop/parcial-de-programacion-2-firebase-adminsdk-fbsvc-bec9c9e7fc.json")  # Ruta al archivo de credenciales
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://parcial-de-programacion-2-default-rtdb.firebaseio.com/'  # URL de la base de datos
})

# --------- CATEGORÍAS CON EMOJIS ---------
CATEGORIAS = [
    "🧪 Ciencia",
    "🎨 Arte",
    "📖 Juvenil",
    "📜 Historia",
    "💻 Tecnología"
]

# --------- CLASE PRINCIPAL DE LA APLICACIÓN ---------
class BibliotecaApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Gestor de Biblioteca con Firebase")  # Título de la ventana

        # --------- LOGIN PARA INGRESAR ---------
        self.usuario = simpledialog.askstring("Inicio de sesión", "Ingresa tu correo:")  # Solicita el correo del usuario
        if not self.usuario:
            messagebox.showerror("Error", "Debes ingresar tu correo para continuar.")
            root.destroy()
            return

        self.crear_widgets()  # Llama a la función para crear los widgets
        self.cargar_libros_desde_firebase()  # Carga los libros ya registrados

    def crear_widgets(self):
        # --------- FRAME PARA REGISTRAR LIBROS ---------
        frame_registro = tk.LabelFrame(self.root, text="Registrar Libro")  # Marco para registrar libros
        frame_registro.grid(row=0, column=0, padx=10, pady=5)

        tk.Label(frame_registro, text="Título:").grid(row=0, column=0)  # Etiqueta de título
        self.entry_titulo = tk.Entry(frame_registro)  # Entrada de texto para el título
        self.entry_titulo.grid(row=0, column=1)

        tk.Label(frame_registro, text="Autor:").grid(row=1, column=0)  # Etiqueta de autor
        self.entry_autor = tk.Entry(frame_registro)  # Entrada de texto para el autor
        self.entry_autor.grid(row=1, column=1)

        tk.Label(frame_registro, text="Categoría:").grid(row=2, column=0)  # Etiqueta de categoría
        self.combo_categoria = ttk.Combobox(frame_registro, values=CATEGORIAS, state="readonly")  # Menú desplegable
        self.combo_categoria.grid(row=2, column=1)
        self.combo_categoria.current(0)  # Selecciona la primera categoría por defecto

        tk.Button(frame_registro, text="Agregar Libro", command=self.registrar_libro).grid(row=3, column=0, columnspan=2, pady=5)  # Botón para agregar libro

        # --------- FRAME DE BÚSQUEDA DE LIBROS ---------
        frame_busqueda = tk.LabelFrame(self.root, text="Buscar Libro")  # Marco de búsqueda
        frame_busqueda.grid(row=1, column=0, padx=10, pady=5)

        tk.Label(frame_busqueda, text="Buscar por título o autor:").grid(row=0, column=0)  # Etiqueta de búsqueda
        self.entry_busqueda = tk.Entry(frame_busqueda)  # Entrada de búsqueda
        self.entry_busqueda.grid(row=0, column=1)
        tk.Button(frame_busqueda, text="Buscar", command=self.buscar_libros).grid(row=0, column=2, padx=5)  # Botón buscar
        tk.Button(frame_busqueda, text="Mostrar Todos", command=self.cargar_libros_desde_firebase).grid(row=0, column=3, padx=5)  # Botón para mostrar todo

        # --------- TABLA PARA MOSTRAR LOS LIBROS ---------
        self.lista_libros = ttk.Treeview(self.root, columns=("Autor", "Categoría", "Disponible", "Prestado a"), show="headings")  # Tabla
        self.lista_libros.grid(row=2, column=0, padx=10, pady=10)
        for col in self.lista_libros["columns"]:
            self.lista_libros.heading(col, text=col)  # Encabezados de la tabla

        # --------- BOTONES DE ACCIÓN (PRESTADO / DEVUELTO) ---------
        frame_botones = tk.Frame(self.root)  # Marco para botones
        frame_botones.grid(row=3, column=0, pady=5)

        tk.Button(frame_botones, text="Marcar como Prestado", command=lambda: self.actualizar_estado(False)).pack(side="left", padx=5)  # Botón para prestar
        tk.Button(frame_botones, text="Marcar como Devuelto", command=lambda: self.actualizar_estado(True)).pack(side="left", padx=5)  # Botón para devolver

        # --------- ETIQUETA DEL USUARIO ACTUAL ---------
        self.etiqueta_usuario = tk.Label(self.root, text=f"Usuario actual: {self.usuario}", fg="blue")  # Muestra el correo
        self.etiqueta_usuario.grid(row=4, column=0, pady=5)

    def registrar_libro(self):
        titulo = self.entry_titulo.get().strip()  # Obtiene el título
        autor = self.entry_autor.get().strip()  # Obtiene el autor
        categoria = self.combo_categoria.get()  # Obtiene la categoría

        if not titulo or not autor:
            messagebox.showwarning("Campos vacíos", "Completa todos los campos.")  # Verifica campos vacíos
            return

        codigo = str(uuid.uuid4())  # Genera un código único para el libro

        nuevo_libro = {
            "titulo": titulo,
            "autor": autor,
            "categoria": categoria,
            "disponible": True
        }

        db.reference(f"libros/{codigo}").set(nuevo_libro)  # Guarda en Firebase con código único

        self.entry_titulo.delete(0, tk.END)  # Limpia campo título
        self.entry_autor.delete(0, tk.END)  # Limpia campo autor
        self.cargar_libros_desde_firebase()  # Recarga la lista

    def cargar_libros_desde_firebase(self):
        libros = db.reference("libros").get()  # Obtiene libros desde Firebase
        self.lista_libros.delete(*self.lista_libros.get_children())  # Limpia la tabla

        if libros:
            for codigo, datos in libros.items():
                disponible = "Sí" if datos["disponible"] else "No"  # Convierte a texto
                prestado_a = datos.get("prestado_a", "-")  # Si está prestado, muestra el correo
                self.lista_libros.insert("", tk.END, iid=codigo, values=(
                    datos["autor"], datos["categoria"], disponible, prestado_a
                ))  # Inserta en la tabla

    def actualizar_estado(self, disponible):
        seleccionado = self.lista_libros.focus()  # Verifica qué libro se seleccionó
        if not seleccionado:
            messagebox.showinfo("Selecciona un libro", "Debes seleccionar un libro primero.")
            return

        ref = db.reference(f"libros/{seleccionado}")  # Referencia al libro
        ref.update({"disponible": disponible})  # Cambia estado de disponibilidad

        if not disponible:
            ref.update({"prestado_a": self.usuario})  # Agrega correo si se presta
        else:
            ref.child("prestado_a").delete()  # Elimina si se devuelve

        self.cargar_libros_desde_firebase()  # Recarga la lista

    def buscar_libros(self):
        termino = self.entry_busqueda.get().strip().lower()  # Obtiene término de búsqueda
        if not termino:
            messagebox.showinfo("Buscar", "Ingresa un título o autor para buscar.")
            return

        libros = db.reference("libros").get()  # Trae todos los libros
        self.lista_libros.delete(*self.lista_libros.get_children())  # Limpia la tabla

        if libros:
            for codigo, datos in libros.items():
                if termino in datos["titulo"].lower() or termino in datos["autor"].lower():  # Compara con título o autor
                    disponible = "Sí" if datos["disponible"] else "No"
                    prestado_a = datos.get("prestado_a", "-")
                    self.lista_libros.insert("", tk.END, iid=codigo, values=(
                        datos["autor"], datos["categoria"], disponible, prestado_a
                    ))

# --------- EJECUCIÓN PRINCIPAL ---------
if __name__ == "__main__":
    root = tk.Tk()  # Crea ventana principal
    app = BibliotecaApp(root)  # Inicia la aplicación
    root.mainloop()  # Ejecuta el bucle principal de la interfaz