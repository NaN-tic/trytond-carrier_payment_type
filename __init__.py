# This file is part of the carrier_payment_type module for Tryton.
# The COPYRIGHT file at the top level of this repository contains the full
# copyright notices and license terms.
from trytond.pool import Pool
from .sale import *
from .carrier import *

def register():
    Pool.register(
        Sale,
        CarrierPaymentType,
        Carrier,
        module='carrier_payment_type', type_='model')
