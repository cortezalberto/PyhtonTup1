#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Demostración de Patrones de Diseño en Python - Sistema de Comercio Electrónico.

Este archivo es el punto de entrada del programa. Ejecuta demostraciones
de los 4 patrones de diseño implementados en el paquete 'patrones/':

    1. Singleton  - Una sola conexión a base de datos para toda la app.
    2. Factory    - Creación centralizada de productos (Libro, Electrónico).
    3. Observer   - Notificaciones automáticas a clientes suscritos.
    4. Strategy   - Diferentes formas de pago intercambiables.

Ejecución:
    python main.py

Cada sección está claramente separada para que el estudiante pueda
identificar qué patrón se está demostrando y cómo se usa.
"""

# Importaciones organizadas por patrón
from patrones.database_connection import DatabaseConnection  # Singleton
from patrones.producto_factory import ProductoFactory         # Factory
from patrones.observer import Cliente                         # Observer
from patrones.tienda import Tienda                            # Observer
from patrones.carrito_compra import CarritoCompra             # Strategy
from patrones.estrategia_pago import PagoTarjeta, PagoEfectivo, PagoPayPal  # Strategy


def main():
    """Función principal que demuestra todos los patrones de diseño."""
    print("=" * 50)
    print("DEMOSTRACIÓN DE PATRONES DE DISEÑO EN PYTHON")
    print("=" * 50)
    print()

    # ============================================
    # 1. PATRÓN SINGLETON - Conexión a BD
    # ============================================
    # Demuestra que get_instance() siempre retorna el MISMO objeto.
    # No importa cuántas veces se llame, solo existe una conexión.
    print(">>> 1. PATRÓN SINGLETON <<<")
    db1 = DatabaseConnection.get_instance()
    db2 = DatabaseConnection.get_instance()

    # 'is' compara identidad (misma posición en memoria), no igualdad de valor
    print(f"¿Son la misma instancia? {db1 is db2}")
    db1.query("SELECT * FROM usuarios")
    print()

    # ============================================
    # 2. PATRÓN FACTORY - Crear productos
    # ============================================
    # La fábrica crea objetos sin que el cliente necesite conocer
    # las clases concretas (Libro, Electronico). Solo usa ProductoFactory.
    print(">>> 2. PATRÓN FACTORY <<<")
    libro1 = ProductoFactory.crear_libro("Cien Años de Soledad", 25.99, "Gabriel García Márquez")
    libro2 = ProductoFactory.crear_libro("Don Quijote", 19.99, "Miguel de Cervantes")
    laptop = ProductoFactory.crear_electronico("Laptop HP", 899.99, 24)
    telefono = ProductoFactory.crear_electronico("iPhone 15", 999.99, 12)

    # mostrar_info() es polimórfico: cada producto muestra su formato propio
    libro1.mostrar_info()
    libro2.mostrar_info()
    laptop.mostrar_info()
    telefono.mostrar_info()
    print()

    # ============================================
    # 3. PATRÓN OBSERVER - Sistema de notificaciones
    # ============================================
    # Los clientes se suscriben a la tienda. Cuando hay una oferta,
    # todos los suscritos reciben la notificación automáticamente.
    print(">>> 3. PATRÓN OBSERVER <<<")
    tienda = Tienda("TechStore")

    cliente1 = Cliente("Juan Pérez")
    cliente2 = Cliente("María López")
    cliente3 = Cliente("Carlos Gómez")

    # Suscribir 3 clientes -> los 3 recibirán la primera oferta
    tienda.suscribir(cliente1)
    tienda.suscribir(cliente2)
    tienda.suscribir(cliente3)

    tienda.nueva_oferta("50% descuento en laptops")

    # Desuscribir a María -> solo Juan y Carlos recibirán la siguiente oferta
    print()
    tienda.desuscribir(cliente2)
    print()

    tienda.nueva_oferta("Black Friday: Todo al 70% de descuento")
    print()

    # ============================================
    # 4. PATRÓN STRATEGY - Diferentes formas de pago
    # ============================================
    # Cada carrito usa una estrategia de pago diferente.
    # El CarritoCompra no sabe cómo funciona cada pago internamente;
    # solo llama a pagar() y la estrategia se encarga del resto.
    print(">>> 4. PATRÓN STRATEGY <<<")

    # Carrito 1 - Pago con tarjeta (muestra solo últimos 4 dígitos)
    carrito1 = CarritoCompra()
    carrito1.agregar_producto(libro1)
    carrito1.agregar_producto(laptop)
    carrito1.set_estrategia_pago(PagoTarjeta("4532-1234-5678-9012"))
    carrito1.checkout()

    # Carrito 2 - Pago en efectivo (aplica 5% de descuento automáticamente)
    carrito2 = CarritoCompra()
    carrito2.agregar_producto(telefono)
    carrito2.agregar_producto(libro2)
    carrito2.set_estrategia_pago(PagoEfectivo())
    carrito2.checkout()

    # Carrito 3 - Pago con PayPal (usa email como identificador)
    carrito3 = CarritoCompra()
    carrito3.agregar_producto(laptop)
    carrito3.agregar_producto(telefono)
    carrito3.set_estrategia_pago(PagoPayPal("usuario@email.com"))
    carrito3.checkout()

    print("=" * 50)
    print("FIN DE LA DEMOSTRACIÓN")
    print("=" * 50)


# Este bloque asegura que main() solo se ejecute cuando el archivo
# se ejecuta directamente (python main.py), no cuando se importa como módulo.
if __name__ == "__main__":
    main()
