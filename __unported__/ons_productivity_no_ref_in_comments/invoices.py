# -*- coding: utf-8 -*-
#
#  File: invoices.py
#  Module: ons_productivity_no_ref_in_comments
#
#  Created by cyp@open-net.ch
#
#  Copyright (c) 2014 Open-Net Ltd. All rights reserved.
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

from osv import osv,fields

import logging
_logger = logging.getLogger(__name__)

class account_invoice_line(osv.osv):
    _inherit = 'account.invoice.line'

    def product_id_change(self, cr, uid, ids, product, uom_id, qty=0, name='', type='out_invoice', partner_id=False, fposition_id=False, price_unit=False, currency_id=False, context=None, company_id=None):
        ret = super(account_invoice_line, self).product_id_change(cr, uid, ids, product, uom_id, qty=qty, name=name, type=type, partner_id=partner_id, fposition_id=fposition_id, price_unit=price_unit, currency_id=currency_id, context=context, company_id=company_id)
        if not ret.get('value', ''): return ret
        
        if product:
            prod = self.pool.get('product.product').read(cr, uid, product, ['name', 'variants'], context=context)
            name = prod.get('name', '') + (prod.get('variants', '') and (' - '+prod['variants']) or '')
            ret['value']['name'] = name
        
        return ret

account_invoice_line()
