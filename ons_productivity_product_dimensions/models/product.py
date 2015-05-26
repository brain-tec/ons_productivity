# -*- coding: utf-8 -*-
#
#  File: models/product.py
#  Module: ons_productivity_product_dimensions
#
#  Created by cyp@open-net.ch
#
#  Copyright (c) 2015-TODAY Open Net Sàrl. <http://www.open-net.ch>
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

from openerp.osv import fields, osv
from openerp.tools.translate import _

class product_uom(osv.osv):
    _inherit = 'product.uom'
    
    _columns = {
        'used_to_comp_vol': fields.boolean("Used to compute a product's volume"),
    }

class product_template(osv.Model):
    _inherit = 'product.template'

    # ---------- Fields management
    
    _columns = {
        'ons_width': fields.float('Width'),
        'ons_height': fields.float('Height'),
        'ons_depth': fields.float('Depth'),
        'ons_dim_units_id': fields.many2one('product.uom', 'Dimensions units',
                                           domain="[('used_to_comp_vol', '=', True)]",
                                           help='Units used to compute the volume'),
    }

    # ---------- Interface management
    
    def on_change_dimension(self, cr, uid, ids, width, height, depth, dim_units_id, context=None):
        uom_obj = self.pool.get('product.uom')
        if not width or not height or not depth or not dim_units_id:
            volume = False
        else:
            uom = uom_obj.browse(cr, uid, dim_units_id, context=context)
            uom_ref_id = uom_obj.search(cr, uid, [('category_id', '=', uom.category_id.id),('uom_type', '=', 'reference')], context=context)
            if not uom_ref_id:
                value = False
            else:
                uom_ref_id = uom_ref_id[0]
                
            q = uom_obj._compute_qty(cr, uid, dim_units_id, 1.0, uom_ref_id, round=False)
            volume = width * height * depth * q**3

        return {'value': {'volume': volume}}

class product_product(osv.Model):
    _inherit = 'product.product'

    # ---------- Interface management
    
    def on_change_dimension(self, cr, uid, ids, width, height, depth, dim_units_id, context=None):
        uom_obj = self.pool.get('product.uom')
        if not width or not height or not depth or not dim_units_id:
            volume = False
        else:
            uom = uom_obj.browse(cr, uid, dim_units_id, context=context)
            uom_ref_id = uom_obj.search(cr, uid, [('category_id', '=', uom.category_id.id),('uom_type', '=', 'reference')], context=context)
            if not uom_ref_id:
                value = False
            else:
                uom_ref_id = uom_ref_id[0]
                
            q = uom_obj._compute_qty(cr, uid, dim_units_id, 1.0, uom_ref_id, round=False)
            volume = width * height * depth * q**3

        return {'value': {'volume': volume}}
