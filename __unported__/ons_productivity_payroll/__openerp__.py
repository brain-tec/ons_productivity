# -*- coding: utf-8 -*-
#
#  File: __openerp__.py
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
{
    'name' : 'Open-Net Productivity Payroll',
    'version' : '1.01',
    'author' : 'Open Net Sarl',
    'category' : 'Human Resources',
    'description' : """
More for your payroll processes, by Open Net
--------------------------------------------

The 'productivity' modules is a complete family of modules offering improvement for OpenERP.
These modules are maintained by Open Net, Swiss Partner of OpenERP.
These modules are included in all our hosting solutions.

**Author :** Open Net Sàrl   Industrie 59  1030 Bussigny  Suisse  http://www.open-net.ch

**Contact :** info@open-net.ch

**History :**

V 1.0: 2013-05-14/Cyp
    - Possibility to pay the salary straight from the employee's salary form
    - Cancel and Draft buttons

V 1.01: 2013-12-18/Cyp
    - Preceding code removed: not used. Only the report is kept.

""",
    'website': 'http://www.open-net.ch',
    'images' : [],
    'depends' : ['hr_payroll','hr_payroll_account'],
    'data': [
        'payroll_view.xml',
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
