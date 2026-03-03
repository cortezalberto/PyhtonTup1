"""
Patrón Factory - Clases base y productos concretos.

El patrón Factory centraliza la creación de objetos en un solo lugar,
evitando que el código cliente conozca las clases concretas que instancia.

Este módulo define:
    - Producto: Clase abstracta base que establece la interfaz común.
    - Libro: Producto concreto que representa un libro con autor.
    - Electronico: Producto concreto que representa un dispositivo con garantía.

Concepto clave - Clase Abstracta (ABC):
    Una clase abstracta NO se puede instanciar directamente. Sirve como
    "contrato" que obliga a las subclases a implementar ciertos métodos.
    En Python se logra heredando de ABC y usando @abstractmethod.

Ejemplo de uso:
    >>> libro = Libro("Don Quijote", 19.99, "Cervantes")
    >>> libro.mostrar_info()
    Libro: Don Quijote | Autor: Cervantes | Precio: $19.99
"""

from abc import ABC, abstractmethod


class Producto(ABC):
    """Clase abstracta base para todos los productos del sistema.

    Define la interfaz común que deben cumplir todos los productos.
    No se puede instanciar directamente (es abstracta).

    Atributos:
        _nombre (str): Nombre del producto.
        _precio (float): Precio del producto.
    """

    def __init__(self, nombre, precio):
        """Inicializa los atributos comunes a todos los productos.

        Args:
            nombre (str): Nombre del producto.
            precio (float): Precio del producto.
        """
        self._nombre = nombre
        self._precio = precio

    @abstractmethod
    def mostrar_info(self):
        """Muestra la información del producto en consola.

        Cada subclase DEBE implementar este método con su propio formato.
        Si no lo implementa, Python lanzará TypeError al intentar instanciarla.
        """
        pass

    def get_nombre(self):
        """Retorna el nombre del producto."""
        return self._nombre

    def get_precio(self):
        """Retorna el precio del producto."""
        return self._precio


class Libro(Producto):
    """Producto concreto que representa un libro.

    Hereda de Producto y agrega el atributo _autor.
    Implementa mostrar_info() con el formato específico para libros.

    Atributos:
        _autor (str): Nombre del autor del libro.
    """

    def __init__(self, nombre, precio, autor):
        """Inicializa un libro con nombre, precio y autor.

        Args:
            nombre (str): Título del libro.
            precio (float): Precio del libro.
            autor (str): Nombre del autor.
        """
        super().__init__(nombre, precio)
        self._autor = autor

    def mostrar_info(self):
        """Muestra la información del libro: título, autor y precio."""
        print(f"Libro: {self._nombre} | Autor: {self._autor} | Precio: ${self._precio}")


class Electronico(Producto):
    """Producto concreto que representa un dispositivo electrónico.

    Hereda de Producto y agrega el atributo _garantia_meses.
    Implementa mostrar_info() con el formato específico para electrónicos.

    Atributos:
        _garantia_meses (int): Duración de la garantía en meses.
    """

    def __init__(self, nombre, precio, garantia_meses):
        """Inicializa un electrónico con nombre, precio y garantía.

        Args:
            nombre (str): Nombre del dispositivo.
            precio (float): Precio del dispositivo.
            garantia_meses (int): Meses de garantía.
        """
        super().__init__(nombre, precio)
        self._garantia_meses = garantia_meses

    def mostrar_info(self):
        """Muestra la información del electrónico: nombre, garantía y precio."""
        print(f"Electrónico: {self._nombre} | Garantía: {self._garantia_meses} meses | Precio: ${self._precio}")
