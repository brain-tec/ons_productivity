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

    _columns = {
        'name': fields.many2one('sale.order.line', 'Sale line', required=True),
        'note': fields.text('Information', required=True),
        'serial': fields.char('Serial Nb', size=64),
        'date_start': fields.date('Date start'),
        'date_end': fields.date('Date end'),
    }
    
    _defaults = {
        'name': lambda s, c, u, ctx: ctx.get('active_id', False),
    }

    def action_create_asset(self, cr, uid, ids, context=None):
        if context is None:
            context = {}
        data = self.read(cr, uid, ids, ['serial','date_start','date_end', 'note'], context=context)[0]
        if data.get('id', False):
            del data['id']
        
        sol = self.pool.get('sale.order.line').browse(cr, uid, context.get('active_id', False), context=context)
        if not sol:
            return {}
        data.update({
            'product_id': sol.product_id and sol.product_id.id or False,
            'sale_id': sol.order_id and sol.order_id.id or False,
            'name': sol.id,
            'partner_id': sol.order_id and sol.order_id.partner_id and sol.order_id.partner_id.id or False,
        })
        assets_obj = self.pool.get('sale.asset')
        assets_obj.create(cr, uid, data, context=context)
        assets_ids = assets_obj.search(cr, uid, [('sale_id','=',data['sale_id'])], context=context)

        action_domain = "[('id','in',[" + ','.join(map(str, assets_ids)) + "])]"
        action_context = {'ons_no_sale_grp':'1'}
        
        ret = assets_obj.action_view_related_assets(cr, uid, [], action_domain, action_context, context=context)
        return ret
