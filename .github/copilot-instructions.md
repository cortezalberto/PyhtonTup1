# Project Guidelines

This repository is a small educational Python project demonstrating four classical design patterns
(Singleton, Factory, Observer, Strategy) through a simple e-commerce scenario. Agents should
be aware that the code is intentionally lightweight and relies solely on the Python standard library.

## Code Style

- Python 3.x syntax is used throughout (target 3.6+ with f-strings, `abc` module, etc.).
- Follow existing conventions in `patrones/`:
  - Classes use `CamelCase`; methods and variables use `snake_case`.
  - Private attributes are prefixed with an underscore (`_`).
  - No type hints currently, but new code may add them if it improves clarity.
  - The repository doesn’t enforce a linter; however, keep lines under ~80–100 chars and
    use f-strings as seen in examples like `main.py` and `README.md`.
- Use the `abc` module for abstract base classes with `@abstractmethod` and `@staticmethod`
as already shown in `producto.py`, `observer.py`, and `estrategia_pago.py`.

## Architecture

- `main.py` drives the demonstration; it instantiates objects from the `patrones` package
  and exercises each pattern in sequence.
- The `patrones` package contains one file per pattern:
  - `database_connection.py` – Singleton implementation controlling a fake DB connection.
  - `producto.py` + `producto_factory.py` – Factory pattern for creating `Libro`/`Electronico`.
  - `observer.py` + `tienda.py` – Observer pattern for notifying subscribed customers.
  - `estrategia_pago.py` + `carrito_compra.py` – Strategy pattern for different payment methods.

Agents should maintain this separation and avoid coupling patterns across modules unless the
change is part of an explicit refactor or improvement.

## Build and Test

- There is no build step; the project runs directly with Python.
- Dependencies: none listed in `requirements.txt` (empty). Targeting the standard library.
- Run the demo with:

  ```bash
  python main.py
  ```

- Simple sanity checks are already provided in the README under "Pruebas"; agents should
  use those as a basis if writing additional tests or CLI commands.

## Project Conventions

- Each pattern has its own module(s) and typically defines an interface/abstract class
  followed by concrete implementations.
- Factory methods are implemented as `@staticmethod` on `ProductoFactory`.
- Singleton uses `__new__` with a `_instance` class variable and `_initialized` flag.
- Observe how each module uses ABCs to express interfaces – new code should follow that
  idiom when adding similar extensible behavior.
- There is no ORM or real database; the `DatabaseConnection` class prints to stdout. Any
  extension should keep this lightweight approach or clearly document added dependencies.

## Integration Points

- The only external interactions are via printing to stdout. No network or file I/O.
- Future expansions might mock a real database or add additional payment gateways; follow
  the pattern of constructor injection and strategy selection seen in `carrito_compra.py`.

## Security

- There is no sensitive information stored or handled. The `DatabaseConnection` URL is a
  hard-coded string in `main.py`.
- Agents need not worry about authentication/authorization; if security features are added,
  clearly document where secrets are stored and how they are accessed.

---

Agents should read `README.md` when they need context on how the patterns are intended to
work. Keep changes focused on the educational purpose of the repository. Ask for clarification
if a requested feature seems outside the scope of a simple design-pattern demo.