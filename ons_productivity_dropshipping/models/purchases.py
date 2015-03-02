# -*- coding: utf-8 -*-
#
#  File: purchases.py
#  Module: ons_prouctivity_dropshipping
#
#  Created by sge@open-net.ch
#
#  Copyright (c) 2015-TODAY Open Net Sàrl All rights reserved.
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

import logging
_logger = logging.getLogger(__name__)

STOCK_LOCATION_USAGE = [
    ('supplier', 'Supplier Location'),
    ('view', 'View'),
    ('internal', 'Internal Location'),
    ('customer', 'Customer Location'),
    ('inventory', 'Inventory'),
    ('procurement', 'Procurement'),
    ('production', 'Production'),
    ('transit', 'Transit Location')]

class purchase_order(osv.Model):
    _inherit = 'purchase.order'
    
    def _is_dropship(self, cr, uid, ids, name, arg, context=None):
        res = {}
        for po in self.browse(cr, uid, ids, context=context):
            res[po.id] = False
            if not po.picking_type_id:
                continue

            if (po.picking_type_id.default_location_dest_id.usage == 'customer'
                and po.picking_type_id.default_location_src_id.usage == 'supplier'):
                res[po.id] = True
        
        return res

    _columns = {
        'ons_dropship_dest' : fields.text('Destination'),
        'ons_is_dropship': fields.function(_is_dropship, type='boolean',
                                           string='Is dropship?',
                                           store=False, readonly=True),
    }

    def onchange_picking_type_id(self, cr, uid, ids, picking_type_id, context=None):
        value = super(purchase_order, self).onchange_picking_type_id(cr, uid, ids,
                                                                     picking_type_id,
                                                                     context=context)
        if not value.get('value', {}): return value

        is_dropship = False
        if picking_type_id:
            picktype = self.pool.get("stock.picking.type").browse(cr, uid,
                                                                  picking_type_id,
                                                                  context=context)
            if (picktype.default_location_dest_id.usage == 'customer'
                and picktype.default_location_src_id.usage == 'supplier'):
                is_dropship = True
        value['value']['ons_is_dropship'] = is_dropship

        return value
