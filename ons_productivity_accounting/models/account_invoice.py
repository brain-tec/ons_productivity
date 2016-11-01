# -*- coding: utf-8 -*-
#
#  File: models/invoices.py
#  Module: ons_productivity_accounting
#
#  dco@open-net.ch & cyp@open-net.ch
#
#  Copyright (c) 2016-TODAY Open-Net Ltd. All rights reserved.
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import models, fields, api

class AccountInvoice(models.Model):
    _inherit = 'account.invoice'

    authorize_same_ref = fields.Boolean(string='Authorize same ref', default=False)

    @api.multi
    def unlink(self):
        for inv in self:
            if inv.state in ('draft', 'cancel'):
                self.write({'move_name': False})
    
        return super(AccountInvoice, self).unlink()

    @api.multi
    def invoice_validate(self):
        for invoice in self:
            if not invoice.authorize_same_ref:
                return super(AccountInvoice, invoice).invoice_validate()
            invoice.write({'state': 'open'})

        return True

