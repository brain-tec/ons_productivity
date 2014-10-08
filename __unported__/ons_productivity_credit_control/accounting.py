# -*- coding: utf-8 -*-
#
#  File: accounting.py
#  Module: ons_productivity_credit_control
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

import time
import tools
from osv import fields, osv, orm

import logging
_logger = logging.getLogger(__name__)

class account_invoice(osv.osv):
    _inherit = 'account.invoice'

    def action_date_assign(self, cr, uid, ids, *args):
        for inv in self.browse(cr, uid, ids):
            if inv.type in ['out_refund']:
                self.write(cr, uid, [inv.id], {'date_due': time.strftime('%Y-%m-%d')})
            else:
                res = self.onchange_payment_term_date_invoice(cr, uid, inv.id, inv.payment_term.id, inv.date_invoice)
                if res and res['value']:
                    self.write(cr, uid, [inv.id], res['value'])
        return True

    def onchange_partner_id(self, cr, uid, ids, type, partner_id,\
            date_invoice=False, payment_term=False, partner_bank_id=False, company_id=False):
            
        ret = super(account_invoice, self).onchange_partner_id(cr, uid, ids, type, partner_id,\
                    date_invoice=date_invoice, payment_term=payment_term, partner_bank_id=partner_bank_id, company_id=company_id)
        
        if type == 'out_refund' and ret.get('value'):
            ret['value']['payment_term'] = False
        
        return ret

account_invoice()

class CreditControlPolicyLevel(orm.Model):
    _inherit = 'credit.control.policy.level'
    
    _columns = {
        'computation_mode': fields.selection([('net_days', 'Due Date'),
                                              ('end_of_month', 'Due Date, End Of Month'),
                                              ('previous_date', 'Previous Reminder'),
                                              ('refund', 'Refund')],
                                             'Compute Mode',
                                             required=True),
    }

    # ----- sql time related methods ---------

#     def _refund_get_boundary(self):
#         return self._net_days_get_boundary()

    def get_level_lines(self, cr, uid, level_id, controlling_date, lines, context=None):
        """get all move lines in entry lines that match the current level"""
        assert not (isinstance(level_id, list) and len(level_id) > 1), \
            "level_id: only one id expected"
        if isinstance(level_id, list):
            level_id = level_id[0]
        matching_lines = set()
        level = self.browse(cr, uid, level_id, context=context)
        if level.computation_mode != 'refund':
            return super(CreditControlPolicyLevel, self).get_level_lines(cr, uid, level_id, controlling_date, lines, context=context)
        
        sql = """select mv_line.id
from account_move_line mv_line, account_invoice inv
where mv_line.move_id=inv.move_id
AND mv_line.id in %(line_ids)s
and inv.type='out_refund'
and (mv_line.date_maturity + %(delay)s)::date <= date(%(controlling_date)s)"""

        level_lines = set()
        if lines:
            data_dict = {'controlling_date': controlling_date,
                         'line_ids': tuple(lines),
                         'delay': level.delay_days}

            cr.execute(sql, data_dict)
            res = cr.fetchall()
            if res:
                level_lines.update([x[0] for x in res])
        
        return level_lines

CreditControlPolicyLevel()

class CreditControlLine(orm.Model):
    _inherit = 'credit.control.line'

    _columns = {
        'is_refund': fields.boolean('Refund'),
    }

    def _prepare_from_move_line(self, cr, uid, move_line, level, controlling_date, open_amount, context=None):
        
        ret = super(CreditControlLine, self)._prepare_from_move_line(cr, uid, move_line, level, controlling_date, open_amount, context=context)
        ret['is_refund'] = level and level.computation_mode == 'refund' or False
        
        return ret

    def create_or_update_from_mv_lines(self, cr, uid, ids, lines,
                                       level_id, controlling_date, context=None):
        """Create or update line based on levels"""
        currency_obj = self.pool.get('res.currency')
        level_obj = self.pool.get('credit.control.policy.level')
        ml_obj = self.pool.get('account.move.line')
        user = self.pool.get('res.users').browse(cr, uid, uid)
        currency_ids = currency_obj.search(cr, uid, [], context=context)

        tolerance = {}
        tolerance_base = user.company_id.credit_control_tolerance
        for c_id in currency_ids:
            tolerance[c_id] = currency_obj.compute(
                cr, uid,
                c_id,
                user.company_id.currency_id.id,
                tolerance_base,
                context=context)

        level = level_obj.browse(cr, uid, level_id, context)
        line_ids = []
        for line in ml_obj.browse(cr, uid, lines, context):

            open_amount = line.amount_residual_currency

            if open_amount > tolerance.get(line.currency_id.id, tolerance_base):
                vals = self._prepare_from_move_line(
                    cr, uid, line, level, controlling_date, open_amount, context=context)
                line_id = self.create(cr, uid, vals, context=context)
                line_ids.append(line_id)

                # when we have lines generated earlier in draft,
                # on the same level, it means that we have left
                # them, so they are to be considered as ignored
                previous_draft_ids = self.search(
                    cr, uid,
                    [('move_line_id', '=', line.id),
                     ('level', '=', level.id),
                     ('state', '=', 'draft'),
                     ('id', '!=', line_id)],
                    context=context)
                if previous_draft_ids:
                    self.write(cr, uid, previous_draft_ids,
                               {'state': 'ignored'}, context=context)

        return line_ids


CreditControlLine()
