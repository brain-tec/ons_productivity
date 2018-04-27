# -*- coding: utf-8 -*-
# © 2018 Open Net Sarl
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models, fields, api

import logging
_logger = logging.getLogger(__name__)

class AccountInvoice(models.Model):
    _inherit = "account.invoice"
    
    @api.multi
    def action_invoice_open(self):
        res = super(AccountInvoice, self).action_invoice_open()
        for inv in self:
            if inv.l10n_ch_isr_number:
                inv.move_id.ref = inv.l10n_ch_isr_number
        return res