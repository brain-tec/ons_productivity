# -*- coding: utf-8 -*-
# © 2016 Open Net Sarl
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp.exceptions import  Warning
from openerp import models, fields, api, _
from openerp.tools import float_compare


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    @api.multi
    def action_confirm(self):
        #Check if the current user is the teamleader of the sale
        if (self.team_id and self.team_id.user_id.id != self.env.uid):
            msg = _("You are not allowed to confirm a sale\nContact the team leader : ")+self.team_id.user_id.name
            raise Warning(msg)
        else:
            return super(SaleOrder, self).action_confirm()
