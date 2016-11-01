# -*- coding: utf-8 -*-
# © 2016 Coninckx David (Open Net Sarl)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import api, fields, models
import openerp.addons.decimal_precision as dp
import logging
_logger = logging.getLogger(__name__)

class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    @api.one
    def _set_uos(self):
        if self.product_id.uos_id and self.product_id.uos_coeff:
            self.product_uom_qty = self.product_uos_qty * self.product_id.uos_coeff
            self.product_uom = self.product_id.uom_id
        _logger.info("SET UOS")

    @api.one
    def _compute_uos(self):
        if self.product_id.uos_id and self.product_id.uos_coeff:
            self.product_uos_qty = self.product_uom_qty / self.product_id.uos_coeff
        # else:
        #     self.product_uos_qty = 1
        #     if product_id:
        #         self.product_uos = self.product_uom
        _logger.info("COMPUTE UOS")

    @api.onchange('product_uos_qty')
    def onchange_product_uos_qty(self):
        if self.product_id:
            self.product_uom_qty = self.product_uos_qty * self.product_id.uos_coeff
            _logger.info("ON CHANGE PRODUCT")

    product_uos_qty = fields.Float(string='Quantity', digits=dp.get_precision('Product Unit of Measure'),
                                    compute='_compute_uos', inverse='_set_uos', readonly=False, default=1)
    product_uos = fields.Many2one('product.uom', string='Unit of Measure', required=False,
                                  related='product_id.uos_id', readonly=False)