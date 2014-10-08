# -*- coding: utf-8 -*-
#
#  File: purchase.py
#  Module: ons_productivity_stock
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

from openerp.osv import fields,osv
from openerp.tools.translate import _
import logging
_logger = logging.getLogger(__name__)

class purchase_order(osv.osv):
    _inherit = 'purchase.order'

    # ------------------------- Utilities
    
    def _prepare_order_picking(self, cr, uid, order, context=None):
        vals = super(purchase_order, self)._prepare_order_picking(cr, uid, order, context=context)
        
        if order.location_id.usage == 'customer' and order.partner_id:
            vals['partner_id'] = order.partner_id.id
            if order.partner_id.property_stock_customer:
                vals['location_id'] = order.partner_id.property_stock_customer.id
        
        _logger.debug("Prepare picking from ons_prod...stock")
        
        return vals

purchase_order()
