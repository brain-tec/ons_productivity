# -*- encoding: utf-8 -*-
#
#  File: wizard/open_invoices_wizard.py
#  Module: ons_productivity_budget
#
#  Created by cyp@open-net.ch
#
#  Copyright (c) 2013 Open Net Sàrl. All rights reserved.
##############################################################################
#
#    Author: Guewen Baconnier
#    Copyright Camptocamp SA 2012
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

from openerp.osv import fields, orm

import logging
_logger = logging.getLogger(__name__)

class AccountReportOpenInvoicesWizard(orm.TransientModel):

    _inherit = 'open.invoices.webkit'

    _columns = {
        'customer_layout': fields.boolean('Customer layout'),
    }

    def _print_report(self, cr, uid, ids, data, context=None):
        me = self.browse(cr, uid, ids[0], context=context)
        # we update form with display account value
        data = self.pre_print_report(cr, uid, ids, data, context=context)
        report_name = 'account.account_report_open_invoices_webkit' if not me.customer_layout else 'account.ons_account_report_open_invoices_webkit'
        return {'type': 'ir.actions.report.xml',
                'report_name': report_name,
                'datas': data}

AccountReportOpenInvoicesWizard()
