# Parcial-de-programacion-2
Widgets usados:
Tk() → Ventana principal
Label → Mostrar textos como Título, Autor, etc.
Entry → Campos para ingresar datos del libro
Button → Botones para acciones: Agregar, Eliminar, Buscar, Prestar, etc.
Treeview (de ttk) → Tabla donde se listan los libros con columnas: Título, Autor, Categoría, Estado, Prestado a
Scrollbar → Barra de desplazamiento para la tabla

Estructura de datos usada:
Lista de diccionarios: Cada libro se representa como un diccionario con claves como titulo, autor, categoria, disponible, prestado_a
Funciones clave:
agregar_libro() → Añade un libro nuevo a la lista y actualiza la tabla
eliminar_libro() → Quita el libro seleccionado
prestar_libro() y devolver_libro() → Cambian el estado de disponibilidad
buscar_libro() → Filtra libros por título
actualizar_tabla() → Refresca la tabla con los libros actuales

Justificación técnica:
Tkinter es una librería ligera y adecuada para aplicaciones pequeñas
Treeview permite mostrar datos estructurados en forma de tabla con múltiples columnas
Los diccionarios permiten almacenar varios atributos de cada libro de forma clara
La separación de funciones mejora la organización del código y facilita el mantenimiento

