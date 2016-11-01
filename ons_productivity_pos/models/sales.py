# -*- coding: utf-8 -*-
#
#  File: models/sales.py
#  Module: ons_productivity_pos
#
#  Created by cyp@open-net.ch
#
#  Copyright (c) 2015-TODAY Open-Net Ltd. All rights reserved.
##############################################################################
#    
# Part of Odoo. See LICENSE file for full copyright and licensing details.
#
##############################################################################


from openerp import models, fields, api


class AccountTax(models.Model):
    _inherit = 'account.tax'

    @api.model
    def _get_tax_included_price(self, price, prod_taxes, line_taxes):
        incl_tax = prod_taxes.filtered(lambda tax: tax not in line_taxes and tax.price_include)
        if incl_tax:
            return incl_tax.compute_all(price)['total_included']
        return price


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    # ---------- Interface management

    @api.multi
    @api.onchange('product_id')
    def product_id_change(self):
        res = super(SaleOrderLine, self).product_id_change()
        for line in self:
            if not line.product_id:
                continue

            if line.order_id.pricelist_id and line.order_id.partner_id:
                line.price_unit = self.env['account.tax']._get_tax_included_price(line.product_id.price, line.product_id.taxes_id, line.tax_id)
        
        return res

    @api.onchange('product_uom')
    def product_uom_change(self):
        res = super(SaleOrderLine, self).product_uom_change()
        for line in self:
            if not line.product_uom:
                continue

            if line.order_id.pricelist_id and line.order_id.partner_id:
                line.price_unit = self.env['account.tax']._get_tax_included_price(line.product_id.price, line.product_id.taxes_id, line.tax_id)
        
        return res
