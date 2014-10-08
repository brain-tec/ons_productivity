# -*- coding: utf-8 -*-
#
#  File: __openerp__.py
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
{
    'name' : 'Open-Net Productivity: credit control',
    'version' : '7.3.02',
    'author' : 'Open Net Sarl',
    'category' : 'Base',
    'description' : """
More for your credit control, by Open Net
-----------------------------------------

The 'productivity' modules is a complete family of modules offering improvement for OpenERP.
These modules are maintained by Open Net, Swiss Partner of OpenERP.
These modules are included in all our hosting solutions.

**Author :** Open Net Sàrl   Industrie 59  1030 Bussigny  Suisse  http://www.open-net.ch

**Contact :** info@open-net.ch

**History :**

V7.0    2013-09-25/Cyp
    - customized mako report with datetime module included 

V7.1    2013-11-07/Cyp
    - "letter" credit lines are set to "done" after being printed
    - "email" credit lines are set to "ready to be sent" after being printer

V7.2    2013-11-18/Cyp
    - Specific follow-up level for refunds
    - Refunds does not inherit from the partner payment terms any more (the field remains manually editable)

V7.3    2013-11-19/Cyp
    - Corresponding invoices and refunds lists in the partner's form

V7.3.02 2013-11-21/Cyp
    - Correct PDF filename (print report)

Contact:
    info@open-net.ch
    """,
    'website': 'http://www.open-net.ch',
    'images' : [],
    'depends' : ['account_credit_control'],
    'data': [
        'report/report.xml',
        'wizard/credit_control_printer_view.xml',
        'accounting_view.xml',
        'partners_view.xml',
    ],
    'js': [
    ],
    'qweb' : [
    ],
    'css':[
    ],
    'demo': [
    ],
    'test': [
    ],
    'installable': True,
    'auto_install': False,
}
