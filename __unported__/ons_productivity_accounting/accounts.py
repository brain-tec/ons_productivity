# -*- coding: utf-8 -*-
#
#  File: accounts.py
#  Module: ons_productivity_accounting
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

from openerp.osv import osv

import logging
_logger = logging.getLogger(__name__)

class account_account(osv.osv):
    _inherit = 'account.account'

    def _parent_store_compute(self, cr):
        active_str = ''
        active_msg = ''
        if 'active' in self._columns:
            active_str = 'active is true and '
            active_msg = 'ACTIVE records '
        if not self._parent_store:
            return
        _logger.info('Computing parent left and right for ' + active_msg + 'of the table %s...', self._table)
        def browse_rec(root, pos=0):
# TODO: set order
            where = active_str + self._parent_name+'='+str(root)
            if not root:
                where = self._parent_name+' IS NULL'
            if self._parent_order:
                where += ' order by '+self._parent_order
            cr.execute('SELECT id FROM '+self._table+' WHERE '+where)
            pos2 = pos + 1
            for id in cr.fetchall():
                pos2 = browse_rec(id[0], pos2)
            cr.execute('update '+self._table+' set parent_left=%s, parent_right=%s where id=%s', (pos, pos2, root))
            return pos2 + 1
        if active_str:
            cr.execute('update '+self._table+' set parent_left=-1, parent_right=-1 where active is false')
        query = 'SELECT id FROM '+self._table+' WHERE '+self._parent_name+' IS NULL'
        if self._parent_order:
            query += ' order by ' + self._parent_order
        pos = 0
        cr.execute(query)
        for (root,) in cr.fetchall():
            pos = browse_rec(root, pos)
        return True

    def search(self, cr, uid, args, offset=0, limit=None, order=None, context=None, count=False):
        if context is None:
            context = {}
        
        if context.get('ons_filter_inactive_parents', False):
            cr.execute("select id from account_account where active is false")
            args += [('parent_id','in', [x[0] for x in cr.fetchall()])]

        result = super(account_account, self).search(cr, uid, args, offset, limit, order, context=context, count=count)

        return result

account_account()
