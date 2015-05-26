# -*- coding: utf-8 -*-
#
#  File: wizards/asset_make_quotation.py
#  Module: ons_productivity_sale_assets
#
#  Created by cyp@open-net.ch
#
#  Copyright (c) 2015-TODAY Open Net Sàrl. <http://www.open-net.ch>
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
        
        new_so_id = self.pool.get('sale.order').copy(cr, uid, data.name.sale_id.id, asset_id=context.get('active_id', False), context=context)
        if not new_so_id:
            return {}
        
        data.name.write({'to_handle':False})

        view_ref = self.pool.get('ir.model.data').get_object_reference(cr, uid, 'sale', 'view_order_form')
        view_id = view_ref and view_ref[1] or False,
        return {
            'type': 'ir.actions.act_window',
            'name': _('Sales Order'),
            'res_model': 'sale.order',
            'res_id': new_so_id,
            'view_type': 'form',
            'view_mode': 'form',
            'view_id': view_id,
            'target': 'current',
            'nodestroy': True,
        }
