# -*- coding: utf-8 -*-
#
#  File: models/invoice.py
#  Module: ons_productivity_discount
#
#  Created by cyp@open-net.ch
#
#  Copyright (c) 2015-TODAY Open-Net Ltd. <http://www.open-net.ch>
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2004-TODAY OpenERP S.A. <http://www.openerp.com>
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

from openerp import models, fields, api, _
import openerp.addons.decimal_precision as dp

class account_invoice_line(models.Model):
    _inherit = 'account.invoice.line'

    # ---------- Fields management

    @api.one
    @api.depends('price_unit', 'discount', 'invoice_line_tax_id', 'quantity',
        'product_id', 'invoice_id.partner_id', 'invoice_id.currency_id')
    def _compute_price(self):
        if self.product_id and self.product_id.is_discount:
            price = -self.price_unit
        else:
            price = (self.price_unit * (1 - (self.discount or 0.0) / 100.0))
        taxes = self.invoice_line_tax_id.compute_all((price * self.quantity) - self.abs_discount, 1, product=self.product_id, partner=self.invoice_id.partner_id)
        self.price_subtotal = taxes['total']
        if self.invoice_id:
            self.price_subtotal = self.invoice_id.currency_id.round(self.price_subtotal)

    @api.model
    def _default_price_unit(self):
        if not self._context.get('check_total'):
            return 0
        total = self._context['check_total']
        for l in self._context.get('invoice_line', []):
            if isinstance(l, (list, tuple)) and len(l) >= 3 and l[2]:
                vals = l[2]
                price = vals.get('price_unit', 0) * (1 - vals.get('discount', 0) / 100.0)
                total = total - (price * vals.get('quantity')) - vals.get('abs_discount', 0)
                taxes = vals.get('invoice_line_tax_id')
                if taxes and len(taxes[0]) >= 3 and taxes[0][2]:
                    taxes = self.env['account.tax'].browse(taxes[0][2])
                    tax_res = taxes.compute_all(price, vals.get('quantity'),
                        product=vals.get('product_id'), partner=self._context.get('partner_id'))
                    for tax in tax_res['taxes']:
                        total = total - tax['amount']
        return total

    price_unit = fields.Float(string='Unit Price', required=True,
        digits= dp.get_precision('Product Price'),
        default=_default_price_unit)
    price_subtotal = fields.Float(string='Amount', digits= dp.get_precision('Account'),
        store=True, readonly=True, compute='_compute_price')
    abs_discount = fields.Float(string='Discount', digits= dp.get_precision('Discount'),
        default=0.0)


class account_invoice(models.Model):
    _inherit = 'account.invoice'
    
    # ---------- Fields management

    @api.one
    @api.depends('invoice_line.price_subtotal', 'invoice_line.quantity', 'invoice_line.price_unit', 'invoice_line.discount', 'invoice_line.abs_discount')
    def _compute_discount_total(self):
        self.discount_total = 0.0

        for line in self.invoice_line:
            if line.product_id and line.product_id.is_discount:
                self.discount_total += line.price_unit
            else:
                self.discount_total +=  line.quantity * (line.price_unit * ((line.discount or 0.0) / 100.0)) + line.abs_discount
    
    discount_total = fields.Float(string='Total of discounts', digits=dp.get_precision('Account'),
        compute='_compute_discount_total', store=True)
