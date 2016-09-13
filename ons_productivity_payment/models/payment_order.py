# -*- coding: utf-8 -*-
# © 2016 Coninckx David (Open Net Sarl)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import models, api, fields

class payment_order(models.Model):
    _inherit = 'account.payment.order'

    @api.multi
    def _prepare_move(self, bank_lines=None):
        res = super(payment_order, self)._prepare_move(bank_lines)
        if bank_lines:
            res['date'] = bank_lines[0].date
        return res

class payment_order_line(models.Model):
    _inherit = 'account.payment.line'

    bank_statement_id = fields.Many2one('account.bank.statement', string="Bank statement")