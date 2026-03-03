# Patrones de Diseño en Python

Proyecto educativo que implementa cuatro patrones de diseño clásicos del libro *Gang of Four* aplicados a un sistema de comercio electrónico simulado. Todo el código está escrito en Python usando únicamente la biblioteca estándar (sin dependencias externas).

**Equipo:** Desarrollo Los Cortez
**Asignatura:** Metodología de Sistemas 2
**Python:** 3.6+

---

## Introducción

Este proyecto simula el núcleo de una tienda en línea con el objetivo de mostrar, en un contexto real y comprensible, cómo los patrones de diseño resuelven problemas concretos de arquitectura de software.

El sistema modela cuatro aspectos fundamentales de cualquier e-commerce:

1. **Gestión de recursos compartidos** — la aplicación necesita una única conexión a la base de datos sin importar cuántas partes del código la soliciten. El patrón *Singleton* garantiza esto.

2. **Catálogo de productos heterogéneo** — la tienda vende artículos de distinta naturaleza: libros (con autor) y electrónicos (con garantía). El patrón *Factory* centraliza su creación y oculta los detalles de cada tipo al código cliente.

3. **Sistema de notificaciones a clientes** — cuando la tienda publica una nueva oferta, todos los clientes suscritos deben ser notificados automáticamente. El patrón *Observer* desacopla a la tienda de sus clientes: la tienda no necesita saber quiénes son ni cuántos hay.

4. **Proceso de pago flexible** — al momento del checkout, el cliente puede pagar con tarjeta de crédito, efectivo (con descuento del 5%) o PayPal, y este método puede cambiar sin modificar el carrito. El patrón *Strategy* encapsula cada algoritmo de pago en su propia clase intercambiable.

Cada patrón vive en su propio subpaquete dentro de `patrones/`, con una interfaz abstracta (ABC) y sus implementaciones concretas, siguiendo la misma estructura en los cuatro casos para que el código sea predecible y fácil de extender.

---

## Patrones Implementados

| # | Patrón | Propósito en el proyecto | Clases principales |
|---|--------|--------------------------|-------------------|
| 1 | **Singleton** | Una única conexión a la base de datos en toda la app | `DatabaseConnection` |
| 2 | **Factory** | Crear distintos tipos de productos de forma centralizada | `ProductoFactory`, `Libro`, `Electronico` |
| 3 | **Observer** | Notificar a clientes suscritos cuando hay nuevas ofertas | `Tienda`, `Cliente` |
| 4 | **Strategy** | Elegir en tiempo de ejecución el método de pago del carrito | `CarritoCompra`, `PagoTarjeta`, `PagoEfectivo`, `PagoPayPal` |

---

## Estructura del Proyecto

```
patronesPython-main/
├── main.py                          # Punto de entrada — demo de los 4 patrones
├── requirements.txt                 # Sin dependencias externas
└── patrones/                        # Paquete principal
    ├── __init__.py
    ├── singleton/
    │   ├── __init__.py              # Re-exporta: DatabaseConnection
    │   └── database_connection.py
    ├── factory/
    │   ├── __init__.py              # Re-exporta: Producto, Libro, Electronico, ProductoFactory
    │   ├── producto.py
    │   └── producto_factory.py
    ├── observer/
    │   ├── __init__.py              # Re-exporta: Observer, Cliente, Tienda
    │   ├── observer.py
    │   └── tienda.py
    └── strategy/
        ├── __init__.py              # Re-exporta: EstrategiaPago, PagoTarjeta, PagoEfectivo, PagoPayPal, CarritoCompra
        ├── estrategia_pago.py
        └── carrito_compra.py
```

Cada subpaquete expone su API pública a través de su `__init__.py` con `__all__`, de modo que los imports desde `main.py` son limpios y no dependen de la estructura interna de archivos.

---

## Requisitos y Ejecución

**Requisitos:**
- Python 3.6 o superior
- Sin dependencias externas (solo biblioteca estándar de Python)

**Ejecutar la demo completa:**

```bash
python main.py
```

**Verificar patrones individualmente:**

```bash
# Singleton — confirma que dos llamadas devuelven el mismo objeto
python -c "from patrones.singleton import DatabaseConnection; db1 = DatabaseConnection.get_instance(); db2 = DatabaseConnection.get_instance(); print('Singleton OK' if db1 is db2 else 'ERROR')"

# Factory — crea un libro por método tipado y verifica su nombre
python -c "from patrones.factory import ProductoFactory; p = ProductoFactory.crear_libro('Test', 10.0, 'Autor'); print('Factory OK' if p.get_nombre() == 'Test' else 'ERROR')"

# Observer — suscribe un cliente dos veces y verifica que no se duplique
python -c "
from patrones.observer import Cliente, Tienda
t = Tienda('Test'); c = Cliente('Ana')
t.suscribir(c); t.suscribir(c)
print('Observer OK' if len(t._clientes) == 1 else 'ERROR')
"

# Strategy — hace checkout y verifica que el carrito quede vacío
python -c "
from patrones.factory import ProductoFactory
from patrones.strategy import CarritoCompra, PagoEfectivo
c = CarritoCompra(); c.set_estrategia_pago(PagoEfectivo())
c.agregar_producto(ProductoFactory.crear_libro('Test', 10.0, 'Autor'))
c.checkout()
print('Strategy OK' if c._productos == [] else 'ERROR')
"
```

---

## Descripción Detallada de Cada Patrón

---

### 1. Singleton — `patrones/singleton/`

**Problema que resuelve:** Garantizar que exista una única instancia de un objeto costoso de crear (como una conexión a base de datos) y proveer un punto de acceso global a esa instancia.

**Diagrama de clases:**

```
┌────────────────────────────────┐
│       DatabaseConnection       │
├────────────────────────────────┤
│ - _instance: cls (class var)   │
│ - _initialized: bool           │
│ - _connection_string: str      │
├────────────────────────────────┤
│ + __new__(cls)                 │  ← controla la creación
│ + __init__(self)               │  ← se ejecuta solo una vez
│ + get_instance() → self        │  ← punto de acceso público
│ + query(sql: str)              │
└────────────────────────────────┘
```

**Uso:**

```python
from patrones.singleton import DatabaseConnection

db1 = DatabaseConnection.get_instance()
db2 = DatabaseConnection.get_instance()

print(db1 is db2)      # True — misma instancia
db1.query("SELECT * FROM usuarios")
```

**Implementación Python:**

El patrón Singleton en Python requiere sobrescribir `__new__`, ya que es el método que crea el objeto antes de que `__init__` lo inicialice. El problema es que Python llama a `__init__` siempre, incluso cuando `__new__` devuelve una instancia existente. Por eso se usa un flag `_initialized`:

```python
class DatabaseConnection:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialized = False
        return cls._instance

    def __init__(self):
        if not self._initialized:
            self._connection_string = "mysql://localhost:3306/midb"
            self._initialized = True
            print(f"Conexión a BD creada: {self._connection_string}")
```

`get_instance()` es el punto de acceso convencional del patrón; internamente solo llama a `DatabaseConnection()`, delegando todo a `__new__`.

---

### 2. Factory — `patrones/factory/`

**Problema que resuelve:** Centralizar la creación de objetos de distintos tipos sin que el código cliente necesite conocer las clases concretas, facilitando agregar nuevos tipos de productos sin modificar el código existente.

**Diagrama de clases:**

```
        ┌──────────────────┐
        │    Producto      │  (ABC)
        │──────────────────│
        │ # _nombre: str   │
        │ # _precio: float │
        │──────────────────│
        │ + mostrar_info() │  ← @abstractmethod
        │ + get_nombre()   │
        │ + get_precio()   │
        └────────┬─────────┘
                 │
        ┌────────┴─────────┐
        │                  │
┌───────┴──────┐   ┌───────┴──────────┐
│    Libro     │   │    Electronico   │
│──────────────│   │──────────────────│
│ # _autor     │   │ # _garantia_meses│
│──────────────│   │──────────────────│
│ mostrar_info │   │ mostrar_info()   │
└──────────────┘   └──────────────────┘

┌────────────────────────────────────────┐
│           ProductoFactory              │
│────────────────────────────────────────│
│ + crear_producto(tipo, nombre, precio) │  ← @staticmethod (genérico)
│ + crear_libro(nombre, precio, autor)   │  ← @staticmethod (tipado)
│ + crear_electronico(nombre, precio,    │  ← @staticmethod (tipado)
│                     garantia)          │
└────────────────────────────────────────┘
```

**Uso:**

```python
from patrones.factory import ProductoFactory

# Métodos tipados (recomendados)
libro  = ProductoFactory.crear_libro("Cien Años de Soledad", 25.99, "García Márquez")
laptop = ProductoFactory.crear_electronico("Laptop HP", 899.99, 24)

libro.mostrar_info()   # Libro: Cien Años de Soledad | Autor: García Márquez | Precio: $25.99
laptop.mostrar_info()  # Electronico: Laptop HP | Garantía: 24 meses | Precio: $899.99

# Método genérico por string (case-insensitive)
p = ProductoFactory.crear_producto("LIBRO", "Don Quijote", 19.99)

# Tipo inválido lanza ValueError
ProductoFactory.crear_producto("videojuego", "FIFA", 59.99)  # ValueError
```

**Implementación Python:**

`Producto` es una clase abstracta real mediante `abc.ABC`. Intentar instanciarla directamente lanza `TypeError`. Las subclases deben implementar `mostrar_info()` o Python las tratará como abstractas también. `ProductoFactory` no tiene estado — todos sus métodos son `@staticmethod` y no hay necesidad de instanciarla.

---

### 3. Observer — `patrones/observer/`

**Problema que resuelve:** Cuando un objeto (la tienda) cambia de estado, notificar automáticamente a todos los objetos suscritos (clientes) sin que la tienda necesite conocer los detalles de cada cliente.

**Diagrama de clases:**

```
┌──────────────────────────┐         ┌───────────────────────────────────┐
│         Tienda           │         │           Observer                │ (ABC)
│──────────────────────────│  notif. │───────────────────────────────────│
│ - _nombre: str           │────────►│ + actualizar(mensaje: str)        │
│ - _clientes: list        │         └──────────────────┬────────────────┘
│──────────────────────────│                            │
│ + suscribir(cliente)     │                   ┌────────┴────────┐
│ + desuscribir(cliente)   │                   │    Cliente      │
│ + notificar_clientes(msg)│                   │─────────────────│
│ + nueva_oferta(desc)     │                   │ - _nombre: str  │
└──────────────────────────┘                   │─────────────────│
                                               │ + actualizar()  │
                                               │ + get_nombre()  │
                                               └─────────────────┘
```

**Uso:**

```python
from patrones.observer import Cliente, Tienda

tienda = Tienda("TechStore")
juan   = Cliente("Juan Pérez")
maria  = Cliente("María López")

tienda.suscribir(juan)
tienda.suscribir(maria)
tienda.nueva_oferta("50% descuento en laptops")
# → Cliente Juan Pérez recibió notificación: Nueva oferta: 50% descuento en laptops
# → Cliente María López recibió notificación: Nueva oferta: 50% descuento en laptops

tienda.desuscribir(maria)
tienda.nueva_oferta("Black Friday: 70% de descuento")
# → solo Juan recibe la notificación
```

**Validaciones implementadas en `Tienda`:**

| Situación | Comportamiento |
|-----------|---------------|
| `suscribir()` con objeto que no es `Observer` | Lanza `TypeError` |
| `suscribir()` con cliente ya suscrito | Imprime aviso y no duplica |
| `desuscribir()` con cliente no suscrito | Imprime aviso sin lanzar excepción |

```python
# Ejemplo de validación de tipo
tienda.suscribir("no soy un observer")  # TypeError: El cliente debe ser una instancia de Observer
```

---

### 4. Strategy — `patrones/strategy/`

**Problema que resuelve:** Definir una familia de algoritmos (métodos de pago), encapsular cada uno y hacerlos intercambiables en tiempo de ejecución, sin modificar el código del contexto que los usa (el carrito de compras).

**Diagrama de clases:**

```
┌──────────────────────────┐       ┌─────────────────────────┐
│      CarritoCompra       │       │     EstrategiaPago      │  (ABC)
│  (Contexto)              │uses   │─────────────────────────│
│──────────────────────────│──────►│ + pagar(monto: float)   │
│ - _productos: list       │       └────────────┬────────────┘
│ - _estrategia_pago       │                    │
│──────────────────────────│       ┌────────────┼────────────┐
│ + agregar_producto(p)    │       │            │            │
│ + set_estrategia_pago(e) │  ┌────┴───┐  ┌────┴────┐  ┌───┴──────┐
│ + calcular_total()       │  │  Pago  │  │  Pago   │  │  Pago    │
│ + checkout()             │  │Tarjeta │  │Efectivo │  │ PayPal   │
└──────────────────────────┘  └────────┘  └─────────┘  └──────────┘
```

**Uso:**

```python
from patrones.factory import ProductoFactory
from patrones.strategy import CarritoCompra, PagoTarjeta, PagoEfectivo, PagoPayPal

libro  = ProductoFactory.crear_libro("Don Quijote", 19.99, "Cervantes")
laptop = ProductoFactory.crear_electronico("Laptop HP", 899.99, 24)

# Pago con tarjeta
carrito1 = CarritoCompra()
carrito1.agregar_producto(libro)
carrito1.agregar_producto(laptop)
carrito1.set_estrategia_pago(PagoTarjeta("4532-1234-5678-9012"))
carrito1.checkout()
# Pagando $919.98 con tarjeta terminada en 9012

# Pago en efectivo (5% de descuento automático)
carrito2 = CarritoCompra()
carrito2.agregar_producto(laptop)
carrito2.set_estrategia_pago(PagoEfectivo())
carrito2.checkout()
# Total a pagar: $854.99 (con 5% descuento aplicado)

# Pago con PayPal
carrito3 = CarritoCompra()
carrito3.agregar_producto(libro)
carrito3.set_estrategia_pago(PagoPayPal("usuario@email.com"))
carrito3.checkout()
# Pagando $19.99 con PayPal desde la cuenta: usuario@email.com
```

**Comportamiento de cada estrategia:**

| Estrategia | Constructor | Lógica de pago |
|------------|-------------|----------------|
| `PagoTarjeta` | `numero_tarjeta: str` | Muestra los últimos 4 dígitos (`[-4:]`) |
| `PagoEfectivo` | sin parámetros | Aplica 5% descuento con `round(monto * 0.95, 2)` |
| `PagoPayPal` | `email: str` | Muestra el correo asociado |

**Validaciones en `CarritoCompra.checkout()`:**

- Si el carrito está vacío → imprime aviso y no procede
- Si no se estableció una estrategia de pago → imprime aviso y no procede
- Al completar el checkout → **el carrito se resetea** (`_productos = []`, `_estrategia_pago = None`)

El reset post-checkout es intencional: previene cobros duplicados y obliga a configurar una nueva estrategia para cada compra.

---

## Integración entre Patrones

`main.py` demuestra cómo los patrones coexisten en un escenario realista:

```
main.py
  │
  ├── Singleton ──────────────── Una conexión DB compartida durante toda la ejecución
  │
  ├── Factory ─────────────────── Crea: libro1, libro2, laptop, iphone
  │             └──────────────── Los productos creados aquí se reutilizan en Strategy
  │
  ├── Observer ────────────────── Tienda notifica a 3 clientes → desuscribe 1 → notifica a 2
  │
  └── Strategy ─────────────────  carrito1 (libro1 + laptop)  → PagoTarjeta
                                   carrito2 (iphone + libro2)  → PagoEfectivo
                                   carrito3 (laptop + iphone)  → PagoPayPal
```

Los objetos `libro1`, `libro2`, `laptop` e `iphone` se instancian una sola vez en la sección Factory y se agregan directamente a los carritos de la sección Strategy, mostrando que los productos son objetos reutilizables independientes del patrón que los creó.

---

## Salida Completa del Programa

```
==================================================
DEMOSTRACIÓN DE PATRONES DE DISEÑO EN PYTHON
==================================================

>>> 1. PATRÓN SINGLETON <<<
Conexión a BD creada: mysql://localhost:3306/midb
¿Son la misma instancia? True
Ejecutando query: SELECT * FROM usuarios

>>> 2. PATRÓN FACTORY <<<
Libro: Cien Años de Soledad | Autor: Gabriel García Márquez | Precio: $25.99
Libro: Don Quijote | Autor: Miguel de Cervantes | Precio: $19.99
Electronico: Laptop HP | Garantía: 24 meses | Precio: $899.99
Electronico: iPhone 15 | Garantía: 12 meses | Precio: $999.99

>>> 3. PATRÓN OBSERVER <<<
Cliente suscrito a la tienda TechStore
Cliente suscrito a la tienda TechStore
Cliente suscrito a la tienda TechStore

¡Nueva oferta en TechStore!

--- Notificando a 3 clientes ---
Cliente Juan Pérez recibió notificación: Nueva oferta: 50% descuento en laptops
Cliente María López recibió notificación: Nueva oferta: 50% descuento en laptops
Cliente Carlos Gómez recibió notificación: Nueva oferta: 50% descuento en laptops

Cliente desuscrito de la tienda TechStore

¡Nueva oferta en TechStore!

--- Notificando a 2 clientes ---
Cliente Juan Pérez recibió notificación: Nueva oferta: Black Friday: Todo al 70% de descuento
Cliente Carlos Gómez recibió notificación: Nueva oferta: Black Friday: Todo al 70% de descuento

>>> 4. PATRÓN STRATEGY <<<
Producto agregado al carrito: Cien Años de Soledad
Producto agregado al carrito: Laptop HP

=== CHECKOUT ===
Productos en el carrito:
Libro: Cien Años de Soledad | Autor: Gabriel García Márquez | Precio: $25.99
Electronico: Laptop HP | Garantía: 24 meses | Precio: $899.99
Total: $925.98
Pagando $925.98 con tarjeta terminada en 9012
¡Compra completada!

Producto agregado al carrito: iPhone 15
Producto agregado al carrito: Don Quijote

=== CHECKOUT ===
Productos en el carrito:
Electronico: iPhone 15 | Garantía: 12 meses | Precio: $999.99
Libro: Don Quijote | Autor: Miguel de Cervantes | Precio: $19.99
Total: $1019.98
Pagando $1019.98 en efectivo. Se aplicó 5% descuento.
Total a pagar: $968.98
¡Compra completada!

Producto agregado al carrito: Laptop HP
Producto agregado al carrito: iPhone 15

=== CHECKOUT ===
Productos en el carrito:
Electronico: Laptop HP | Garantía: 24 meses | Precio: $899.99
Electronico: iPhone 15 | Garantía: 12 meses | Precio: $999.99
Total: $1899.98
Pagando $1899.98 con PayPal desde la cuenta: usuario@email.com
¡Compra completada!

==================================================
FIN DE LA DEMOSTRACIÓN
==================================================
```

---

## Características de Python Utilizadas

| Característica | Dónde se usa |
|----------------|-------------|
| `__new__` + `_initialized` | Singleton — controla instancia única sin re-inicialización |
| `abc.ABC` + `@abstractmethod` | Factory, Observer, Strategy — define interfaces obligatorias |
| `@staticmethod` | `ProductoFactory` — métodos de creación sin estado de instancia |
| `isinstance()` | `Tienda.suscribir()` — validación de tipo en runtime |
| Índice negativo `[-4:]` | `PagoTarjeta` — extrae últimos 4 dígitos de forma idiomática |
| `round(x, 2)` | `PagoEfectivo` — evita errores de precisión en aritmética flotante |
| f-strings | En toda la capa de presentación (`print`) |
| `__all__` en `__init__.py` | Declara la API pública de cada subpaquete |

---

## Extensiones Sugeridas

```python
# 1. Type hints para mejor documentación y autocompletado
def crear_libro(nombre: str, precio: float, autor: str) -> Libro: ...

# 2. @property en lugar de getters explícitos
@property
def nombre(self) -> str:
    return self._nombre

# 3. dataclasses para simplificar clases de datos (Python 3.7+)
from dataclasses import dataclass

@dataclass
class Libro(Producto):
    autor: str

# 4. decimal.Decimal para precisión monetaria real (en lugar de round())
from decimal import Decimal
descuento = Decimal(str(monto)) * Decimal("0.95")

# 5. Context manager en Singleton para garantizar cierre de recursos
with DatabaseConnection.get_instance() as db:
    db.query("SELECT * FROM pedidos")
```

---

## Licencia

Proyecto educativo — uso libre para aprendizaje y estudio.
