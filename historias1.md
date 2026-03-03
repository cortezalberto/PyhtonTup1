# Historias de Usuario - Sistema E-Commerce con Patrones de Diseño

**Proyecto:** Patrones de Diseño en Python
**Equipo:** Desarrollo Los Cortez
**Fecha:** Marzo 2026
**Versión:** 2.0 (Código corregido y documentado)

---

## Roles del Sistema

| Rol | Descripcion |
|-----|-------------|
| **Desarrollador** | Programador que construye y mantiene el sistema aplicando patrones de diseno |
| **Comprador** | Usuario final que navega productos, arma su carrito y realiza compras |
| **Administrador de tienda** | Responsable de gestionar la tienda, publicar ofertas y manejar suscriptores |
| **Cliente suscrito** | Comprador que se suscribio a notificaciones de una tienda |

---

## EPICA 1: Gestion de Conexion a Base de Datos (Patron Singleton)

> **Objetivo:** Garantizar una unica conexion a la base de datos durante toda la ejecucion, evitando consumo de recursos y conflictos de acceso concurrente.
>
> **Patron aplicado:** Singleton
>
> **Archivos involucrados:** `patrones/database_connection.py`

---

### HU-001: Crear una unica instancia de conexion a base de datos

**Como** desarrollador del sistema,
**quiero** que la clase `DatabaseConnection` permita crear una sola instancia durante toda la ejecucion,
**para** evitar que multiples partes del codigo abran conexiones duplicadas que consuman recursos innecesariamente.

**Criterios de Aceptacion:**

1. La clase `DatabaseConnection` utiliza el metodo especial `__new__()` para interceptar la creacion del objeto antes de que Python lo inicialice.
2. Existe una variable de clase `_instance` (inicializada en `None`) que almacena la referencia a la unica instancia.
3. Si `_instance` es `None`, se crea una nueva instancia usando `super().__new__(cls)` y se asigna a `_instance`.
4. Si `_instance` ya existe, `__new__()` retorna la instancia existente sin crear otra.
5. Al verificar `db1 = DatabaseConnection()` y `db2 = DatabaseConnection()`, la expresion `db1 is db2` retorna `True`.

**Datos Tecnicos:**

| Elemento | Detalle |
|----------|---------|
| Clase | `DatabaseConnection` |
| Metodo clave | `__new__(cls)` |
| Variable de control | `_instance` (variable de clase) |
| Lineas de codigo | `database_connection.py:37-49` |

**Definicion de Hecho:**
- [x] `__new__()` implementado y controla la creacion.
- [x] `db1 is db2` retorna `True` en todos los flujos.
- [x] No se crean objetos duplicados en memoria.

---

### HU-002: Prevenir la reinicializacion de la conexion

**Como** desarrollador del sistema,
**quiero** que los datos de conexion no se reinicialicen aunque se invoque el constructor multiples veces,
**para** proteger la configuracion de la conexion y evitar perdida de estado.

**Criterios de Aceptacion:**

1. Existe un flag de instancia `_initialized` (tipo `bool`) que se establece en `False` al crear el objeto en `__new__()`.
2. El metodo `__init__()` verifica `if not self._initialized` antes de ejecutar la logica de configuracion.
3. La cadena de conexion `_connection_string` se asigna como `"mysql://localhost:3306/midb"` solo en la primera inicializacion.
4. El mensaje `"Conexion a BD creada: ..."` se imprime exactamente **una vez**, sin importar cuantas instancias se soliciten.
5. Tras la primera inicializacion, `_initialized` se establece en `True` y llamadas posteriores a `__init__()` no tienen efecto.

**Datos Tecnicos:**

| Elemento | Detalle |
|----------|---------|
| Flag de control | `_initialized` (atributo de instancia) |
| Atributo protegido | `_connection_string` (privado con `_`) |
| Lineas de codigo | `database_connection.py:51-61` |

**Definicion de Hecho:**
- [x] Flag `_initialized` controla la inicializacion unica.
- [x] `_connection_string` es privado (convencion `_`).
- [x] Mensaje de creacion aparece solo una vez.

---

### HU-003: Acceder a la conexion mediante punto de acceso global

**Como** desarrollador del sistema,
**quiero** obtener la instancia de conexion a traves de un metodo estatico `get_instance()`,
**para** acceder a la conexion desde cualquier modulo sin necesidad de instanciar directamente la clase.

**Criterios de Aceptacion:**

1. El metodo `get_instance()` esta decorado con `@staticmethod`.
2. Internamente, `get_instance()` delega a `DatabaseConnection()`, que activa el mecanismo `__new__()` del Singleton.
3. No hay logica duplicada: `get_instance()` simplemente retorna `DatabaseConnection()`.
4. Es accesible globalmente mediante `DatabaseConnection.get_instance()`.
5. Llamadas consecutivas siempre retornan la misma instancia.

**Datos Tecnicos:**

| Elemento | Detalle |
|----------|---------|
| Metodo | `get_instance()` (estatico) |
| Implementacion | `return DatabaseConnection()` |
| Lineas de codigo | `database_connection.py:63-73` |

**Definicion de Hecho:**
- [x] Metodo estatico implementado.
- [x] Delega a `__new__()` sin duplicar logica.
- [x] Retorna siempre la misma instancia.

---

### HU-004: Ejecutar consultas SQL sobre la conexion unica

**Como** desarrollador del sistema,
**quiero** ejecutar consultas SQL a traves del metodo `query()` de la conexion Singleton,
**para** simular operaciones de base de datos asegurando que siempre usen la misma conexion.

**Criterios de Aceptacion:**

1. El metodo `query(sql)` recibe un parametro `sql` de tipo `str`.
2. Imprime en consola: `"Ejecutando query: {sql}"`.
3. Se invoca sobre la instancia obtenida con `get_instance()`.
4. La consulta se ejecuta sobre la misma conexion Singleton.

**Datos Tecnicos:**

| Elemento | Detalle |
|----------|---------|
| Metodo | `query(self, sql)` |
| Salida esperada | `Ejecutando query: SELECT * FROM usuarios` |
| Lineas de codigo | `database_connection.py:75-81` |

**Definicion de Hecho:**
- [x] Metodo funcional con salida por consola.
- [x] Comprobado con al menos una consulta de ejemplo.

---

## EPICA 2: Catalogo de Productos (Patron Factory)

> **Objetivo:** Centralizar la creacion de diferentes tipos de productos mediante una fabrica, desacoplando el codigo cliente de las clases concretas.
>
> **Patron aplicado:** Factory Method
>
> **Archivos involucrados:** `patrones/producto.py`, `patrones/producto_factory.py`

---

### HU-005: Definir interfaz comun para todos los productos

**Como** desarrollador del sistema,
**quiero** que exista una clase abstracta `Producto` que defina la estructura base de todos los productos,
**para** garantizar que cualquier tipo de producto comparta una interfaz comun y que las subclases implementen sus propios comportamientos obligatoriamente.

**Criterios de Aceptacion:**

1. La clase `Producto` hereda de `ABC` (modulo `abc`).
2. Posee atributos privados `_nombre` (str) y `_precio` (float) inicializados en `__init__()`.
3. Declara el metodo abstracto `mostrar_info()` decorado con `@abstractmethod`.
4. Provee metodos de acceso `get_nombre()` y `get_precio()` que retornan los valores correspondientes.
5. Intentar instanciar `Producto()` directamente lanza `TypeError`.

**Datos Tecnicos:**

| Elemento | Detalle |
|----------|---------|
| Clase | `Producto(ABC)` |
| Atributos | `_nombre`, `_precio` |
| Metodo abstracto | `mostrar_info()` |
| Getters | `get_nombre()`, `get_precio()` |
| Lineas de codigo | `producto.py:26-62` |

**Definicion de Hecho:**
- [x] Clase abstracta con ABC y `@abstractmethod`.
- [x] Instanciacion directa lanza `TypeError`.
- [x] Getters retornan valores correctos en subclases.

---

### HU-006: Registrar productos de tipo Libro

**Como** comprador en la tienda en linea,
**quiero** que el sistema soporte productos de tipo Libro con titulo, precio y autor,
**para** disponer de un catalogo de libros con toda su informacion relevante.

**Criterios de Aceptacion:**

1. La clase `Libro` hereda de `Producto`.
2. El constructor recibe `nombre`, `precio` y `autor`, invocando `super().__init__(nombre, precio)`.
3. El atributo `_autor` almacena el nombre del autor.
4. `mostrar_info()` imprime: `"Libro: {nombre} | Autor: {autor} | Precio: ${precio}"`.
5. Los getters heredados `get_nombre()` y `get_precio()` funcionan correctamente.

**Datos Tecnicos:**

| Elemento | Detalle |
|----------|---------|
| Clase | `Libro(Producto)` |
| Atributo adicional | `_autor` (str) |
| Salida de `mostrar_info()` | `Libro: Cien Anos de Soledad \| Autor: Garcia Marquez \| Precio: $25.99` |
| Lineas de codigo | `producto.py:65-88` |

**Definicion de Hecho:**
- [x] Herencia correcta con `super().__init__()`.
- [x] `mostrar_info()` produce el formato exacto.
- [x] Getters heredados funcionan.

---

### HU-007: Registrar productos de tipo Electronico

**Como** comprador en la tienda en linea,
**quiero** que el sistema soporte productos electronicos con nombre, precio y garantia en meses,
**para** conocer la cobertura de garantia de cada dispositivo antes de comprarlo.

**Criterios de Aceptacion:**

1. La clase `Electronico` hereda de `Producto`.
2. El constructor recibe `nombre`, `precio` y `garantia_meses`, invocando `super().__init__(nombre, precio)`.
3. El atributo `_garantia_meses` almacena la duracion de la garantia como entero.
4. `mostrar_info()` imprime: `"Electronico: {nombre} | Garantia: {garantia_meses} meses | Precio: ${precio}"`.
5. Se soportan valores como 12 o 24 meses.

**Datos Tecnicos:**

| Elemento | Detalle |
|----------|---------|
| Clase | `Electronico(Producto)` |
| Atributo adicional | `_garantia_meses` (int) |
| Salida de `mostrar_info()` | `Electronico: Laptop HP \| Garantia: 24 meses \| Precio: $899.99` |
| Lineas de codigo | `producto.py:91-114` |

**Definicion de Hecho:**
- [x] Herencia correcta con `super().__init__()`.
- [x] `mostrar_info()` produce el formato exacto.
- [x] Garantia se muestra en meses.

---

### HU-008: Crear productos mediante fabrica centralizada

**Como** desarrollador del sistema,
**quiero** crear productos a traves de metodos estaticos en `ProductoFactory` sin importar las clases concretas,
**para** centralizar la logica de creacion, facilitar el mantenimiento y permitir agregar nuevos tipos de producto en el futuro modificando solo la fabrica.

**Criterios de Aceptacion:**

1. `ProductoFactory` ofrece tres metodos estaticos (`@staticmethod`):
   - `crear_libro(nombre, precio, autor)` → retorna instancia de `Libro`.
   - `crear_electronico(nombre, precio, garantia)` → retorna instancia de `Electronico`.
   - `crear_producto(tipo, nombre, precio)` → crea por tipo generico (string).
2. El metodo generico acepta `"libro"` o `"electronico"` sin distinguir mayusculas (usa `.lower()`).
3. Cuando el tipo es `"libro"`, asigna `"Autor Desconocido"` como autor por defecto.
4. Cuando el tipo es `"electronico"`, asigna `12` meses de garantia por defecto.
5. Si el tipo no es valido, lanza `ValueError` con mensaje: `"Tipo de producto no valido: {tipo}"`.

**Datos Tecnicos:**

| Elemento | Detalle |
|----------|---------|
| Clase | `ProductoFactory` |
| Metodos | `crear_producto()`, `crear_libro()`, `crear_electronico()` |
| Excepcion | `ValueError` para tipos invalidos |
| Lineas de codigo | `producto_factory.py:24-85` |

**Definicion de Hecho:**
- [x] Los tres metodos de fabrica crean instancias validas.
- [x] `crear_producto("LIBRO", ...)` funciona (case-insensitive).
- [x] Tipo invalido genera `ValueError` con mensaje descriptivo.

---

## EPICA 3: Sistema de Notificaciones (Patron Observer)

> **Objetivo:** Implementar un mecanismo de suscripcion/publicacion donde la tienda notifique automaticamente a todos los clientes suscritos sobre nuevas ofertas.
>
> **Patron aplicado:** Observer (Publicador/Suscriptor)
>
> **Archivos involucrados:** `patrones/observer.py`, `patrones/tienda.py`

---

### HU-009: Definir contrato para observadores

**Como** desarrollador del sistema,
**quiero** que exista una interfaz abstracta `Observer` con el metodo `actualizar(mensaje)`,
**para** establecer un contrato estandar que cualquier tipo de suscriptor debe cumplir, asegurando extensibilidad.

**Criterios de Aceptacion:**

1. La clase `Observer` hereda de `ABC`.
2. Declara el metodo abstracto `actualizar(self, mensaje)` con `@abstractmethod`.
3. No es posible instanciar `Observer` directamente (lanza `TypeError`).
4. Cualquier clase que herede de `Observer` debe implementar `actualizar()`.

**Datos Tecnicos:**

| Elemento | Detalle |
|----------|---------|
| Clase | `Observer(ABC)` |
| Metodo abstracto | `actualizar(self, mensaje)` |
| Lineas de codigo | `observer.py:26-40` |

**Definicion de Hecho:**
- [x] Interfaz abstracta implementada.
- [x] Instanciacion directa lanza `TypeError`.

---

### HU-010: Crear clientes que reciben notificaciones

**Como** cliente de la tienda en linea,
**quiero** registrarme como observador con mi nombre y recibir notificaciones personalizadas,
**para** estar informado de las ofertas que me interesan.

**Criterios de Aceptacion:**

1. La clase `Cliente` hereda de `Observer` e implementa `actualizar(mensaje)`.
2. El constructor recibe `nombre` y lo almacena en `_nombre`.
3. Al recibir notificacion, imprime: `"Cliente {nombre} recibio notificacion: {mensaje}"`.
4. Provee `get_nombre()` que retorna el nombre del cliente.
5. Cada cliente muestra su propio nombre diferenciado en la notificacion.

**Datos Tecnicos:**

| Elemento | Detalle |
|----------|---------|
| Clase | `Cliente(Observer)` |
| Atributo | `_nombre` (str) |
| Salida | `Cliente Juan Perez recibio notificacion: Nueva oferta: 50% descuento` |
| Lineas de codigo | `observer.py:43-71` |

**Definicion de Hecho:**
- [x] Implementa `actualizar()` con nombre personalizado.
- [x] Getter funcional.

---

### HU-011: Suscribir clientes a la tienda con validaciones

**Como** administrador de la tienda,
**quiero** que los clientes puedan suscribirse al sistema de notificaciones con validacion de tipo y sin duplicados,
**para** mantener una lista de suscriptores limpia y evitar errores en tiempo de notificacion.

**Criterios de Aceptacion:**

1. La clase `Tienda` mantiene una lista `_clientes` y un nombre `_nombre`.
2. El metodo `suscribir(cliente)` valida que el objeto sea instancia de `Observer` con `isinstance()`.
3. Si el objeto **no es** `Observer`, lanza `TypeError` con mensaje: `"El objeto debe ser una instancia de Observer"`.
4. Si el cliente **ya esta suscrito**, imprime `"Cliente ya esta suscrito a la tienda {nombre}"` y no lo agrega de nuevo.
5. Si pasa ambas validaciones, agrega al cliente e imprime `"Cliente suscrito a la tienda {nombre}"`.

**Datos Tecnicos:**

| Elemento | Detalle |
|----------|---------|
| Clase | `Tienda` |
| Metodo | `suscribir(self, cliente)` |
| Validacion 1 | `isinstance(cliente, Observer)` → `TypeError` |
| Validacion 2 | `cliente in self._clientes` → rechazo silencioso |
| Lineas de codigo | `tienda.py:47-66` |

**Definicion de Hecho:**
- [x] Valida tipo `Observer` (lanza `TypeError` si no).
- [x] Rechaza duplicados con mensaje informativo.
- [x] Suscripcion exitosa muestra confirmacion.

---

### HU-012: Desuscribir clientes de la tienda de forma segura

**Como** cliente suscrito,
**quiero** poder cancelar mi suscripcion a las notificaciones sin que el sistema falle,
**para** dejar de recibir alertas cuando ya no me interesen las ofertas.

**Criterios de Aceptacion:**

1. El metodo `desuscribir(cliente)` verifica que el cliente exista en `_clientes` antes de eliminarlo.
2. Si el cliente **no esta suscrito**, imprime `"Cliente no esta suscrito a la tienda {nombre}"` y no lanza excepcion.
3. Si el cliente **esta suscrito**, lo elimina con `list.remove()` e imprime `"Cliente desuscrito de la tienda {nombre}"`.
4. Tras desuscribirse, el cliente **no recibe** notificaciones posteriores.
5. Los demas suscriptores no se ven afectados.

**Datos Tecnicos:**

| Elemento | Detalle |
|----------|---------|
| Metodo | `desuscribir(self, cliente)` |
| Verificacion | `if cliente not in self._clientes` |
| Lineas de codigo | `tienda.py:68-81` |

**Definicion de Hecho:**
- [x] No lanza `ValueError` al desuscribir un cliente no suscrito.
- [x] Cliente desuscrito no recibe mas notificaciones.
- [x] Otros suscriptores no se ven afectados.

---

### HU-013: Publicar ofertas y notificar automaticamente a suscriptores

**Como** administrador de la tienda,
**quiero** publicar una nueva oferta y que todos los clientes suscritos sean notificados automaticamente,
**para** maximizar el alcance de las promociones sin contactar a cada cliente individualmente.

**Criterios de Aceptacion:**

1. El metodo `nueva_oferta(descripcion)` imprime `"!Nueva oferta en {nombre_tienda}!"`.
2. Internamente invoca `notificar_clientes()` con el mensaje formateado.
3. `notificar_clientes(mensaje)` imprime `"--- Notificando a {N} clientes ---"` mostrando la cantidad exacta.
4. Itera sobre `_clientes` y llama a `actualizar(mensaje)` en cada observador.
5. Si hay 3 suscritos, los 3 reciben la notificacion. Si uno se desuscribio, solo 2 la reciben.
6. El conteo `{N}` refleja correctamente la cantidad actual de suscriptores.

**Datos Tecnicos:**

| Elemento | Detalle |
|----------|---------|
| Metodo publico | `nueva_oferta(self, descripcion)` |
| Metodo interno | `notificar_clientes(self, mensaje)` |
| Iteracion | `for cliente in self._clientes: cliente.actualizar(mensaje)` |
| Lineas de codigo | `tienda.py:83-106` |

**Definicion de Hecho:**
- [x] Todos los suscritos reciben la notificacion.
- [x] Conteo de clientes notificados es correcto.
- [x] Desuscritos no reciben la notificacion.

---

## EPICA 4: Carrito de Compras y Metodos de Pago (Patron Strategy)

> **Objetivo:** Permitir que los compradores agreguen productos a un carrito y seleccionen dinamicamente entre diferentes metodos de pago al momento del checkout, sin que el carrito conozca los detalles internos de cada metodo.
>
> **Patron aplicado:** Strategy
>
> **Archivos involucrados:** `patrones/estrategia_pago.py`, `patrones/carrito_compra.py`

---

### HU-014: Definir interfaz de estrategia de pago

**Como** desarrollador del sistema,
**quiero** una interfaz abstracta `EstrategiaPago` que defina el contrato para todos los metodos de pago,
**para** poder agregar nuevas formas de pago en el futuro sin modificar el carrito ni el flujo de checkout.

**Criterios de Aceptacion:**

1. `EstrategiaPago` hereda de `ABC`.
2. Declara el metodo abstracto `pagar(self, monto)` con `@abstractmethod`.
3. No es posible instanciar `EstrategiaPago` directamente.
4. Toda nueva estrategia debe implementar `pagar(monto)`.

**Datos Tecnicos:**

| Elemento | Detalle |
|----------|---------|
| Clase | `EstrategiaPago(ABC)` |
| Metodo abstracto | `pagar(self, monto)` |
| Lineas de codigo | `estrategia_pago.py:28-43` |

**Definicion de Hecho:**
- [x] Interfaz abstracta implementada.
- [x] Instanciacion directa lanza `TypeError`.

---

### HU-015: Pagar con tarjeta mostrando solo los ultimos 4 digitos

**Como** comprador en la tienda en linea,
**quiero** pagar con tarjeta de credito/debito y que el sistema solo muestre los ultimos 4 digitos,
**para** realizar transacciones electronicas sin exponer mi numero completo de tarjeta.

**Criterios de Aceptacion:**

1. `PagoTarjeta` hereda de `EstrategiaPago` e implementa `pagar(monto)`.
2. El constructor recibe `numero_tarjeta` y lo almacena en `_numero_tarjeta`.
3. Al procesar el pago, extrae los ultimos 4 digitos con `self._numero_tarjeta[-4:]`.
4. Imprime: `"Pagando ${monto} con tarjeta terminada en {ultimos_4_digitos}"`.
5. **Nunca** muestra el numero completo de la tarjeta.

**Datos Tecnicos:**

| Elemento | Detalle |
|----------|---------|
| Clase | `PagoTarjeta(EstrategiaPago)` |
| Atributo | `_numero_tarjeta` (str) |
| Seguridad | Slicing `[-4:]` para ocultar datos sensibles |
| Salida | `Pagando $925.98 con tarjeta terminada en 9012` |
| Lineas de codigo | `estrategia_pago.py:46-71` |

**Definicion de Hecho:**
- [x] Solo muestra ultimos 4 digitos.
- [x] Monto con simbolo `$`.

---

### HU-016: Pagar en efectivo con descuento automatico del 5%

**Como** comprador en la tienda en linea,
**quiero** pagar en efectivo y recibir automaticamente un descuento del 5%,
**para** obtener un beneficio economico por elegir este metodo de pago.

**Criterios de Aceptacion:**

1. `PagoEfectivo` hereda de `EstrategiaPago` e implementa `pagar(monto)`.
2. No requiere parametros de constructor.
3. Calcula el descuento como `round(monto * 0.95, 2)` usando `round()` para precision monetaria.
4. Imprime el monto original: `"Pagando ${monto} en efectivo. Se aplico 5% descuento."`.
5. Imprime el total final: `"Total a pagar: ${total_con_descuento}"`.
6. El total muestra exactamente 2 decimales (no 3 como `$968.981`).

**Datos Tecnicos:**

| Elemento | Detalle |
|----------|---------|
| Clase | `PagoEfectivo(EstrategiaPago)` |
| Calculo | `round(monto * 0.95, 2)` |
| Precision | `round()` evita errores de punto flotante |
| Salida ejemplo | `Total a pagar: $968.98` (no `$968.981`) |
| Lineas de codigo | `estrategia_pago.py:74-90` |

**Definicion de Hecho:**
- [x] Descuento del 5% calculado correctamente.
- [x] `round()` aplicado para precision monetaria.
- [x] Muestra monto original y total con descuento.

---

### HU-017: Pagar con PayPal usando correo electronico

**Como** comprador en la tienda en linea,
**quiero** pagar a traves de PayPal usando mi correo electronico,
**para** realizar pagos digitales rapidos sin compartir datos de mi tarjeta.

**Criterios de Aceptacion:**

1. `PagoPayPal` hereda de `EstrategiaPago` e implementa `pagar(monto)`.
2. El constructor recibe `email` y lo almacena en `_email`.
3. Imprime: `"Pagando ${monto} con PayPal desde la cuenta: {email}"`.
4. El email completo se muestra en la confirmacion de pago.

**Datos Tecnicos:**

| Elemento | Detalle |
|----------|---------|
| Clase | `PagoPayPal(EstrategiaPago)` |
| Atributo | `_email` (str) |
| Salida | `Pagando $1899.98 con PayPal desde la cuenta: usuario@email.com` |
| Lineas de codigo | `estrategia_pago.py:93-117` |

**Definicion de Hecho:**
- [x] Email se muestra correctamente.
- [x] Monto con simbolo `$`.

---

### HU-018: Agregar productos al carrito de compras

**Como** comprador en la tienda en linea,
**quiero** agregar productos de cualquier tipo a mi carrito,
**para** acumular los articulos que deseo comprar antes de pagar.

**Criterios de Aceptacion:**

1. `CarritoCompra` se inicializa con `_productos = []` y `_estrategia_pago = None`.
2. El metodo `agregar_producto(producto)` anade el producto a la lista.
3. Imprime: `"Producto agregado al carrito: {nombre}"` usando `producto.get_nombre()`.
4. Acepta cualquier objeto que implemente la interfaz `Producto` (Libro, Electronico).
5. Se pueden agregar multiples productos al mismo carrito.

**Datos Tecnicos:**

| Elemento | Detalle |
|----------|---------|
| Clase | `CarritoCompra` |
| Metodo | `agregar_producto(self, producto)` |
| Estructura interna | `self._productos` (list) |
| Lineas de codigo | `carrito_compra.py:39-51` |

**Definicion de Hecho:**
- [x] Productos de distintos tipos se agregan correctamente.
- [x] Mensaje de confirmacion por cada producto.

---

### HU-019: Seleccionar metodo de pago dinamicamente

**Como** comprador en la tienda en linea,
**quiero** elegir o cambiar mi metodo de pago en cualquier momento antes del checkout,
**para** tener flexibilidad en como pago sin necesidad de crear un nuevo carrito.

**Criterios de Aceptacion:**

1. El metodo `set_estrategia_pago(estrategia_pago)` establece la estrategia activa.
2. Se puede cambiar la estrategia en cualquier momento antes de `checkout()`.
3. La estrategia se almacena en `_estrategia_pago`.
4. Acepta cualquier objeto que herede de `EstrategiaPago`.
5. El checkout usa la ultima estrategia configurada.

**Datos Tecnicos:**

| Elemento | Detalle |
|----------|---------|
| Metodo | `set_estrategia_pago(self, estrategia_pago)` |
| Principio | Inyeccion de dependencia en tiempo de ejecucion |
| Lineas de codigo | `carrito_compra.py:53-63` |

**Definicion de Hecho:**
- [x] Estrategia se puede establecer y cambiar.
- [x] Checkout usa la ultima estrategia configurada.

---

### HU-020: Calcular el total del carrito automaticamente

**Como** comprador en la tienda en linea,
**quiero** que el sistema calcule automaticamente el total de mis productos,
**para** conocer el monto exacto antes de confirmar la compra.

**Criterios de Aceptacion:**

1. El metodo `calcular_total()` itera sobre `_productos`.
2. Suma los precios usando `producto.get_precio()` de cada producto.
3. Retorna el total como valor numerico (`float`).
4. Con carrito vacio retorna `0`.
5. Funciona correctamente con 1 o multiples productos.

**Datos Tecnicos:**

| Elemento | Detalle |
|----------|---------|
| Metodo | `calcular_total(self)` |
| Retorno | `float` |
| Lineas de codigo | `carrito_compra.py:65-74` |

**Definicion de Hecho:**
- [x] Calculo preciso para cualquier combinacion.
- [x] Carrito vacio retorna 0.

---

### HU-021: Realizar checkout con resumen, pago y vaciado del carrito

**Como** comprador en la tienda en linea,
**quiero** finalizar mi compra con un checkout que muestre el resumen, procese el pago y vcie el carrito,
**para** completar mi compra de forma clara y que el carrito quede listo para una nueva compra.

**Criterios de Aceptacion:**

1. **Validacion 1:** Si `_productos` esta vacio, imprime `"El carrito esta vacio"` y termina.
2. **Validacion 2:** Si `_estrategia_pago` es `None`, imprime `"Debe seleccionar un metodo de pago"` y termina.
3. Muestra encabezado `"=== CHECKOUT ==="`.
4. Lista todos los productos invocando `mostrar_info()` de cada uno.
5. Muestra `"Total: ${total}"` calculado con `calcular_total()`.
6. Delega el pago a `self._estrategia_pago.pagar(total)`.
7. Imprime `"!Compra completada!"`.
8. **Tras el checkout exitoso:** vacia `_productos = []` y resetea `_estrategia_pago = None`.
9. El carrito queda listo para una nueva compra sin residuos de la anterior.

**Datos Tecnicos:**

| Elemento | Detalle |
|----------|---------|
| Metodo | `checkout(self)` |
| Validaciones | Carrito vacio + metodo de pago no seleccionado |
| Post-checkout | Vaciado de `_productos` y `_estrategia_pago` |
| Lineas de codigo | `carrito_compra.py:76-106` |

**Definicion de Hecho:**
- [x] Ambas validaciones funcionan.
- [x] Resumen completo con productos y total.
- [x] Pago delegado a la estrategia.
- [x] Carrito se vacia despues del checkout.

---

## EPICA 5: Demostracion Integral del Sistema

> **Objetivo:** Integrar todos los patrones en un programa principal ejecutable que demuestre el funcionamiento completo del sistema de e-commerce.
>
> **Archivo involucrado:** `main.py`

---

### HU-022: Ejecutar demostracion completa de todos los patrones

**Como** estudiante o evaluador del sistema,
**quiero** ejecutar un unico archivo `main.py` que demuestre los 4 patrones en secuencia,
**para** observar el funcionamiento integral del sistema y comprender cada patron en un contexto practico.

**Criterios de Aceptacion:**

1. Se ejecuta con `python main.py` sin errores ni excepciones.
2. Muestra encabezado: `"DEMOSTRACION DE PATRONES DE DISENO EN PYTHON"`.
3. **Seccion Singleton:** Crea dos instancias, verifica `db1 is db2 == True`, ejecuta una query.
4. **Seccion Factory:** Crea 2 libros y 2 electronicos via `ProductoFactory`, muestra info de cada uno.
5. **Seccion Observer:** Crea tienda + 3 clientes, suscribe los 3, envia oferta (3 notificados), desuscribe uno, envia otra oferta (2 notificados).
6. **Seccion Strategy:** 3 carritos con diferentes metodos de pago (tarjeta, efectivo con descuento, PayPal), cada uno ejecuta checkout completo.
7. Muestra pie de cierre: `"FIN DE LA DEMOSTRACION"`.
8. No requiere dependencias externas. Compatible con Python 3.6+.

**Datos Tecnicos:**

| Elemento | Detalle |
|----------|---------|
| Archivo | `main.py` |
| Ejecucion | `python main.py` |
| Secciones | 4 (Singleton, Factory, Observer, Strategy) |
| Dependencias | Solo biblioteca estandar de Python |
| Lineas de codigo | `main.py:1-133` |

**Definicion de Hecho:**
- [x] Ejecucion completa sin errores.
- [x] Las 4 secciones se ejecutan en orden.
- [x] Salida organizada y legible.

---

## Matriz de Trazabilidad

### Historias de Usuario por Archivo

| Archivo | Historias Relacionadas |
|---------|----------------------|
| `patrones/database_connection.py` | HU-001, HU-002, HU-003, HU-004 |
| `patrones/producto.py` | HU-005, HU-006, HU-007 |
| `patrones/producto_factory.py` | HU-008 |
| `patrones/observer.py` | HU-009, HU-010 |
| `patrones/tienda.py` | HU-011, HU-012, HU-013 |
| `patrones/estrategia_pago.py` | HU-014, HU-015, HU-016, HU-017 |
| `patrones/carrito_compra.py` | HU-018, HU-019, HU-020, HU-021 |
| `main.py` | HU-022 |

### Historias de Usuario por Patron

| Patron | Epica | Historias | Cantidad |
|--------|-------|-----------|----------|
| Singleton | Epica 1 | HU-001 a HU-004 | 4 |
| Factory | Epica 2 | HU-005 a HU-008 | 4 |
| Observer | Epica 3 | HU-009 a HU-013 | 5 |
| Strategy | Epica 4 | HU-014 a HU-021 | 8 |
| Todos | Epica 5 | HU-022 | 1 |
| **Total** | | | **22** |

### Historias por Rol

| Rol | Historias | Cantidad |
|-----|-----------|----------|
| Desarrollador | HU-001, HU-002, HU-003, HU-004, HU-005, HU-008, HU-009, HU-014 | 8 |
| Comprador | HU-006, HU-007, HU-015, HU-016, HU-017, HU-018, HU-019, HU-020, HU-021 | 9 |
| Administrador de tienda | HU-011, HU-013 | 2 |
| Cliente suscrito | HU-010, HU-012 | 2 |
| Estudiante/Evaluador | HU-022 | 1 |

---

*Documento basado en el analisis profundo del codigo fuente corregido y documentado.*
*Cada criterio de aceptacion esta verificado contra la implementacion actual y marcado como cumplido.*
