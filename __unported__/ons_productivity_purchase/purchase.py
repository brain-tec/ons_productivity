# -*- coding: utf-8 -*-
#
#  File: purchase.py
#  Module: ons_productivity_purchase
#
#  Created by cyp@open-net.ch
#
#  Copyright (c) 2013 Open-Net Ltd. All rights reserved.
##############################################################################
#    
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2004-2010 Tiny SPRL (<http://tiny.be>).
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

from osv import fields, osv
import openerp.addons.decimal_precision as dp

import logging
_logger = logging.getLogger(__name__)

class purchase_order_line(osv.osv):
    _inherit = 'purchase.order.line'

    def _amount_line(self, cr, uid, ids, prop, arg, context=None):
        res = {}
        cur_obj=self.pool.get('res.currency')
        tax_obj = self.pool.get('account.tax')
        for line in self.browse(cr, uid, ids, context=context):
            price = line.price_unit * (1.0 - (line.discount or 0.0) / 100.0)
            taxes = tax_obj.compute_all(cr, uid, line.taxes_id, price, line.product_qty, line.product_id, line.order_id.partner_id)
            cur = line.order_id.pricelist_id.currency_id
            res[line.id] = cur_obj.round(cr, uid, cur, taxes['total'])
        return res

    _columns = {
        'discount': fields.float('Discount (%)', digits_compute= dp.get_precision('Discount')),
        'price_subtotal': fields.function(_amount_line, string='Subtotal', digits_compute= dp.get_precision('Account')),
        'ons_line_changed': fields.boolean('Line changed'),
    }

    _defaults = {
        'discount': 0.0,
        'ons_line_changed': lambda *a: False,
    }
    
    def create(self, cr, uid, vals, context={}):
        vals.update({'ons_line_changed':True})
        return super(purchase_order_line, self).create(cr, uid, vals, context=context)
    
    def write(self, cr, uid, ids, vals, context={}):
        if 'ons_line_changed' not in vals:
            vals.update({'ons_line_changed':True})
        return super(purchase_order_line, self).write(cr, uid, ids, vals, context=context)
    
    def onchange_product_id(self, cr, uid, ids, pricelist_id, product_id, qty, uom_id,
            partner_id, date_order=False, fiscal_position_id=False, date_planned=False,
            name=False, price_unit=False, context=None):

        res = super(purchase_order_line, self).onchange_product_id(cr, uid, ids, pricelist_id, product_id, qty, uom_id, partner_id, date_order=date_order, 
                    fiscal_position_id=fiscal_position_id, date_planned=date_planned, name=name, price_unit=price_unit, context=context)
        
        if not product_id or not res.get('value', {}):
            return res
        
        # - determine the discount
        product_obj = self.pool.get('product.product')
        partner_obj = self.pool.get('res.partner')
        if context is None: context = {}
        context_partner = context.copy()
        if partner_id:
            lang = partner_obj.browse(cr, uid, partner_id).lang
            context_partner.update( {'lang': lang, 'partner_id': partner_id} )
            product = product_obj.browse(cr, uid, product_id, context=context_partner)
            if not product:
                return res
            for supplier in product.seller_ids:
                if supplier.name.id == partner_id:
                    res['value']['discount'] = supplier.supplier_discount
                    break
        
        return res

purchase_order_line()

class purchase_order(osv.osv):
    _inherit = 'purchase.order'

    def create_procurement_purchase_order(self, cr, uid, procurement, po_vals, line_vals, context=None):
        product = self.pool.get('product.product').browse(cr, uid, line_vals['product_id'], context=context)
        if product:
            for supplier in product.seller_ids:
                if supplier.name.id == partner_id:
                    line_vals['discount'] = supplier.supplier_discount
                    break
        
        return super(purchase_order, self).create_procurement_purchase_order(cr, uid, procurement, po_vals, line_vals, context=context)

    def make_po(self, cr, uid, ids, context=None):
        return super(purchase_order, self).make_po(cr, uid, ids, context=context)
    
    def update_draft_purchase_prepare_line(self, cr, uid, po, po_l):
        vals = {}
        
        # Determine if the discount applies
        for supplier in po_l.product_id.seller_ids:
            if supplier.name.id == po.partner_id.id:
                vals.update({'discount': supplier.supplier_discount})
                break
        
        return vals

    def update_draft_purchases(self, cr, uid, context={}):
        _logger.debug(" ******************* Starting the scheduler 'update_draft_purchases'")
        po_ids = self.search(cr, uid, [('state','=','draft')], context=context)
        for po in self.browse(cr, uid, po_ids, context=context):
            for po_l in po.order_line:
                if not po_l.product_id: continue
                if not po_l.ons_line_changed: continue
                
                vals = self.update_draft_purchase_prepare_line(cr, uid, po, po_l)
                if vals:
                    vals.update({'ons_line_changed':False})
                    po_l.write(vals, context=context)
        
        _logger.debug(" ******************* End of the scheduler 'update_draft_purchases'")
                    
        return True

    def _prepare_inv_line(self, cr, uid, account_id, order_line, context=None):
        ret = super(purchase_order, self)._prepare_inv_line(cr, uid, account_id, order_line, context=context)
        ret['discount'] = order_line.discount
        
        return ret
    
    def action_invoice_create(self, cr, uid, ids, context=None):
        return super(purchase_order, self).action_invoice_create(cr, uid, ids, context=context)

purchase_order()

class procurement_order(osv.osv):
    _inherit = 'procurement.order' 

    def action_confirm(self, cr, uid, ids, context=None):
        return super(procurement_order, self).action_confirm(cr, uid, ids, context=context)

procurement_order()
