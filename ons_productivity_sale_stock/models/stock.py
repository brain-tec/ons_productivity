# -*- coding: utf-8 -*-
#
#  File: models/stock.py
#  Module: ons_productivity_discount
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

class stock_move(osv.osv):
    _inherit = 'stock.move'

    _columns = {
        'sale_line_id': fields.many2one('sale.order.line', 'Sale Order Line', ondelete='set null', select=True, readonly=True),
        'sequence': fields.integer('Sequence'),
    }

    _defaults = {
        'sale_line_id': lambda *a:False,
        'sequence': lambda *a: 10,
    }

    def create(self, cr, uid, vals, context={}):
        return super(stock_move, self).create(cr, uid, vals, context=context)

class procurement_order(osv.osv):
    _inherit = 'procurement.order'

    def _run_move_create(self, cr, uid, procurement, context=None):
        vals = super(procurement_order, self)._run_move_create(cr, uid, procurement, context=context)
        if procurement and procurement.sale_line_id:
            vals.update({
                'sale_line_id': procurement.sale_line_id.id,
                'sequence': procurement.sale_line_id.sequence,
            })
        
        return vals
