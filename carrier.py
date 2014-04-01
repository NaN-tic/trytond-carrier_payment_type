# This file is part of the carrier_payment_type module for Tryton.
# The COPYRIGHT file at the top level of this repository contains the full
# copyright notices and license terms.
import tokenize
from StringIO import StringIO

from trytond.model import ModelView, ModelSQL, fields
from trytond.pool import PoolMeta
from trytond.transaction import Transaction
from trytond.pyson import Eval
from trytond.tools import safe_eval

__all__ = ['CarrierPaymentType', 'Carrier']
__metaclass__ = PoolMeta

# code snippet taken from http://docs.python.org/library/tokenize.html
def decistmt(s):
    """Substitute Decimals for floats in a string of statements.

    >>> from decimal import Decimal
    >>> s = 'print +21.3e-5*-.1234/81.7'
    >>> decistmt(s)
    "print +Decimal ('21.3e-5')*-Decimal ('.1234')/Decimal ('81.7')"

    >>> exec(s)
    -3.21716034272e-007
    >>> exec(decistmt(s))
    -3.217160342717258261933904529E-7
    """
    result = []
    # tokenize the string
    g = tokenize.generate_tokens(StringIO(s).readline)
    for toknum, tokval, _, _, _ in g:
        # replace NUMBER tokens
        if toknum == tokenize.NUMBER and '.' in tokval:
            result.extend([
                (tokenize.NAME, 'Decimal'),
                (tokenize.OP, '('),
                (tokenize.STRING, repr(tokval)),
                (tokenize.OP, ')')
            ])
        else:
            result.append((toknum, tokval))
    return tokenize.untokenize(result)


class CarrierPaymentType(ModelSQL, ModelView):
    'Carrier Payment Type'
    __name__ = 'carrier.payment.type'
    payment_type = fields.Many2One('account.payment.type', 'Payment Type',
            required=True)
    carrier = fields.Many2One('carrier', 'Carrier', required=True)
    sum_carrier_price = fields.Boolean('Sum Carrier Price')
    operation = fields.Selection([
            ('percentage', 'Percentage (%)'),
            ('sum', 'Sum (+)'),
            ('formula', 'Formula'),
            ], 'Operation')
    value = fields.Numeric('Value', digits=(16, 2),
            states={
                'invisible': Eval('operation') == 'formula',
                'required': Eval('operation') != 'formula',
            })
    formula = fields.Char('Formula', states={
                'invisible': Eval('operation') != 'formula',
                'required': Eval('operation') == 'formula',
            }, help=('Python expression that will be evaluated and sum. Eg:\n'
            '0.10*(record.untaxed_amount)'))

    @staticmethod
    def default_sum_carrier_price():
        return True

    @staticmethod
    def default_operation():
        return 'percentage'


class Carrier:
    __name__ = 'carrier'
    payment_types = fields.One2Many('carrier.payment.type', 'carrier',
        'Payment Types')

    @classmethod
    def __setup__(cls):
        super(Carrier, cls).__setup__()
        cls._error_messages.update({
                'error_formula': ('Invalid carrier payment type formula '
                    '"%s".'),
                })

    def get_sale_price(self):
        price, currency_id = super(Carrier, self).get_sale_price()
        record = Transaction().context.get('record', None)
        if record:
            price_payment = 0
            for payment_type in record.carrier.payment_types:
                if record.payment_type == payment_type.payment_type:
                    if payment_type.operation == 'sum':
                        price_payment = payment_type.value
                    elif payment_type.operation == 'formula':
                        try:
                            price_payment = safe_eval(decistmt(payment_type.formula), Transaction().context)
                        except:
                            self.raise_user_error('error_formula', (payment_type.formula,))
                    else:
                        price_payment = price * (1 + payment_type.value / 100)

                    if payment_type.sum_carrier_price:
                        price += price_payment
                    else:
                        price = price_payment
                    break
        return price, currency_id

    def get_purchase_price(self):
        price, currency_id = super(Carrier, self).get_sale_price()
        record = Transaction().context.get('record', None)
        if record:
            price_payment = 0
            for payment_type in record.carrier.payment_types:
                if record.payment_type == payment_type.payment_type:
                    if payment_type.operation == 'sum':
                        price_payment = payment_type.value
                    elif payment_type.operation == 'formula':
                        try:
                            price_payment = safe_eval(decistmt(payment_type.formula), Transaction().context)
                        except:
                            self.raise_user_error('error_formula', (payment_type.formula,))
                    else:
                        price_payment = price * (1 + payment_type.value / 100)

                    if payment_type.sum_carrier_price:
                        price += price_payment
                    else:
                        price = price_payment
                    break
        return price, currency_id
