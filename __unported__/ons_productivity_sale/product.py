# -*- coding: utf-8 -*-
#
#  File: product.py
#  Module: ons_productivity_sale
#
#  Created by cyp@open-net.ch
#
#  Copyright (c) 2013 Open Net Sàrl. All rights reserved.
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

class product_product(osv.osv):
    _inherit = 'product.product'

    # ------------------------- Fields management

    def _comp_draft_sales_quant(self, cr, uid, prod_ids, field_name, arg, context=None):
        res = {}
        if context is None:
            context = {}
        
        sl_obj = self.pool.get('sale.order.line')
        for prod_id in prod_ids:
            sl_ids = sl_obj.search(cr, uid, [('order_id.state','=','draft'),('product_id','=',prod_id)], context=context)
            q = reduce(lambda x,y: x+y, [sl.product_uom_qty for sl in sl_obj.browse(cr, uid, sl_ids, context=context)], 0)
            res[prod_id] = q
        
        return res

    _columns = {
        'draft_sales_quant': fields.function( _comp_draft_sales_quant, method=True, type='float', string="Quant. in quotations" ),
    }

product_product()
    
