# This file is part of the carrier_payment_type module for Tryton.
# The COPYRIGHT file at the top level of this repository contains the full
# copyright notices and license terms.
from trytond.pool import Pool
from . import sale
from . import carrier

def register():
    Pool.register(
        sale.Sale,
        carrier.CarrierPaymentType,
        carrier.Carrier,
        module='carrier_payment_type', type_='model')
