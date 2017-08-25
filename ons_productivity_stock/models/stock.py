# -*- coding: utf-8 -*-
#
#  File: models/product.py
#  Module: ons_productivity_stock
#
#  Created by cyp@open-net.ch
#
#  Copyright (c) 2017-TODAY Open Net Sàrl. <http://www.open-net.ch>

from odoo import models, fields, api, _
import odoo.addons.decimal_precision as dp


class StockMove(models.Model):
    _inherit = 'stock.move'

    onsp_hs_code = fields.Char(
        string="HS Code",
        related='product_id.categ_id.onsp_hs_code'
    )
    onsp_cat_eccn = fields.Char(
        string="ECCN",
        related='product_id.categ_id.onsp_eccn'
    )
    onsp_prod_eccn = fields.Char(
        string="ECCN",
        related='product_id.onsp_eccn'
    )
    price_total = fields.Monetary(
        string='Total',
        digits=dp.get_precision('Product Price'),
        currency_field = 'currency_id'
    )
    currency_id = fields.Many2one('res.currency', string='Currency')

    @api.model
    def create(self, vals):
        if vals.get('procurement_id'):
            proc = self.env['procurement.order'].browse(vals['procurement_id'])
            if proc and getattr(proc, 'sale_line_id'):
                vals.update({
                    'price_total': proc.sale_line_id.price_total,
                    'currency_id': proc.sale_line_id.currency_id.id or False
                })

        return super(StockMove, self).create(vals)
