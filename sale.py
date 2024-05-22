#This file is part carrier_formula module for Tryton.
#The COPYRIGHT file at the top level of this repository contains
#the full copyright notices and license terms.
from trytond.pool import PoolMeta
from trytond.model import fields


class Sale(metaclass=PoolMeta):
    __name__ = 'sale.sale'

    @fields.depends('carrier', 'payment_type')
    def on_change_lines(self):
        super().on_change_lines()

    def _get_carrier_context(self, carrier):
        context = super(Sale, self)._get_carrier_context(carrier)
        carrier = carrier or self.carrier
        if carrier:
            context = context.copy()
            context['record'] = str(self)
        return context
