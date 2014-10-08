# -*- coding: utf-8 -*-
#
#  File: product.py
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

from openerp.osv import fields,osv
from openerp.tools.translate import _

import logging
_logger = logging.getLogger(__name__)

class product_supplierinfo(osv.osv):
    _inherit = 'product.supplierinfo'

    _columns = {
        'supplier_discount': fields.float('Discount [%]'),
    }
    
    _defaults = {
        'supplier_discount': lambda *a: 0.0,
    }

product_supplierinfo()
