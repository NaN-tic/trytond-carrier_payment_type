# This file is part of the carrier_payment_type module for Tryton.
# The COPYRIGHT file at the top level of this repository contains the full
# copyright notices and license terms.
import unittest
import trytond.tests.test_tryton
from trytond.tests.test_tryton import ModuleTestCase


class CarrierPaymentTypeTestCase(ModuleTestCase):
    'Test Carrier Payment Type module'
    module = 'carrier_payment_type'


def suite():
    suite = trytond.tests.test_tryton.suite()
    suite.addTests(unittest.TestLoader().loadTestsFromTestCase(
        CarrierPaymentTypeTestCase))
    return suite