# -*- coding: utf-8 -*-
#
#  File: wizards/sale_make_invoice_advance.py
#  Module: ons_productivity_sale_assets
#
#  Created by cyp@open-net.ch
#
#  Copyright (c) 2015-TODAY Open Net Ltd. <http://www.open-net.ch>
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

from openerp.osv import fields, osv
from openerp.tools.translate import _
import openerp.addons.decimal_precision as dp

class sale_asset_create_wizard(osv.osv_memory):
    _name = 'sale.asset.create_wizard'
    _description = 'Create an asset from a sale order line'
    _rec_name = 'product_id'

    _columns = {
        'product_id': fields.many2one('product.product', 'Product'),
        'sale_line_id': fields.many2one('sale.order.line', 'Sale line'),
        'product_info': fields.char('Product infos', size=200),
        'note': fields.text('Information', required=True),
        'serial': fields.char('Serial Nb', size=64),
        'date_start': fields.date('Date start'),
        'date_end': fields.date('Date end'),
    }
    
    def _get_default_product(self, cr, uid, context={}):
        sale_line_id = (context or {}).get('active_id', False)
        if not sale_line_id:
            return False
        
        sale_line = self.pool.get('sale.order.line').browse(cr, uid, sale_line_id, context=context)
        return sale_line and sale_line.product_id and sale_line.product_id.id or False
    
    _defaults = {
        'sale_line_id': lambda s, c, u, ctx: ctx.get('active_id', False),
        'product_id': _get_default_product,
    }

    def action_create_asset(self, cr, uid, ids, context=None):
        if context is None:
            context = {}
        data = self.read(cr, uid, ids, ['serial','date_start','date_end', 'note', 'product_id', 'product_info'], context=context)[0]
        if data.get('id', False):
            del data['id']
        
        sol = False
        if context.get('active_id', False):
            sol = self.pool.get('sale.order.line').browse(cr, uid, context.get('active_id', False), context=context)
            if not sol:
                return {}
        product_id = (sol and sol.product_id and sol.product_id.id) or False
        if data.get('product_id', False):
            product_id = data['product_id'][0]
        if not product_id:
            return {}
        if not isinstance(product_id, (int, long)):
            product_id = product_id.id
        data.update({
            'product_id': product_id,
            'sale_id': sol and sol.order_id and sol.order_id.id or False,
            'sale_line_id': sol and sol.id or False,
            'partner_id': sol and sol.order_id and sol.order_id.partner_id and sol.order_id.partner_id.id or False,
        })
        assets_obj = self.pool.get('sale.asset')
        assets_obj.create(cr, uid, data, context=context)
        assets_ids = assets_obj.search(cr, uid, [('sale_id','=',data['sale_id'])], context=context)

        action_domain = "[('id','in',[" + ','.join(map(str, assets_ids)) + "])]"
        action_context = {'ons_no_sale_grp':'1'}
        
        ret = assets_obj.action_view_related_assets(cr, uid, [], action_domain, action_context, context=context)
        return ret
