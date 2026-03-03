# Subpaquete: Patrón Strategy
from patrones.strategy.estrategia_pago import (
    EstrategiaPago,
    PagoTarjeta,
    PagoEfectivo,
    PagoPayPal,
)
from patrones.strategy.carrito_compra import CarritoCompra

__all__ = [
    "EstrategiaPago",
    "PagoTarjeta",
    "PagoEfectivo",
    "PagoPayPal",
    "CarritoCompra",
]
