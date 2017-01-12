# -*- coding: utf-8 -*-
# Copyright 2016 Open Net Sàrl
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import models, fields, api
import logging
#Get the logger
_logger = logging.getLogger(__name__)

class SaleConfiguration(models.TransientModel):
    _inherit = 'sale.config.settings'

    deposit_journal_id_setting = fields.Many2one('account.journal', string="Deposit Journal", domain=[('type', '=', 'sale')])
    deposit_payment_term_id_setting = fields.Many2one('account.payment.term', string="Deposit Payment Term")

    @api.multi
    def set_deposit_journal_id_setting(self):
        return self.env['ir.values'].sudo().set_default(
            'sale.config.settings', 'deposit_journal_id_setting', self.deposit_journal_id_setting.id)

    @api.multi
    def set_deposit_payment_term_id_setting(self):
        return self.env['ir.values'].sudo().set_default(
            'sale.config.settings', 'deposit_payment_term_id_setting', self.deposit_payment_term_id_setting.id)

class SaleAdvancePaymentInv(models.TransientModel):
    _inherit = "sale.advance.payment.inv"

    @api.onchange('advance_payment_method')
    def change_payment_method(self):
        for wizard in self:
            _logger.info("ON CHANGE %s" % self.env['ir.values'].get_default('sale.config.settings', 'deposit_journal_id_setting'))
            wizard.deposit_journal_id = self.env['ir.values'].get_default('sale.config.settings', 'deposit_journal_id_setting')
            wizard.deposit_payment_term_id = self.env['ir.values'].get_default('sale.config.settings', 'deposit_payment_term_id_setting')

    deposit_journal_id = fields.Many2one("account.journal", string="Income Journal")
    deposit_payment_term_id = fields.Many2one("account.payment.term", string="Deposit Payment Term")

    @api.multi
    def _create_invoice(self, order, so_line, amount):
        invoice = super(SaleAdvancePaymentInv, self)._create_invoice(order, so_line, amount)
        if self.advance_payment_method in ['percentage', 'fixed']:
            invoice.journal_id = self.deposit_journal_id
            invoice.payment_term_id = self.deposit_payment_term_id
        return invoice
