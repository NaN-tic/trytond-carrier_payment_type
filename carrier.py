# This file is part of the carrier_payment_type module for Tryton.
# The COPYRIGHT file at the top level of this repository contains the full
# copyright notices and license terms.
from trytond.model import ModelView, ModelSQL, fields
from trytond.pool import PoolMeta
from trytond.transaction import Transaction

__all__ = ['CarrierPaymentType', 'Carrier']
__metaclass__ = PoolMeta


class CarrierPaymentType(ModelSQL, ModelView):
    'Carrier Payment Type'
    __name__ = 'carrier.payment.type'
    payment_type = fields.Many2One('account.payment.type', 'Payment Type',
            required=True)
    carrier = fields.Many2One('carrier', 'Carrier', required=True)
    operation = fields.Selection([
            ('percentage', 'Percentage (%)'),
            ('sum', 'Sum (+)'),
            ], 'Operation')
    value = fields.Numeric('Value', digits=(16, 2), required=True)

    @staticmethod
    def default_operation():
        return 'percentage'


class Carrier:
    __name__ = 'carrier'
    payment_types = fields.One2Many('carrier.payment.type', 'carrier',
        'Payment Types')

    def get_sale_price(self):
        price, currency_id = super(Carrier, self).get_sale_price()
        sale = Transaction().context.get('record', None)
        if sale:
            for payment_type in sale.carrier.payment_types:
                if sale.payment_type == payment_type.payment_type:
                    if payment_type.operation == 'sum':
                        price += payment_type.value
                    else:
                        price = price * (1 + payment_type.value / 100)

        return price, currency_id

    def get_purchase_price(self):
        price, currency_id = super(Carrier, self).get_sale_price()
        purchase = Transaction().context.get('record', None)
        if purchase:
            for payment_type in purchase.carrier.payment_types:
                if purchase.payment_type == payment_type.payment_type:
                    if payment_type.operation == 'sum':
                        price += payment_type.value
                    else:
                        price = price * (1 + payment_type.value / 100)
        return price, currency_id

