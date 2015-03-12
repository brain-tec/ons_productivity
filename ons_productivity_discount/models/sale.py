# -*- coding: utf-8 -*-
#
#  File: models/sale.py
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

from openerp.osv import osv, fields
import openerp.addons.decimal_precision as dp

class sale_order_line(osv.Model):
    _inherit = 'sale.order.line'
    
    # ---------- Fields management

    def _amount_line(self, cr, uid, ids, field_name, arg, context=None):
        tax_obj = self.pool.get('account.tax')
        cur_obj = self.pool.get('res.currency')
        res = {}
        if context is None:
            context = {}
        for line in self.browse(cr, uid, ids, context=context):
            if line.product_id and line.product_id.is_discount:
                price = -line.price_unit
            else:
                price = line.price_unit * (1 - (line.discount or 0.0) / 100.0)
            taxes = tax_obj.compute_all(cr, uid, line.tax_id, (price * line.product_uom_qty) - line.abs_discount, 1, line.product_id, line.order_id.partner_id)
            cur = line.order_id.pricelist_id.currency_id
            res[line.id] = cur_obj.round(cr, uid, cur, taxes['total'])
        return res
    
    _columns = {
        'abs_discount': fields.float('Discount', digits_compute=dp.get_precision('Discount'), readonly=True, states={'draft': [('readonly', False)]}),
        'price_subtotal': fields.function(_amount_line, string='Subtotal', digits_compute= dp.get_precision('Account')),
    }

    # ---------- Utilities
    
    def _prepare_order_line_invoice_line(self, cr, uid, line, account_id=False, context=None):
        values = super(sale_order_line, self)._prepare_order_line_invoice_line(cr, uid, line, account_id=account_id, context=context)
        values['abs_discount'] = line.abs_discount
        
        return values


class sale_order(osv.Model):
    _inherit = 'sale.order'
    
    # ---------- Fields management

    def _compute_discount_total(self, cr, uid, ids, field_name, arg, context=None):
        tax_obj = self.pool.get('account.tax')
        cur_obj = self.pool.get('res.currency')
        res = {}
        if context is None:
            context = {}
        for so in self.browse(cr, uid, ids, context=context):
            val = 0.0
            for line in so.order_line:
                if line.product_id and line.product_id.is_discount:
                    val += line.price_unit
                else:
                    val +=  line.product_uom_qty * (line.price_unit * ((line.discount or 0.0) / 100.0)) + line.abs_discount
            
            res[so.id] = val
        
        return res
    
    _columns = {
        'discount_total': fields.function(_compute_discount_total, string='Total of discounts', digits_compute= dp.get_precision('Account')),
    }
