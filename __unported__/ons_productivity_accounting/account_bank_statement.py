# -*- coding: utf-8 -*-
#
#  File: account_bank_statement.py
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

from openerp.osv import osv, fields

import logging
_logger = logging.getLogger(__name__)

class account_bank_statement_line(osv.osv):
    _inherit = 'account.bank.statement.line'
    
    _columns = {
        'onsp_use_bnk_stmt_date': fields.boolean('Use the date of the bank statement instead'),
    }
    
    def create(self, cr, uid, vals, context={}):
        if self.pool.get('ir.values').get_default(cr, uid, self._name, 'onsp_use_bnk_stmt_date'):
            bnk_stmt = self.pool.get('account.bank.statement').read(cr, uid, vals['statement_id'], ['date'], context=context)
            if bnk_stmt and bnk_stmt.get('date'):
                vals['date'] = bnk_stmt['date']
        
        return super(account_bank_statement_line, self).create(cr, uid, vals, context=context)
    
account_bank_statement_line()

class account_bank_statement(osv.osv):
    _inherit = 'account.bank.statement'
    
    def button_journal_entries(self, cr, uid, ids, context=None):
      ctx = (context or {}).copy()
      ctx['journal_id'] = self.browse(cr, uid, ids[0], context=context).journal_id.id
      return {
        'view_type':'form',
        'view_mode':'tree',
        'res_model':'account.move.line',
        'view_id':False,
        'type':'ir.actions.act_window',
        'domain':[('statement_id','in',ids)],
        'context':ctx,
      }
    
account_bank_statement()

