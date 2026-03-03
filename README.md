# Patrones de Diseño en Python

Proyecto educativo que demuestra 4 patrones de diseño fundamentales aplicados a un sistema de comercio electrónico en Python.

- **Singleton**: Gestión de conexión única a base de datos
- **Factory**: Creación de diferentes tipos de productos (Libros y Electrónicos)
- **Observer**: Sistema de notificaciones para clientes de una tienda
- **Strategy**: Múltiples estrategias de pago (Tarjeta, Efectivo, PayPal)

## Estructura del Proyecto

```
├── main.py                              # Demostración completa de todos los patrones
├── patrones/                            # Paquete principal
│   ├── __init__.py                      # Documentación del paquete
│   ├── singleton/                       # Patrón Singleton
│   │   ├── __init__.py                  # Re-exporta DatabaseConnection
│   │   └── database_connection.py       # Conexión única a BD
│   ├── factory/                         # Patrón Factory
│   │   ├── __init__.py                  # Re-exporta Producto, Libro, Electronico, ProductoFactory
│   │   ├── producto.py                  # Clase abstracta base y productos concretos
│   │   └── producto_factory.py          # Fábrica centralizada de productos
│   ├── observer/                        # Patrón Observer
│   │   ├── __init__.py                  # Re-exporta Observer, Cliente, Tienda
│   │   ├── observer.py                  # Interfaz Observer y Cliente concreto
│   │   └── tienda.py                    # Sujeto observable (Tienda)
│   └── strategy/                        # Patrón Strategy
│       ├── __init__.py                  # Re-exporta estrategias y CarritoCompra
│       ├── estrategia_pago.py           # Interfaz y estrategias de pago concretas
│       └── carrito_compra.py            # Contexto (Carrito de Compras)
├── README.md                            # Este archivo
└── requirements.txt                     # Dependencias (ninguna)
```

## Requisitos

- Python 3.6 o superior
- No requiere dependencias externas (solo biblioteca estándar)

## Ejecución

```bash
python main.py
```

O usando Python 3 explícitamente:

```bash
python3 main.py
```

En sistemas Unix/Linux, también puedes hacer el archivo ejecutable:

```bash
chmod +x main.py
./main.py
```

## Patrones Implementados

### 1. Singleton - DatabaseConnection

**Archivo**: `patrones/singleton/database_connection.py`

Garantiza una única instancia de conexión a la base de datos en toda la aplicación.

```python
db1 = DatabaseConnection.get_instance()
db2 = DatabaseConnection.get_instance()
print(db1 is db2)  # True - misma instancia
```

**Características Python**:
- Usa `__new__` para controlar la creación de instancias
- Variable de clase `_instance` almacena la única instancia
- Flag `_initialized` previene reinicialización

### 2. Factory - ProductoFactory

**Archivos**:
- `patrones/factory/producto.py` (Producto, Libro, Electronico)
- `patrones/factory/producto_factory.py` (ProductoFactory)

Centraliza la creación de diferentes tipos de productos.

```python
libro = ProductoFactory.crear_libro("Cien Años de Soledad", 25.99, "García Márquez")
laptop = ProductoFactory.crear_electronico("Laptop HP", 899.99, 24)
```

**Características Python**:
- Usa ABC (Abstract Base Class) para clase abstracta
- Decorador `@abstractmethod` para métodos abstractos
- Métodos estáticos con `@staticmethod`

### 3. Observer - Tienda y Cliente

**Archivos**:
- `patrones/observer/observer.py` (Observer, Cliente)
- `patrones/observer/tienda.py` (Tienda)

Sistema de notificaciones donde la tienda notifica a clientes suscritos sobre ofertas.

```python
tienda = Tienda("TechStore")
cliente = Cliente("Juan Pérez")
tienda.suscribir(cliente)
tienda.nueva_oferta("50% descuento en laptops")
```

**Características Python**:
- Interfaz Observer usando ABC
- Lista de observadores gestionada con list nativo
- Notificación mediante iteración simple

### 4. Strategy - CarritoCompra y Estrategias de Pago

**Archivos**:
- `patrones/strategy/estrategia_pago.py` (EstrategiaPago, PagoTarjeta, PagoEfectivo, PagoPayPal)
- `patrones/strategy/carrito_compra.py` (CarritoCompra)

Permite cambiar dinámicamente el método de pago del carrito.

```python
carrito = CarritoCompra()
carrito.agregar_producto(libro)
carrito.set_estrategia_pago(PagoTarjeta("4532-1234-5678-9012"))
carrito.checkout()
```

**Características Python**:
- Interfaz de estrategia usando ABC
- Tres implementaciones concretas de pago
- Contexto (CarritoCompra) mantiene referencia a estrategia actual

## Características de Python Utilizadas

1. **Duck Typing**: No es necesario declarar tipos explícitamente
2. **Properties**: Los getters se implementan con convención `_variable` privada
3. **Métodos Mágicos**: `__init__`, `__new__` para Singleton
4. **Decoradores**: `@abstractmethod`, `@staticmethod`
5. **ABC Module**: Para clases abstractas e interfaces
6. **F-strings**: Para formateo de cadenas (`f"texto {variable}"`)
7. **List nativas**: Sin necesidad de importar ArrayList

## Salida del Programa

```
==================================================
DEMOSTRACIÓN DE PATRONES DE DISEÑO EN PYTHON
==================================================

>>> 1. PATRÓN SINGLETON <<<
Conexión a BD creada: mysql://localhost:3306/midb
¿Son la misma instancia? True
Ejecutando query: SELECT * FROM usuarios

>>> 2. PATRÓN FACTORY <<<
[Lista de productos creados...]

>>> 3. PATRÓN OBSERVER <<<
[Notificaciones a clientes...]

>>> 4. PATRÓN STRATEGY <<<
[Diferentes carritos con distintos métodos de pago...]

==================================================
FIN DE LA DEMOSTRACIÓN
==================================================
```

## Extensiones Posibles

1. **Type Hints**: Agregar anotaciones de tipo para mejor documentación
   ```python
   def crear_libro(nombre: str, precio: float, autor: str) -> Libro:
   ```

2. **Dataclasses**: Simplificar clases de datos (Python 3.7+)
   ```python
   from dataclasses import dataclass
   ```

3. **Properties**: Usar `@property` para getters más pythónicos
   ```python
   @property
   def nombre(self):
       return self._nombre
   ```

4. **Context Managers**: Para gestión de recursos en Singleton
   ```python
   with DatabaseConnection.get_instance() as db:
       db.query("SELECT...")
   ```

## Pruebas

Para verificar que cada patrón funciona correctamente:

```bash
# Prueba individual del Singleton
python -c "from patrones.singleton import DatabaseConnection; db1 = DatabaseConnection.get_instance(); db2 = DatabaseConnection.get_instance(); print('Singleton OK' if db1 is db2 else 'ERROR')"

# Prueba individual del Factory
python -c "from patrones.factory import ProductoFactory; p = ProductoFactory.crear_libro('Test', 10.0, 'Autor'); print('Factory OK' if p.get_nombre() == 'Test' else 'ERROR')"
```

## Autor

Proyecto educativo de Patrones de Diseño
Equipo: Desarrollo Los Cortez

## Licencia

Proyecto educativo - Uso libre para aprendizaje
