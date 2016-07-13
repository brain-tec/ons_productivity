# -*- coding: utf-8 -*-
# © 2016 Coninckx David (Open Net Sarl)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import api, fields, models
import openerp.addons.decimal_precision as dp

class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    @api.one
    def _set_uos(self):
        if self.product_id.uos_coeff:
            self.product_uom_qty = self.product_uos_qty * self.product_id.uos_coeff
            self.product_uom = self.product_id.uom_id

    @api.one
    def _compute_uos(self):
        if self.product_id.uos_coeff != 0:
            self.product_uos_qty = self.product_uom_qty / self.product_id.uos_coeff

    @api.onchange('product_uos_qty')
    def onchange_product_uos_qty(self):
        if self.product_id:
            self.product_uom_qty = self.product_uos_qty * self.product_id.uos_coeff

    product_uos_qty = fields.Float(string='Quantity', digits=dp.get_precision('Product Unit of Measure'),
                                    compute='_compute_uos', inverse='_set_uos', readonly=False)
    product_uos = fields.Many2one('product.uom', string='Unit of Measure', required=True,
                                  related='product_id.uos_id', readonly=True)