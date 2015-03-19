# -*- coding: utf-8 -*-
#
#  File: models/asset.py
#  Module: ons_productivity_sale_assets
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
from lxml import etree

import logging
_logger = logging.getLogger(__name__)

class sale_asset(osv.Model):
    _name = 'sale.asset'
    _description = 'Sale asset'
    
    # ---------- Fields management

    _columns = {
        'name': fields.text('Information', required=True),
        'product_id': fields.many2one('product.product', 'Product', domain=[('sale_ok', '=', True)], ondelete='restrict'),
        'partner_id': fields.many2one('res.partner', 'Partner', ondelete='restrict'),
        'sale_line_id': fields.many2one('sale.order.line', 'Sale line', ondelete='restrict'),
        'sale_id': fields.many2one('sale.order', 'Sale', ondelete='restrict'),
        'serial': fields.char('Serial Nb', size=64),
        'date_start': fields.date('Date start'),
        'date_end': fields.date('Date end'),
        'active': fields.boolean('Active'),
    }
    
    _defaults = {
        'active': lambda *a: True,
    }

    
    def action_view_related_assets(self, cr, uid, ids, action_domain, action_context, context=None):
        act_obj = self.pool.get('ir.actions.act_window')
        mod_obj = self.pool.get('ir.model.data')
        
        result = mod_obj.xmlid_to_res_id(cr, uid, 'ons_productivity_sale_assets.onsp_sale_asset_action', raise_if_not_found=True)
        result = act_obj.read(cr, uid, [result], context=context)[0]
        result['domain'] = action_domain
        ctx = eval(result.get('context', '{}')) or {}
        ctx.update(action_context)
        result['context'] = str(ctx)

        return result

    def fields_view_get(self, cr, uid, view_id=None, view_type='form', context=None, toolbar=False, submenu=False):
        res = super(sale_asset,self).fields_view_get(cr, uid, view_id, view_type, context, toolbar=toolbar, submenu=submenu)
        if context is None:
            context = {}

        if view_type == 'tree':
            doc = etree.XML(res['arch'])
            if context.get('ons_no_sale_grp', False):
                for node in doc.xpath("//field[@name='sale_id']"):
                    node.set('invisible', '1')
                    node.set('modifiers', node.get('modifiers').replace('false', 'true'))
            if context.get('ons_no_partner_grp', False):
                for node in doc.xpath("//field[@name='partner_id']"):
                    node.set('invisible', '1')
                    node.set('modifiers', node.get('modifiers').replace('false', 'true'))
            if context.get('ons_no_product_grp', False):
                for node in doc.xpath("//field[@name='product_id']"):
                    node.set('invisible', '1')
                    node.set('modifiers', node.get('modifiers').replace('false', 'true'))
            res['arch'] = etree.tostring(doc)
        
        return res

class sale_order(osv.Model):
    _inherit = 'sale.order'
    
    def action_view_stockable_products(self, cr, uid, ids, context=None):
        sol_obj = self.pool.get("sale.order.line")
        act_obj = self.pool.get('ir.actions.act_window')
        mod_obj = self.pool.get('ir.model.data')
        sol_ids = []
        for so in self.browse(cr, uid, ids, context=context):
            sol_ids += [sol.id for sol in so.order_line if sol.product_id and sol.product_id.type == 'product']
        if not sol_ids:
            sol_ids = [-1]

        result = mod_obj.xmlid_to_res_id(cr, uid, 'sale.action_order_line_product_tree', raise_if_not_found=True)
        result = act_obj.read(cr, uid, [result], context=context)[0]
        result['domain'] = "[('id','in',[" + ','.join(map(str, sol_ids)) + "])]"

        return result
    
    def action_view_related_assets(self, cr, uid, ids, context=None):
        action_domain = "[('sale_id','in',[" + ','.join(map(str, ids)) + "])]"
        action_context = {'ons_no_sale_grp':'1'}

        return self.pool.get('sale.asset').action_view_related_assets(cr, uid, [], action_domain, action_context, context=context)


class res_partner(osv.Model):
    _inherit = 'res.partner'
    
    # ---------- Fields management
    
    def _sale_asset_count(self, cr, uid, ids, field_name, arg, context=None):
        res = dict(map(lambda x: (x,0), ids))
        assets_obj = self.pool.get('sale.asset')

        # The current user may not have access rights for sale assets
        try:
            for partner in self.browse(cr, uid, ids, context):
                assets_ids = assets_obj.search(cr, uid, [('partner_id', '=', partner.id)], context=context)
                res[partner.id] = len(assets_ids)
        except:
            pass

        return res

    _columns = {
        'sale_asset_count': fields.function(_sale_asset_count, string='# of Sales Asset', type='integer'),
    }
    
    def action_view_related_assets(self, cr, uid, ids, context=None):
        action_domain = "[('partner_id','in',[" + ','.join(map(str, ids)) + "])]"
        action_context = {'ons_no_partner_grp':'1'}

        return self.pool.get('sale.asset').action_view_related_assets(cr, uid, [], action_domain, action_context, context=context)


class product_product(osv.Model):
    _inherit = 'product.product'
    
    # ---------- Fields management
    
    def _sale_asset_count(self, cr, uid, ids, field_name, arg, context=None):
        res = dict(map(lambda x: (x,0), ids))
        assets_obj = self.pool.get('sale.asset')

        # The current user may not have access rights for sale assets
        try:
            for product in self.browse(cr, uid, ids, context):
                assets_ids = assets_obj.search(cr, uid, [('product_id', '=', product.id)], context=context)
                res[product.id] = len(assets_ids)
        except:
            pass

        return res

    _columns = {
        'sale_asset_count': fields.function(_sale_asset_count, string='# of Sales Asset', type='integer'),
    }
    
    def action_view_related_assets(self, cr, uid, ids, context=None):
        action_domain = "[('product_id','in',[" + ','.join(map(str, ids)) + "])]"
        action_context = {'ons_no_product_grp':'1'}

        return self.pool.get('sale.asset').action_view_related_assets(cr, uid, [], action_domain, action_context, context=context)

