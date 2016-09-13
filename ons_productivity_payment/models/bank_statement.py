# -*- coding: utf-8 -*-
# © 2016 Coninckx David (Open Net Sarl)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import models, api, fields

class bank_statement(models.Model):
    _inherit = 'account.bank.statement'

    payment_order_lines = fields.One2many('account.payment.line', 'bank_statement_id', string="Payment lines")

    @api.one
    @api.depends('line_ids', 'payment_order_lines','balance_start', 'line_ids.amount', 'balance_end_real')
    def _end_balance(self):
        super(bank_statement, self)._end_balance()
        total_payment_lines = sum([line.amount_currency for line in self.payment_order_lines])
        self.balance_end = self.balance_end - total_payment_lines
        self.difference = self.balance_end_real - self.balance_end

    @api.one
    def copy(self, default=None):
        rec = super(bank_statement, self).copy(default)
        rec['payment_order_lines'] = False
        return rec