"""
Patrón Strategy - Contexto (Carrito de Compras).

En el patrón Strategy, el "contexto" es la clase que UTILIZA las estrategias
sin conocer su implementación interna. En este caso, CarritoCompra delega
el procesamiento del pago a cualquier objeto que implemente EstrategiaPago.

Relación con el patrón:
    - CarritoCompra = Contexto (usa la estrategia).
    - EstrategiaPago = Interfaz de estrategia (contrato).
    - PagoTarjeta/PagoEfectivo/PagoPayPal = Estrategias concretas.

Flujo de uso:
    1. Crear un carrito: carrito = CarritoCompra()
    2. Agregar productos: carrito.agregar_producto(producto)
    3. Elegir forma de pago: carrito.set_estrategia_pago(PagoTarjeta(...))
    4. Finalizar compra: carrito.checkout()
    5. Tras el checkout, el carrito se vacía automáticamente.

Ejemplo de uso:
    >>> carrito = CarritoCompra()
    >>> carrito.agregar_producto(libro)
    >>> carrito.set_estrategia_pago(PagoEfectivo())
    >>> carrito.checkout()
"""


class CarritoCompra:
    """Carrito de compras que utiliza el patrón Strategy para el pago.

    El carrito acumula productos y, al momento del checkout, delega
    el procesamiento del pago a la estrategia configurada.

    Atributos:
        _productos (list): Lista de productos agregados al carrito.
        _estrategia_pago (EstrategiaPago | None): Método de pago seleccionado.
    """

    def __init__(self):
        """Inicializa un carrito vacío sin método de pago seleccionado."""
        self._productos = []
        self._estrategia_pago = None

    def agregar_producto(self, producto):
        """Agrega un producto al carrito.

        Args:
            producto (Producto): El producto a agregar (Libro o Electronico).
        """
        self._productos.append(producto)
        print(f"Producto agregado al carrito: {producto.get_nombre()}")

    def set_estrategia_pago(self, estrategia_pago):
        """Establece o cambia el método de pago del carrito.

        Este es el método clave del patrón Strategy: permite cambiar
        el comportamiento de pago en tiempo de ejecución sin modificar
        la clase CarritoCompra.

        Args:
            estrategia_pago (EstrategiaPago): La estrategia de pago a usar.
        """
        self._estrategia_pago = estrategia_pago

    def calcular_total(self):
        """Calcula la suma de los precios de todos los productos.

        Returns:
            float: El total acumulado de los productos en el carrito.
        """
        total = 0
        for producto in self._productos:
            total += producto.get_precio()
        return total

    def checkout(self):
        """Finaliza la compra: muestra resumen, calcula total y procesa el pago.

        Validaciones antes de proceder:
            1. El carrito no debe estar vacío.
            2. Debe haber un método de pago seleccionado.

        Flujo exitoso:
            - Muestra todos los productos con mostrar_info().
            - Calcula el total con calcular_total().
            - Delega el pago a self._estrategia_pago.pagar(total).
            - Vacía el carrito y resetea la estrategia de pago.
        """
        if not self._productos:
            print("El carrito está vacío")
            return

        if self._estrategia_pago is None:
            print("Debe seleccionar un método de pago")
            return

        total = self.calcular_total()
        print("\n=== CHECKOUT ===")
        print("Productos en el carrito:")
        for producto in self._productos:
            producto.mostrar_info()
        print(f"Total: ${total}")
        self._estrategia_pago.pagar(total)
        print("¡Compra completada!\n")
        self._productos = []
        self._estrategia_pago = None
