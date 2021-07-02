# This file is part of the carrier_payment_type module for Tryton.
# The COPYRIGHT file at the top level of this repository contains the full
# copyright notices and license terms.
from decimal import Decimal
from simpleeval import simple_eval
from trytond.model import ModelView, ModelSQL, fields
from trytond.pool import Pool, PoolMeta
from trytond.transaction import Transaction
from trytond.pyson import Eval
from trytond.config import config as config_
from trytond.tools import decistmt
from trytond.i18n import gettext
from trytond.exceptions import UserError

__all__ = ['CarrierPaymentType', 'Carrier']

DIGITS = config_.getint('product', 'price_decimal', default=4)


class CarrierPaymentType(ModelSQL, ModelView):
    'Carrier Payment Type'
    __name__ = 'carrier.payment.type'
    payment_type = fields.Many2One('account.payment.type', 'Payment Type',
            required=True)
    carrier = fields.Many2One('carrier', 'Carrier', required=True)
    sum_carrier_price = fields.Boolean('Sum Carrier Price')
    operation = fields.Selection([
            ('percentage', 'Percentage (%)'),
            ('fix', 'Fix'),
            ('formula', 'Formula'),
            ], 'Operation')
    value = fields.Numeric('Value', digits=(16, DIGITS),
            states={
                'invisible': Eval('operation') == 'formula',
                'required': Eval('operation') != 'formula',
            })
    formula = fields.Char('Formula', states={
                'invisible': Eval('operation') != 'formula',
                'required': Eval('operation') == 'formula',
            }, help=('Python expression that will be evaluated and sum. Eg:\n'
            '0.10 * getattr(record, "untaxed_amount")'))

    @staticmethod
    def default_sum_carrier_price():
        return True

    @staticmethod
    def default_operation():
        return 'percentage'


class Carrier(metaclass=PoolMeta):
    __name__ = 'carrier'
    payment_types = fields.One2Many('carrier.payment.type', 'carrier',
        'Payment Types')

    def compute_formula_payment_price(self, formula, record):
        "Compute price based on payment formula"
        context = self.get_context_formula(record)
        return simple_eval(decistmt(formula), **context) or Decimal(0)

    def get_sale_price(self):
        price, currency_id = super(Carrier, self).get_sale_price()
        record = Transaction().context.get('record', None)
        model = Transaction().context.get('record_model', None)

        if not record:
            return None, None

        # is an object that not saved (has not id)
        if isinstance(record, dict):
            if not model:
                return price, currency_id
            record = Pool().get(model)(**record)
        else:
            model, id = record.split(',')
            record = Pool().get(model)(id)

        if model == 'sale.sale':
            if not record.carrier:
                return price, currency_id

            price_payment = 0
            for payment_type in record.carrier.payment_types:
                if record.payment_type == payment_type.payment_type:
                    if payment_type.operation == 'fix':
                        price_payment = payment_type.value
                    elif payment_type.operation == 'formula':
                        try:
                            price_payment = self.compute_formula_payment_price(
                                    payment_type.formula, record)
                        except:
                            raise UserError(gettext(
                                'carrier_payment_type.rror_formula',
                                    formula=payment_type.formula))
                    else:
                        price_payment = price * (1 + payment_type.value / 100)

                    if payment_type.sum_carrier_price:
                        price += price_payment
                    else:
                        price = price_payment
                    break

        price = self.round_price_formula(price, self.formula_currency_digits)
        return price, currency_id

    def get_purchase_price(self):
        price, currency_id = super(Carrier, self).get_sale_price()
        record = Transaction().context.get('record', None)
        model = Transaction().context.get('record_model', None)

        if not record:
            return None, None

        # is an object that not saved (has not id)
        if isinstance(record, dict):
            if not model:
                return price, currency_id
            record = Pool().get(model)(**record)
        else:
            model, id = record.split(',')
            record = Pool().get(model)(id)

        if model == 'purchase.purchase':
            if not record.carrier:
                return price, currency_id

            price_payment = 0
            for payment_type in record.carrier.payment_types:
                if record.payment_type == payment_type.payment_type:
                    if payment_type.operation == 'fix':
                        price_payment = payment_type.value
                    elif payment_type.operation == 'formula':
                        try:
                            price_payment = self.compute_formula_payment_price(
                                    payment_type.formula, record)
                        except:
                            self.raise_user_error('error_formula', (
                                    payment_type.formula,))
                    else:
                        price_payment = price * (1 + payment_type.value / 100)

                    if payment_type.sum_carrier_price:
                        price += price_payment
                    else:
                        price = price_payment
                    break

        price = self.round_price_formula(price, self.formula_currency_digits)
        return price, currency_id
