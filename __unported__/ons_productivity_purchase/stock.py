# -*- coding: utf-8 -*-
#
#  File: stock.py
#  Module: ons_productivity_purchase
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

from osv import fields, osv
import openerp.addons.decimal_precision as dp

import logging
_logger = logging.getLogger(__name__)

class stock_picking(osv.osv):
    _inherit = 'stock.picking'

    def _get_discount_invoice(self, cr, uid, move_line):
        '''Return the discount for the move line'''
        if move_line.sale_line_id:
            return move_line.sale_line_id.discount
        if move_line.purchase_line_id:
            return move_line.purchase_line_id.discount
        return 0.0

    def _prepare_invoice_line(self, cr, uid, group, picking, move_line, invoice_id,
        invoice_vals, context=None):
        return super(stock_picking, self)._prepare_invoice_line(cr, uid, group, picking, move_line, invoice_id, invoice_vals, context=context)

    def action_invoice_create(self, cr, uid, ids, journal_id=False, group=False, type='out_invoice', context=None):
        return super(stock_picking, self).action_invoice_create(cr, uid, ids, journal_id=journal_id, group=group, type=type, context=context)

stock_picking()
