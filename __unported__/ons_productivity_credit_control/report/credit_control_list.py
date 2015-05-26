# -*- coding: utf-8 -*-
#
#  File: report/credit_control_list.py
#  Module: ons_productivity_credit_control
#
#  Created by cyp@open-net.ch
#
#  Copyright (c) 2013 Open Net Sàrl. All rights reserved.
##############################################################################
#
#    Author: Nicolas Bessi, Guewen Baconnier
#    Copyright 2012 Camptocamp SA
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

from openerp.report import report_sxw

import logging
logger = logging.getLogger('credit.control.line')

class CreditControlListReport(report_sxw.rml_parse):
    def __init__(self, cr, uid, name, context):
        super(CreditControlListReport, self).__init__(cr, uid, name, context=context)
        self.localcontext.update({
            'time': time,
            'datetime': datetime,
            'cr':cr,
            'uid': uid,
        })

report_sxw.report_sxw('report.ons_credit_control_list',
                      'credit.control.line',
                      'addons/ons_productivity_credit_control/report/credit_control_list.html.mako',
                      parser=CreditControlListReport)
