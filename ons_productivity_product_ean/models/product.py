# -*- coding: utf-8 -*-
#
#  File: models/product.py
#  Module: ons_productivity_product_ean
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

from openerp.osv import fields, osv
from openerp.tools.translate import _

import math

def ean_checksum(eancode):
    """returns the checksum of an ean string of length 13, returns -1 if the string has the wrong length"""
    if len(eancode) not in [8, 12, 13, 14]:
        return -1
    oddsum=0
    evensum=0
    total=0
    eanvalue=eancode
    reversevalue = eanvalue[::-1]
    finalean=reversevalue[1:]
    for i in range(len(finalean)):
        if i % 2 == 0:
            oddsum += int(finalean[i])
        else:
            evensum += int(finalean[i])
    total=(oddsum * 3) + evensum
    check = int(10 - math.ceil(total % 10.0)) %10
    return check

def upc_checksum(eancode):
    sum_pair = 0
    ean_len = int(len(eancode))
    for i in range(ean_len-1):
        if not i % 2:   # if is pair
            sum_pair += int(eancode[i])
    sum = sum_pair * 3
    for i in range(ean_len-1):
        if i % 2:       # if isn't pair
            sum += int(eancode[i])
    check = ((sum/10 + 1) * 10) - sum
    return check

def check_ean(eancode):
    """returns True if eancode is a valid ean13 string, or null"""
    if not eancode:
        return True
    try:
        int(eancode)
    except:
        return False

    if len(eancode) in [8, 12, 14]:
        return ean_checksum(eancode) == int(eancode[-1])
    if len(eancode) == 13:
        return (ean_checksum(eancode) == int(eancode[-1])) or (upc_checksum(eancode) == int(eancode[-1]))

    return False
    


class product_template(osv.Model):
    _inherit = 'product.template'

    # ---------- Fields management
    
    _columns = {
        'ean13': fields.related('product_variant_ids', 'ean13', type='char', string='EAN Barcode'),
    }


class product_product(osv.Model):
    _inherit = 'product.product'

    # ---------- Fields management
    
    _columns = {
        'ean13': fields.char('EAN Barcode', size=14, help="International Article Number used for product identification."),
    }

    # ---------- Constraints management

    def _check_ean_key(self, cr, uid, ids, context=None):
        for product in self.read(cr, uid, ids, ['ean13'], context=context):
            if not check_ean(product['ean13']):
                return False
        return True

    _constraints = [(_check_ean_key, 'You provided an invalid "EAN Barcode" reference. You may use the "Internal Reference" field instead.', ['ean13'])]

