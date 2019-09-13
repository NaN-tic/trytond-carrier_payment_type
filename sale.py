#This file is part carrier_formula module for Tryton.
#The COPYRIGHT file at the top level of this repository contains
#the full copyright notices and license terms.
from trytond.pool import PoolMeta

__all__ = ['Sale']


class Sale(metaclass=PoolMeta):
    __name__ = 'sale.sale'

    @classmethod
    def __setup__(cls):
        super(Sale, cls).__setup__()
        for fname in ('carrier', 'payment_type'):
            if fname not in cls.lines.on_change:
                cls.lines.on_change.add(fname)
        # TODO
        # for fname in cls.lines.on_change:
        #     if fname not in cls.carrier.on_change:
        #         cls.carrier.on_change.add(fname)

    def _get_carrier_context(self):
        context = super(Sale, self)._get_carrier_context()
        if self.carrier:
            context = context.copy()
            context['record'] = self
        return context
