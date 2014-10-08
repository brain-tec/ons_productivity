# -*- coding: utf-8 -*-
#
#  File: product.py
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

class product_product(osv.osv):
    _inherit = 'product.product'

    def search(self, cr, uid, args, offset=0, limit=None, order=None, context=None, count=False):

        if context is None:
            context = {}

        _logger.debug("****** args="+str(args))

        if context.get('ons_existing_only', False):
            c = context.copy()
            c.update({ 'states': ('done',), 'what': ('in', 'out') })
            
            q = "Select distinct product_id from stock_move"
            if context.get('location', False):
                if type(context['location']) == type(1):
                    location_ids = [context['location']]
                elif type(context['location']) in (type(''), type(u'')):
                    location_ids = self.pool.get('stock.location').search(cr, uid, [('name','ilike',context['location'])], context=context)
                else:
                    location_ids = context['location']
                if location_ids:
                    s_locs = '(' + ','.join([str(x) for x in location_ids]) + ')'
                    q += " where location_id in " + s_locs + ' or location_dest_id in ' + s_locs
            cr.execute(q)
            prod_ids = [x[0] for x in cr.fetchall()]
            
            stock = self.get_product_available(cr, uid, prod_ids, context=c)
            prod_ids = [x for x in stock if stock[x]]
            
            args += [('id','in',prod_ids)]

        return super(product_product, self).search(cr, uid, args, offset=offset, limit=limit, order=order, context=context, count=count)

product_product()
