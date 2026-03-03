"""
Patrón Factory - Fábrica de productos.

Este módulo contiene la clase ProductoFactory, que es el corazón del patrón.
La fábrica encapsula la lógica de creación de objetos, de modo que el código
cliente nunca necesita hacer "from producto import Libro" directamente.

Ventajas del patrón Factory:
    1. Desacoplamiento: El cliente no conoce las clases concretas.
    2. Punto único de creación: Si se agrega un nuevo tipo de producto,
       solo se modifica la fábrica.
    3. Valores por defecto: El método genérico asigna valores razonables
       cuando no se especifican todos los parámetros.

Ejemplo de uso:
    >>> libro = ProductoFactory.crear_libro("1984", 15.99, "George Orwell")
    >>> laptop = ProductoFactory.crear_electronico("Laptop", 899.99, 24)
    >>> generico = ProductoFactory.crear_producto("libro", "Test", 10.0)
"""

from patrones.producto import Libro, Electronico


class ProductoFactory:
    """Fábrica centralizada para la creación de productos.

    Todos los métodos son estáticos (@staticmethod) porque la fábrica no
    necesita mantener estado propio — solo crea y retorna objetos.
    """

    @staticmethod
    def crear_producto(tipo, nombre, precio):
        """Crea un producto genérico según el tipo indicado (texto).

        Método genérico que decide qué clase concreta instanciar basándose
        en el string 'tipo'. Asigna valores por defecto para los atributos
        específicos de cada tipo.

        Args:
            tipo (str): Tipo de producto ("libro" o "electronico"), sin
                        distinguir mayúsculas/minúsculas.
            nombre (str): Nombre del producto.
            precio (float): Precio del producto.

        Returns:
            Producto: Instancia de Libro o Electronico según el tipo.

        Raises:
            ValueError: Si el tipo no es "libro" ni "electronico".
        """
        tipo_lower = tipo.lower()
        if tipo_lower == "libro":
            return Libro(nombre, precio, "Autor Desconocido")
        elif tipo_lower == "electronico":
            return Electronico(nombre, precio, 12)
        else:
            raise ValueError(f"Tipo de producto no válido: {tipo}")

    @staticmethod
    def crear_libro(nombre, precio, autor):
        """Crea un producto de tipo Libro con todos sus atributos.

        Args:
            nombre (str): Título del libro.
            precio (float): Precio del libro.
            autor (str): Nombre del autor.

        Returns:
            Libro: Nueva instancia de Libro.
        """
        return Libro(nombre, precio, autor)

    @staticmethod
    def crear_electronico(nombre, precio, garantia):
        """Crea un producto de tipo Electrónico con todos sus atributos.

        Args:
            nombre (str): Nombre del dispositivo.
            precio (float): Precio del dispositivo.
            garantia (int): Meses de garantía.

        Returns:
            Electronico: Nueva instancia de Electronico.
        """
        return Electronico(nombre, precio, garantia)
