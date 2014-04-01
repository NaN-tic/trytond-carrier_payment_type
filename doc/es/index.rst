====================================================================
Transportista. Añadir porcentage o suma al coste de envío según pago
====================================================================

Según el tipo de pago del pedido de venta o compra, el precio del coste
de la entrega puede tener un incremento o decremento de precio en el precio
del envío.

Las operaciones permitidas son:

* Sumar. Sumar o restar un valor fijo.
* Porcentage. Sumar o restar un porcentaje del precio del coste de envío.
* Formula. Sumar o restar una operación con los datos del pedido: 0.10*(record.untaxed_amount)
