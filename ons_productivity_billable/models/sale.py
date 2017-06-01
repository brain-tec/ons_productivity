# -*- coding: utf-8 -*-
# Module: ons_productivity_billable
# © 2017 Open Net Sarl
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import api, fields, models, _
import openerp.addons.decimal_precision as dp
from openerp.tools import float_is_zero, float_compare

class SaleOrder(models.Model):
    _inherit = 'sale.order'

    amount_billable = fields.Monetary(string='Billable Amount', store=True, readonly=True, compute='_comp_amount_billable')
    fully_billable = fields.Boolean(string="Is fully billable ?", compute="_is_fully_billable", store=True)

    @api.depends('amount_billable')
    def _is_fully_billable(self):
        for order in self:
            order.fully_billable = (order.amount_billable == order.amount_total)

    @api.depends('order_line.qty_to_invoice')
    def _comp_amount_billable(self):
        precision = self.env['decimal.precision'].precision_get('Product Unit of Measure')
        down_product_id = self.env['ir.values'].get_default('sale.config.settings', 'deposit_product_id_setting')
        for order in self:
            billable = 0.0

            # Start by cumulating what should be invoiced
            for line in order.order_line.filtered(lambda l: not float_is_zero(l.qty_to_invoice, precision_digits=precision)):
                price = line.price_unit * (1 - (line.discount or 0.0) / 100.0)
                billable += line.qty_to_invoice * price
                billable += line.price_tax

            # Then, deduct what have already invoiced in advance
            for line in order.order_line.filtered(lambda l: l.product_id and l.product_id.id == down_product_id):
                billable -= line.qty_to_invoice * line.price_unit


            if billable < 0.0:
                billable = 0.0

            order.amount_billable = billable
