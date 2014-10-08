# -*- coding: utf-8 -*-
#
#  File: partner.py
#  Module: ons_productivity_sale
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

class res_partner(osv.osv):
    _inherit = 'res.partner'
    
    def name_search(self, cr, uid, name, args=None, operator='ilike', context=None, limit=100):
        _logger.debug(" ****************************** args="+str(args)+" and context="+str(context))
        if context is None: context = {}
        if context.get('search_default_type_company'):
            if args is None: args = []
            args += [('is_company','!=',False)]
        return super(res_partner, self).name_search(cr, uid, name, args=args, operator=operator, context=context, limit=limit)

res_partner()
