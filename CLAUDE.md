# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Educational Python project (Equipo: Desarrollo Los Cortez) demonstrating four design patterns (Singleton, Factory, Observer, Strategy) through an e-commerce scenario. Uses only the Python standard library — no external dependencies. Keep changes focused on the educational purpose of the repository.

## Running the Project

```bash
python main.py
```

Quick sanity checks for individual patterns:

```bash
# Singleton
python -c "from patrones.database_connection import DatabaseConnection; db1 = DatabaseConnection.get_instance(); db2 = DatabaseConnection.get_instance(); print('OK' if db1 is db2 else 'FAIL')"

# Factory
python -c "from patrones.producto_factory import ProductoFactory; p = ProductoFactory.crear_libro('Test', 10.0, 'Autor'); print('OK' if p.get_nombre() == 'Test' else 'FAIL')"
```

No build step, no linter configured, no test framework. Target Python 3.6+.

## Architecture

`main.py` is the entry point — it imports from the `patrones` package and demos each pattern in sequence.

The `patrones/` package has one module per pattern, each with an abstract interface (ABC) and concrete implementations:

| Pattern | Files | Key Classes |
|---------|-------|-------------|
| Singleton | `database_connection.py` | `DatabaseConnection` (`__new__` controls instance; `get_instance()` delegates to it) |
| Factory | `producto.py`, `producto_factory.py` | Abstract `Producto` → `Libro`, `Electronico`; `ProductoFactory` (static methods) |
| Observer | `observer.py`, `tienda.py` | Abstract `Observer` → `Cliente`; `Tienda` (validates Observer type, prevents duplicate subscriptions) |
| Strategy | `estrategia_pago.py`, `carrito_compra.py` | Abstract `EstrategiaPago` → `PagoTarjeta`, `PagoEfectivo`, `PagoPayPal`; `CarritoCompra` (resets after checkout) |

Patterns are intentionally decoupled — maintain this separation and avoid coupling patterns across modules unless part of an explicit refactor. There is no ORM or real database; `DatabaseConnection` prints to stdout. Extensions should keep this lightweight approach or clearly document added dependencies.

## Key Implementation Details

- **Tienda.suscribir()** validates `isinstance(cliente, Observer)` and rejects duplicates.
- **Tienda.desuscribir()** checks membership before removing to avoid `ValueError`.
- **PagoEfectivo.pagar()** uses `round(monto * 0.95, 2)` for monetary precision.
- **CarritoCompra.checkout()** clears `_productos` and `_estrategia_pago` after completing a purchase.

## Code Conventions

- Classes: `CamelCase`. Methods/variables: `snake_case`. Private attributes: `_prefixed`.
- Abstract interfaces use `abc.ABC` with `@abstractmethod`. Factory methods use `@staticmethod`.
- All output is via `print()` to stdout — no real DB, network, or file I/O.
- No type hints currently; acceptable to add if they improve clarity.
- Keep lines under ~100 chars. Use f-strings for formatting.
- All code and output is in Spanish (method names, print messages, documentation).
- All modules, classes, and methods have educational docstrings (Google style with Args/Returns/Raises). Maintain this convention when adding new code.

## Extending the Project

When adding new product types, observers, or payment strategies, follow the existing idiom: define an ABC interface, then implement concrete classes. For new payment methods, follow the constructor injection pattern seen in `carrito_compra.py` (`set_estrategia_pago`). Suggested improvements documented in README: type hints, `@property` decorators, `dataclasses`, context managers.
