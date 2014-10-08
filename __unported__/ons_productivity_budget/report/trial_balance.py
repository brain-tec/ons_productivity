# -*- encoding: utf-8 -*-
#
#  File: report/account_balance.py
#  Module: ons_productivity_budget
#
#  Created by cyp@open-net.ch
#
#  Copyright (c) 2013 Open-Net Ltd. All rights reserved.
##############################################################################
#
#    Author: Guewen Baconnier
#    Copyright Camptocamp SA 2011
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


from datetime import datetime

from openerp import pooler
from openerp.report import report_sxw
from openerp.tools.translate import _
from account_financial_report_webkit.report.common_balance_reports import CommonBalanceReportHeaderWebkit
from account_financial_report_webkit.report.webkit_parser_header_fix import HeaderFooterTextWebKitParser

import logging
_logger = logging.getLogger(__name__)

def sign(number):
    return cmp(number, 0)

class TrialBalanceWebkit(report_sxw.rml_parse, CommonBalanceReportHeaderWebkit):

    def __init__(self, cursor, uid, name, context):
        super(TrialBalanceWebkit, self).__init__(cursor, uid, name, context=context)
        self.pool = pooler.get_pool(self.cr.dbname)
        self.cursor = self.cr

        company = self.pool.get('res.users').browse(self.cr, uid, uid, context=context).company_id
        header_report_name = ' - '.join((_('TRIAL BALANCE'), company.name, company.currency_id.name))

        footer_date_time = self.formatLang(str(datetime.today()), date_time=True)

        self.localcontext.update({
            'cr': cursor,
            'uid': uid,
            'report_name': _('Trial Balance'),
            'display_account': self._get_display_account,
            'display_account_raw': self._get_display_account_raw,
            'filter_form': self._get_filter,
            'target_move': self._get_target_move,
            'display_target_move': self._get_display_target_move,
            'accounts': self._get_accounts_br,
            'additional_args': [
                ('--header-font-name', 'Helvetica'),
                ('--footer-font-name', 'Helvetica'),
                ('--header-font-size', '10'),
                ('--footer-font-size', '6'),
                ('--header-left', header_report_name),
                ('--header-spacing', '2'),
                ('--footer-left', footer_date_time),
                ('--footer-right', ' '.join((_('Page'), '[page]', _('of'), '[topage]'))),
                ('--footer-line',),
            ],
            'get_budget_value': self._get_budget_value,
        })

    def set_context(self, objects, data, ids, report_type=None):
        """Populate a ledger_lines attribute on each browse record that will be used
        by mako template"""
        objects, new_ids, context_report_values = self.compute_balance_data(data)
        context_report_values['budget_period_from'] = data.get('form',{}).get('used_context',{}).get('budget_period_from', 0)
        context_report_values['budget_period_to'] = data.get('form',{}).get('used_context',{}).get('budget_period_to', 0)
        context_report_values['budget_ref_day'] = data.get('form',{}).get('used_context',{}).get('budget_ref_day', 0)

        self.localcontext.update(context_report_values)

        return super(TrialBalanceWebkit, self).set_context(objects, data, new_ids,
                                                            report_type=report_type)

    def _get_budget_value(self, account, field_name, default_string=None, decimals=None, suffix=None):
        ret = False
        
        ctx = self.localcontext.get('data', {}).get('form', {}).get('used_context', {})
        
        if field_name == 'onsp_budget_rate':
            ret = self.pool.get('account.account')._comp_budget_rate(
                        self.localcontext['cr'], 
                        self.localcontext['uid'], 
                        [account.id], 
                        field_name, 
                        None, 
                        context=ctx)[account.id]
        
        if field_name == 'onsp_budget_cum':
            ret = self.pool.get('account.account')._comp_budget_cum(
                        self.localcontext['cr'], 
                        self.localcontext['uid'], 
                        [account.id], 
                        field_name, 
                        None, 
                        context=ctx)[account.id]
        
        if not ret:
            if default_string is not None:
                ret = default_string
        else:
            if decimals is not None:
                ret = (('%.' + str(decimals) + 'f') % ret) + (suffix or '')
        
        return ret

HeaderFooterTextWebKitParser('report.account.ons_account_report_trial_balance_s_budget',
                             'account.account',
                             'addons/ons_productivity_budget/report/trial_balance_s_budget.mako',
                             parser=TrialBalanceWebkit)

HeaderFooterTextWebKitParser('report.account.ons_account_report_trial_balance_f_budget',
                             'account.account',
                             'addons/ons_productivity_budget/report/trial_balance_f_budget.mako',
                             parser=TrialBalanceWebkit)

HeaderFooterTextWebKitParser('report.account.ons_account_report_trial_balance_simplified',
                             'account.account',
                             'addons/ons_productivity_budget/report/trial_balance_simplified.mako',
                             parser=TrialBalanceWebkit)
