# -*- coding: utf-8 -*-
#
#  File: wizard/trial_balance_wizard.py
#  Module: ons_productivity_budget
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

from openerp.osv import fields, osv
from openerp.tools.translate import _
import datetime
from dateutil.relativedelta import relativedelta

import logging
_logger = logging.getLogger(__name__)

class AccountTrialBalanceWizard(osv.osv_memory):
    _inherit = 'trial.balance.webkit'

    _columns = {
        'add_budget': fields.boolean("Add the budget"),
        'simplified_budget': fields.boolean("Simplified"),
        'simplified': fields.boolean('Simplified'),
    }
    
    def on_change_add_budget(self, cr, uid, ids, add_budget, date_from, date_to, context={}):
        vals = {
            'comp0_filter': 'filter_no',
            'comp0_date_from': False,
            'comp0_date_to': False,
        }
        if add_budget:
            dt = datetime.datetime.strptime(date_from, '%Y-%m-%d')
            vals['comp0_date_from'] = datetime.datetime(dt.year-1, dt.month,dt.day).strftime('%Y-%m-%d')
            dt = datetime.datetime.strptime(date_to, '%Y-%m-%d')
            vals.update({
                'comp0_date_to': datetime.datetime(dt.year-1, dt.month,dt.day).strftime('%Y-%m-%d'),
                'comp0_filter': 'filter_date',
                'simplified_budget': True,
                'simplified': False,
            })
        
        return { 'value': vals }

    def on_change_simplified(self, cr, uid, ids, simplified, context={}):
        vals = {}
        if simplified:
            vals['add_budget'] = False
        
        return { 'value': vals }

    def onchange_filter(self, cr, uid, ids, filter='filter_no', fiscalyear_id=False, context=None):
        ret = super(AccountTrialBalanceWizard, self).onchange_filter(cr, uid, ids, filter=filter, fiscalyear_id=fiscalyear_id, context=context)
        if filter != 'filter_date' and ret.get('value', {}):
            ret['value']['add_budget'] = False
        
        return ret

    def _print_report(self, cr, uid, ids, data, context=None):
        context = context or {}

        data['form']['used_context'].update({
            'budget_period_from': 0,
            'budget_period_to': 0
        })

        row = self.read(cr, uid, ids[0], ['date_from', 'date_to', 'add_budget', 'simplified_budget', 'simplified'], context=context)
        if row.get('add_budget',False):
            if  row.get('date_from'):
                data['form']['used_context'].update({'budget_period_from': int(row['date_from'][5:7])})
                context.update({'budget_period_from': int(row['date_from'][5:7])})
            if  row.get('date_to'):
                data['form']['used_context'].update({
                    'budget_period_to': int(row['date_to'][5:7]),
                    'budget_ref_day': row['date_to'],
                })
                context.update({
                    'budget_period_to': int(row['date_to'][5:7]),
                    'budget_ref_day': row['date_to'],
                })

        data = self.pre_print_report(cr, uid, ids, data, context=context)

        report_name = 'account.account_report_trial_balance_webkit'
        if row.get('simplified', False):
            report_name = 'account.ons_account_report_trial_balance_simplified'
        elif row.get('add_budget', False):
            if row.get('simplified_budget', False):
                report_name = 'account.ons_account_report_trial_balance_s_budget'
            else:
                report_name = 'account.ons_account_report_trial_balance_f_budget'

        return {'type': 'ir.actions.report.xml',
                'report_name': report_name,
                'datas': data}

        return {'type': 'ir.actions.report.xml',
                'report_name': report_name,
                'datas': data}

AccountTrialBalanceWizard()
