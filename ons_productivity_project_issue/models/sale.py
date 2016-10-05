# -*- coding: utf-8 -*-
# © 2016 Coninckx David (Open Net Sarl)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import api, fields, models, _
import logging
#Get the logger
_logger = logging.getLogger(__name__)

class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    @api.multi
    def _compute_analytic(self, domain=None):
        lines = {}
        if not domain:
            # To filter on analyic lines linked to an expense
            domain = [('so_line', 'in', self.ids), ('amount', '<=', 0.0)]
        data = self.env['account.analytic.line'].read_group(
            domain,
            ['so_line', 'unit_amount', 'product_uom_id'], ['product_uom_id', 'so_line'], lazy=False
        )
        for d in data:
            if not d['product_uom_id']:
                continue
            line = self.browse(d['so_line'][0])
            lines.setdefault(line, 0.0)
            sub_lines = self.env['account.analytic.line'].search([
                ('so_line', '=', d['so_line'][0]),
                ('product_uom_id', '=', d['product_uom_id'][0])
            ])
            uom = self.env['product.uom'].browse(d['product_uom_id'][0])
            qty = 0.0
            for sub_line in sub_lines:
                if sub_line.ons_to_invoice:
                    if line.product_uom.category_id == uom.category_id:
                        qty += self.env['product.uom']._compute_qty_obj(uom, sub_line.unit_amount, line.product_uom)
                    else:
                        qty += sub_line.unit_amount
            lines[line] += qty
        for line, qty in lines.items(): 
            line.qty_delivered = qty
        return True
