# -*- coding: utf-8 -*-
# © 2016 Coninckx David (Open Net Sarl)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import fields, models, api

class sale_order(models.Model):
    _inherit = "sale.order"

    ons_prescripteur = fields.Many2one('res.partner', string="Presripteur")

    @api.multi
    @api.onchange('partner_id')
    def onchange_partner_id(self):
        res = super(sale_order, self).onchange_partner_id()
        for order in self:
            order.ons_prescripteur = order.partner_id.ons_prescripteur
        return res