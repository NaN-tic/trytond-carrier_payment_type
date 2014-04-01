====================================================================
Transportista. Añadir porcentage o suma al coste de envío según pago
====================================================================

Según el tipo de pago del pedido de venta o compra, el precio del coste
de la entrega puede tener un incremento o decremento de precio en el precio
del envío.

Las operaciones permitidas son:

* Fijo.
* Porcentage. Un porcentaje del precio del coste de envío.
* Formula. Expressión Python con los datos del pedido: 0.10*(record.untaxed_amount)

El precio calculado según el tipo de pago se sumará o será fijo respeto el precio del transporte
si se marca la opción "Sumar precio transporte".
