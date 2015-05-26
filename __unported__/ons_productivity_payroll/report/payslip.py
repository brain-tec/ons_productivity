# -*- coding: utf-8 -*-
#
#  File: report/crm_meeting.py
#  Module: ons_productivity_payroll
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

from openerp.osv import fields,osv
from openerp.tools.translate import _
from report import report_sxw
import pooler
import time

class payslip_webkit(report_sxw.rml_parse):
    def __init__(self, cursor, uid, name, context):
        super(payslip_webkit, self).__init__(cursor, uid, name, context=context)
        self.pool = pooler.get_pool(self.cr.dbname)
        self.cursor = self.cr
        self.localcontext.update({
            'cr': cursor,
            'uid': uid,
            'time': time,
        })


report_sxw.report_sxw('report.onsp_payslip_webkit',
                      'hr.payslip',
                      'addons/ons_productivity_payroll/report/payslip.mako',
                      parser=payslip_webkit)
