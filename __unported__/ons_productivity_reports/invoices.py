# -*- coding: utf-8 -*-
#
#  File: invoices.py
#  Module: ons_productivity_reports
#
#  Created by cyp@open-net.ch
#
#  Copyright (c) 2014 Open Net Sàrl. All rights reserved.
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

from osv import osv,fields
from tools.translate import _

import logging
_logger = logging.getLogger(__name__)

class account_invoice(osv.osv):
    _inherit = 'account.invoice'

    def invoice_print(self, cr, uid, ids, context=None):
        ret = super(account_invoice, self).invoice_print(cr, uid, ids, context=context)
        # Ret is something like that:
        # {
        #     'type': 'ir.actions.report.xml',
        #     'report_name': 'account.invoice',
        #     'datas': datas,
        #     'nodestroy' : True
        # }
        ret['report_name'] = 'ons.account.invoice'
        
        return ret

account_invoice()
