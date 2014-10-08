# -*- coding: utf-8 -*-
#
#  File: budget.py
#  Module: ons_productivity_budget
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

import datetime
from dateutil.relativedelta import relativedelta
from openerp.osv import fields,osv
from openerp.tools.translate import _
import openerp.addons.decimal_precision as dp

import logging
_logger = logging.getLogger(__name__)

def strToDate(dt):
        dt_date=datetime.date(int(dt[0:4]),int(dt[5:7]),int(dt[8:10]))
        return dt_date

class crossovered_budget_lines(osv.osv):
    _inherit = 'crossovered.budget.lines'

    # ------------------------- Fields management

    def _theo_amt(self, cr, uid, ids, context=None):
        res = {}
        if context is None: 
            context = {}
        for line in self.browse(cr, uid, ids, context=context):
            today = datetime.datetime.today()
            date_to = today.strftime("%Y-%m-%d")
            date_from = line.date_from
            if context.has_key('wizard_date_from'):
                date_from = context['wizard_date_from']
            if context.has_key('wizard_date_to'):
                date_to = context['wizard_date_to']

            if line.paid_date:
                if strToDate(today.strftime("%Y-%m-%d")) <= strToDate(line.paid_date):
                    theo_amt = 0.00
                else:
                    theo_amt = line.planned_amount
            else:
                total = strToDate(line.date_to) - strToDate(line.date_from)
                elapsed = min(strToDate(line.date_to),strToDate(date_to)) - max(strToDate(line.date_from),strToDate(date_from))
                if strToDate(date_to) < strToDate(line.date_from):
                    elapsed = strToDate(date_to) - strToDate(date_to)

                if total.days:
                    theo_amt = float(elapsed.days / float(total.days)) * line.planned_amount
                else:
                    theo_amt = line.planned_amount

            res[line.id] = theo_amt
        return res

    def _theo(self, cr, uid, ids, name, args, context=None):
        res = {}
        for line in self.browse(cr, uid, ids, context=context):
            res[line.id] = self._theo_amt(cr, uid, [line.id], context=context)[line.id]
        return res

    _columns = {
        'name': fields.char('Name', select=True),
        'theoritical_amount':fields.function(_theo, string='Theoretical Amount', type='float', digits_compute=dp.get_precision('Account')),
    }

crossovered_budget_lines()

class budget_position(osv.osv):
    _name = 'onsp.budget.position'
    _description = 'Open-Net: budget position'
    
    _columns = {
        'name': fields.char('Name', size=50, required=True),
        'fiscalyear_id': fields.many2one('account.fiscalyear', 'Fiscal year', required=True),
        'period_ids': fields.one2many('onsp.budget.position.period', 'pos_id', 'Periods'),
        'account_id': fields.many2one('account.account', 'Account', required=True),
        'amount': fields.float('Amount', required=True),
        'nb_periods': fields.integer('Nb periods', required=True),
    }

    _defaults = {
        'nb_periods': lambda *a: 12,
    }

    # ---------- Instances management

    def create(self, cr, uid, vals, context={}):
        if vals.get('fiscalyear_id') and vals.get('account_id') and vals.get('amount'):
            vals['name'] = "Y%dA%dT%f" % (vals['fiscalyear_id'], vals['account_id'], vals['amount'] )
        
        new_id = super(budget_position, self).create(cr, uid, vals, context=context)

        period_obj = self.pool.get('onsp.budget.position.period')
        period_amount = float(vals['amount']) / float(vals['nb_periods'])
        format = vals['nb_periods'] < 10 and '%d' or '%02d'
        for i in range(1,vals['nb_periods']+1):
            vals = {
                'name': format % i,
                'amount': period_amount,
                'pos_id': new_id,
                'period_id': i,
            }
            period_obj.create(cr, uid, vals, context=context)
        
        return new_id
    
    def write(self, cr, uid, ids, vals, context={}):
        if isinstance(ids, (int,long)): ids = [ids]
        ret = super(budget_position, self).write(cr, uid, ids, vals, context=context)
        if isinstance(ids, (int,long)): ids = [ids]
        if 'name' not in vals:
            for row in self.browse(cr, uid, ids, context=context):
                row.write({'name': "Y%dA%dT%f" % (row.fiscalyear_id.id, row.account_id.id, row.amount)}, context=context)
        
        return ret

budget_position()

class budget_position_line(osv.osv):
    _name = 'onsp.budget.position.period'
    _description = 'Open-Net: budget position'
    _order = 'pos_id asc, period_id asc'
    
    # ------------------------- Fields-related functions
    
    _columns = {
        'name': fields.char('Name', size=50, required=True),
        'amount': fields.float('Amount', required=True),
        'pos_id': fields.many2one('onsp.budget.position', 'Budget position', ondelete='cascade', select=True),
        'period_id': fields.integer('Period ID'),
    }

    # ------------------------- Instances management
    
    def write(self, cr, uid, ids, vals, context={}):
    
        todo_list = []
        if 'amount' in vals:
            if 'pos_id' in vals:
                todo_list.append(vals['pos_id'])
            for ln in self.browse(cr, uid, ids, context=context):
                if not ln.pos_id: continue
                if ln.pos_id.id not in todo_list:
                    todo_list.append(ln.pos_id.id)
        
        ret = super(budget_position_line, self).write(cr, uid, ids, vals, context=context)
        
        for budget in self.pool.get('onsp.budget.position').browse(cr, uid, todo_list, context=context):
            sum = 0.0
            for ln in budget.period_ids:
                sum += ln.amount
            if sum != budget.amount:
                budget.write({'amount':sum}, context=context)
        
        return ret    

budget_position_line()

class account_account(osv.osv):
    _inherit = 'account.account'

    # ------------------------- Fields-related functions
    
    def _comp_budget_rate(self, cr, uid, acc_ids, field_name, arg, context=None):
        
        ret = {}
        for acc_id in acc_ids:
            ret[acc_id] = 0.0

        linear_method = self.pool.get('ir.values').get_default(cr, uid, self._name, 'budget_linear_method')
        nb_periods = self.pool.get('ir.values').get_default(cr, uid, 'onsp.wiz.setup_budget_periods', 'nb_periods')
        if not nb_periods: nb_periods = 12
        if nb_periods != 12:
            return ret

        ref_day = datetime.datetime.today()
        if context.get('budget_ref_day'):
            ref_day = datetime.datetime.strptime(context['budget_ref_day'], '%Y-%m-%d')
        s_ref_day = ref_day.strftime('%Y-%m-%d')

        end_period_id = ref_day.month
        end_of_period = datetime.date(ref_day.year, ref_day.month, 1) + relativedelta(months=1, days=-1)
        if context.get('budget_period_to'):
            end_period_id = context['budget_period_to']
            end_of_period = datetime.date(ref_day.year, context['budget_period_to'], 1) + relativedelta(months=1, days=-1)
        s_end_of_period = end_of_period.strftime('%Y-%m-%d')
        start_period_id = context.get('budget_period_from', 1)
        
        for acc in self.browse(cr, uid, acc_ids, context=context):
            for acc_budget in acc.onsp_budget_pos_ids:
                if acc_budget.fiscalyear_id.date_start > s_ref_day or acc_budget.fiscalyear_id.date_stop < s_ref_day:
                    continue
                budget_cum = 0
                for bl in acc_budget.period_ids:
                    if bl.period_id > end_period_id:
                        break
                    if bl.period_id < start_period_id:
                        continue
                    if bl.period_id < end_period_id:
                        budget_cum += bl.amount
                        continue
                    if linear_method:
                        if s_ref_day >= s_end_of_period:
                            budget_cum += bl.amount
                        else:
                            q = float(s_ref_day[8:10]) / float(s_end_of_period[8:10])
                            budget_cum += q * bl.amount
                        if not budget_cum or budget_cum == 0.0:
                            ret[acc.id] = 0.0
                        else:
                            ret[acc.id] = 100.0 * acc.balance / budget_cum
                    else:
                        if s_ref_day >= s_end_of_period:
                            budget_cum += bl.amount
                        if not budget_cum or budget_cum == 0.0:
                            ret[acc.id] = 0.0
                        else:
                            ret[acc.id] = 100.0 * acc.balance / budget_cum
        
        return ret    

    def _comp_budget_cum(self, cr, uid, acc_ids, field_name, arg, context=None):
        
        ret = {}
        for acc_id in acc_ids:
            ret[acc_id] = 0.0

        linear_method = self.pool.get('ir.values').get_default(cr, uid, self._name, 'budget_linear_method')
        nb_periods = self.pool.get('ir.values').get_default(cr, uid, 'onsp.wiz.setup_budget_periods', 'nb_periods')
        if not nb_periods: nb_periods = 12
        if nb_periods != 12:
            return ret

        ref_day = datetime.datetime.today()
        if context.get('budget_ref_day'):
            ref_day = datetime.datetime.strptime(context['budget_ref_day'], '%Y-%m-%d')
        s_ref_day = ref_day.strftime('%Y-%m-%d')

        end_period_id = ref_day.month
        end_of_period = datetime.date(ref_day.year, ref_day.month, 1) + relativedelta(months=1, days=-1)
        if context.get('budget_period_to'):
            end_period_id = context['budget_period_to']
            end_of_period = datetime.date(ref_day.year, context['budget_period_to'], 1) + relativedelta(months=1, days=-1)
        s_end_of_period = end_of_period.strftime('%Y-%m-%d')
        start_period_id = context.get('budget_period_from', 1)
        
        for acc in self.browse(cr, uid, acc_ids, context=context):
            for acc_budget in acc.onsp_budget_pos_ids:
                if acc_budget.fiscalyear_id.date_start > s_ref_day or acc_budget.fiscalyear_id.date_stop < s_ref_day:
                    continue
                budget_cum = 0
                for bl in acc_budget.period_ids:
                    if bl.period_id > end_period_id:
                        break
                    if bl.period_id < start_period_id:
                        continue
                    if bl.period_id < end_period_id:
                        budget_cum += bl.amount
                        continue
                    if linear_method:
                        if s_ref_day >= s_end_of_period:
                            budget_cum += bl.amount
                        else:
                            q = float(s_ref_day[8:10]) / float(s_end_of_period[8:10])
                            budget_cum += q * bl.amount
                        ret[acc.id] = budget_cum
                    else:
                        if s_ref_day >= s_end_of_period:
                            budget_cum += bl.amount
                        ret[acc.id] = budget_cum
        
        return ret    

    _columns = {
        'onsp_budget_pos_ids': fields.one2many('onsp.budget.position', 'account_id', 'Budget position'),
        'budget_linear_method': fields.boolean('Budget management: linear way'),
        'onsp_budget_rate': fields.function(_comp_budget_rate, method=True, type='float', string='Budget rate', store=False),
        'onsp_budget_cum': fields.function(_comp_budget_cum, method=True, type='float', string='Budget rate', store=False),
    }

account_account()
