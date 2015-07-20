# -*- coding: utf-8 -*-
#
#  File: accounts.py
#  Module: ons_productivity_accounting
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

from openerp.osv import osv

import logging
_logger = logging.getLogger(__name__)

class account_account(osv.osv):
    _inherit = 'account.account'

    def search(self, cr, uid, args, offset=0, limit=None, order=None, context=None, count=False):
        if context is None:
            context = {}
        
        if context.get('ons_filter_inactive_parents', False):
            cr.execute("select id from account_account where active is false")
            args += [('parent_id','in', [x[0] for x in cr.fetchall()])]

        result = super(account_account, self).search(cr, uid, args, offset, limit, order, context=context, count=count)

        return result
