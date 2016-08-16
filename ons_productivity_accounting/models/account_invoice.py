# -*- coding: utf-8 -*-
# © 2016 Coninckx David (Open Net Sarl)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import models, api

class account_invoice(models.Model):
    _inherit = 'account.invoice'

    @api.multi
    def unlink(self):
        for inv in self:
            if inv.state in ('draft', 'cancel'):
                self.write({'move_name': False})
    
        return super(account_invoice, self).unlink()
