# -*- coding: utf-8 -*-
#
#  File: wizards/asset_make_quotation.py
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
    _name = 'sale.asset.quotation_wizard'
    _description = 'Create a quotation from a sale asset'

    _columns = {
        'name': fields.many2one('sale.asset', 'Information', required=True),
        'date_end': fields.date('New end date for the asset'),
    }
    
    _defaults = {
        'name': lambda s, c, u, ctx: ctx.get('active_id', False),
    }

    def action_create_quotation(self, cr, uid, ids, context=None):
        if context is None:
            context = {}
        data = self.browse(cr, uid, ids[0], context=context)
        
        so_obj = self.pool.get('sale.order')
        
        so_id = so_obj.search(cr, uid, [('partner_id','=',data.name.sale_id.partner_id.id),('state','=','draft')], context=context, limit=1)
        if so_id:
            so_id = so_id[0]
            sol_id = self.pool.get('sale.order.line').copy(cr, uid, data.name.name.id, default={'order_id':so_id}, context=context)
        else:
            so_id = so_obj.copy(cr, uid, data.name.sale_id.id, default={'asset_id':context.get('active_id', False)}, context=context)

        if not so_id:
            return {}
        
        data.name.write({'to_handle':False})

        view_ref = self.pool.get('ir.model.data').get_object_reference(cr, uid, 'sale', 'view_order_form')
        view_id = view_ref and view_ref[1] or False,
        return {
            'type': 'ir.actions.act_window',
            'name': _('Sales Order'),
            'res_model': 'sale.order',
            'res_id': so_id,
            'view_type': 'form',
            'view_mode': 'form',
            'view_id': view_id,
            'target': 'current',
            'nodestroy': True,
        }
