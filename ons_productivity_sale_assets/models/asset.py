# -*- coding: utf-8 -*-
#
#  File: models/asset.py
#  Module: ons_productivity_sale_assets
#
#  Created by cyp@open-net.ch
#
#  Copyright (c) 2015-TODAY Open Net Ltd. <http://www.open-net.ch>
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
from datetime import datetime
from dateutil.relativedelta import relativedelta
import time
from email.Utils import make_msgid
from openerp.addons.base.ir import ir_mail_server
import simplejson

import logging
_logger = logging.getLogger(__name__)

class sale_asset(osv.Model):
    _name = 'sale.asset'
    _description = 'Sale asset'
    
    # ---------- Fields management

    _columns = {
        'name': fields.many2one('sale.order.line', 'Sale line', ondelete='restrict'),
        'note': fields.text('Information', required=True),
        'product_id': fields.many2one('product.product', 'Product', domain=[('sale_ok', '=', True)], ondelete='restrict'),
        'partner_id': fields.many2one('res.partner', 'Partner', ondelete='restrict'),
        'sale_id': fields.many2one('sale.order', 'Sale', ondelete='restrict'),
        'serial': fields.char('Serial Nb', size=64),
        'date_start': fields.date('Date start'),
        'date_end': fields.date('Date end'),
        'active': fields.boolean('Active'),
        'to_handle': fields.boolean('To handle'),
        'gen_qtl_ids': fields.one2many('sale.order.line', 'org_asset_id', string='Generated lines', domain=[('order_id.state','in',['draft','sent'])]),
        'gen_quot_ids': fields.related('gen_qtl_ids', 'order_id', relation='sale.order', type='one2many', string='Quotations'),
        'gen_sol_ids': fields.one2many('sale.order.line', 'org_asset_id', string='Generated lines', domain=[('order_id.state','not in',['draft','sent','cancel'])]),
        'gen_sale_ids': fields.related('gen_sol_ids', 'order_id', relation='sale.order', type='one2many', string='Sales'),
        'product_info': fields.char('Product infos', size=200),
    }
    
    _defaults = {
        'active': lambda *a: True,
        'to_handle': lambda *a: False,
    }

    # ---------- Interface management
    
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

        # Depending on the source of the list, some fields may be hidden
        #   For example the assets from a sale order point of view are 
        #       filtered with it => no need to display it in the list
        #
        if view_type == 'tree':
            doc = etree.XML(res['arch'])

            if context.get('ons_no_sale_grp', False):
                for node in doc.xpath("//field[@name='sale_id']"):
                    node.set('invisible', '1')
                    d = simplejson.loads(node.get('modifiers'))
                    for k,v in d.items():
                        if not v:
                            d[k] = True
                    node.set('modifiers', simplejson.dumps(d))

            if context.get('ons_no_partner_grp', False):
                for node in doc.xpath("//field[@name='partner_id']"):
                    node.set('invisible', '1')
                    d = simplejson.loads(node.get('modifiers'))
                    for k,v in d.items():
                        if not v:
                            d[k] = True
                    node.set('modifiers', simplejson.dumps(d))

            if context.get('ons_no_product_grp', False):
                for node in doc.xpath("//field[@name='product_id']"):
                    node.set('invisible', '1')
                    d = simplejson.loads(node.get('modifiers'))
                    for k,v in d.items():
                        if not v:
                            d[k] = True
                    node.set('modifiers', simplejson.dumps(d))

            res['arch'] = etree.tostring(doc)
        
        return res

    # ---------- Scheduler management
    
    def cron_search_next_assets(self, cr, uid, nb_days=7, mail_to=False, context={}):
        today = datetime.now().strftime('%Y-%m-%d')
        next_stop = (datetime.now() + relativedelta(days=nb_days)).strftime('%Y-%m-%d')
        filter = [
            ('to_handle', '=', False),
            ('date_end', '!=', False),
            ('date_end', '>=', today),
            ('date_end', '<=', next_stop),
        ]
        asset_ids = self.search(cr, uid, filter, context=context)
        if asset_ids:
            self.write(cr, uid, asset_ids, {'to_handle':True}, context=context)
        
        return len(asset_ids) > 0


class sale_order(osv.Model):
    _inherit = 'sale.order'
    
    # ---------- Fields management

    def _comp_asset_count(self, cr, uid, ids, field_name, arg, context=None):
        res = dict(map(lambda x: (x,0), ids))
        assets_obj = self.pool.get('sale.asset')

        result = {}
        for id in ids:
            result.setdefault(id, 0)

        for so in self.browse(cr, uid, ids, context=context):
            search = assets_obj.search(cr, uid, 
                            [('name', 'in', [sol.id for sol in so.order_line if sol.product_id]),('active', '=', True)], 
                            context=context)
            result[so.id] = len(search)

        return result

    def _comp_product_count(self, cr, uid, ids, field_name, arg, context=None):
        res = dict(map(lambda x: (x,0), ids))
        assets_obj = self.pool.get('sale.asset')

        result = {}
        for id in ids:
            result.setdefault(id, 0)

        for so in self.browse(cr, uid, ids, context=context):
            count = len([sol.id for sol in so.order_line if sol.product_id and sol.product_id.type != 'service'])
            result[so.id] = count

        return result
    
    _columns = {
        'sale_asset_id': fields.many2one('sale.asset', 'Asset'),
        'sale_asset_count': fields.function(_comp_asset_count, string='# of Sales Asset', type='integer'),
        'sale_product_count': fields.function(_comp_product_count, string='# of Sales Products', type='integer'),
    }
    
    # ---------- Interface management

    def action_view_products(self, cr, uid, ids, context=None):
        sol_obj = self.pool.get("sale.order.line")
        act_obj = self.pool.get('ir.actions.act_window')
        mod_obj = self.pool.get('ir.model.data')
        sol_ids = []
        for so in self.browse(cr, uid, ids, context=context):
            sol_ids += [sol.id for sol in so.order_line if sol.product_id]
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
    
    # ---------- Instances management

    def copy(self, cr, uid, id, default=None, context=None, asset_id=False):
        default = {} if default is None else default.copy()
        asset = self.pool.get('sale.asset').browse(cr, uid, asset_id, context=context) if asset_id else False
        if asset and asset.name:
            default['order_line'] = [(6, 0, [])]
            default['sale_asset_id'] = asset_id
        new_so_id = super(sale_order, self).copy(cr, uid, id, default=default, context=context)
        if not new_so_id:
            return new_so_id
        if asset and asset.name:
            new_sol_id = self.pool.get('sale.order.line').copy(cr, uid, asset.name.id, default={'order_id':new_so_id}, context=context)
        
        return new_so_id


class sale_order_line(osv.Model):
    _inherit = 'sale.order.line'
    
    # ---------- Fields management

    def _detect_assets(self, cr, uid, ids, field_name, arg, context=None):
        res = dict(map(lambda x: (x,False), ids))
        for sol in self.browse(cr, uid, ids, context=context):
            if sol.org_asset_id:
                res[sol.id] = True

#         assets_obj = self.pool.get('sale.asset')
#         for sol_id in ids:
#             res[sol_id] = assets_obj.search(cr, uid, [('name', '=', sol_id),('active', '=', True)], context=context)
        
        return res
    
    _columns = {
        'org_asset_id': fields.many2one('sale.asset', 'Generated by'),
        'has_an_asset': fields.function(_detect_assets, type='boolean', string='Has an asset?'),
        'product_type': fields.related('product_id', 'product_tmpl_id', 'type', relation='product.product', type='selection', 
                selection=[('product', 'Stockable Product'), ('consu', 'Consumable'), ('service', 'Service')], string='Product type'),
    }

    # ---------- Interface management
    
    def action_view_related_assets(self, cr, uid, ids, context=None):
        action_domain = "[('name','in',[" + ','.join(map(str, ids)) + "])]"
        action_context = {} # {'ons_no_sale_grp':'1'}

        return self.pool.get('sale.asset').action_view_related_assets(cr, uid, [], action_domain, action_context, context=context)


class res_partner(osv.Model):
    _inherit = 'res.partner'
    
    # ---------- Fields management
    
    def _comp_sale_asset_count(self, cr, uid, ids, field_name, arg, context=None):
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
        'sale_asset_count': fields.function(_comp_sale_asset_count, string='# of Sales Asset', type='integer'),
    }
    
    # ---------- Interface management
    
    def action_view_related_assets(self, cr, uid, ids, context=None):
        action_domain = "[('partner_id','in',[" + ','.join(map(str, ids)) + "])]"
        action_context = {'ons_no_partner_grp':'1'}

        return self.pool.get('sale.asset').action_view_related_assets(cr, uid, [], action_domain, action_context, context=context)


class product_product(osv.Model):
    _inherit = 'product.product'
    
    # ---------- Fields management
    
    def _comp_sale_asset_count(self, cr, uid, ids, field_name, arg, context=None):
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
        'sale_asset_count': fields.function(_comp_sale_asset_count, string='# of Sales Asset', type='integer'),
    }
    
    # ---------- Interface management
    
    def action_view_related_assets(self, cr, uid, ids, context=None):
        action_domain = "[('product_id','in',[" + ','.join(map(str, ids)) + "])]"
        action_context = {'ons_no_product_grp':'1'}

        return self.pool.get('sale.asset').action_view_related_assets(cr, uid, [], action_domain, action_context, context=context)

