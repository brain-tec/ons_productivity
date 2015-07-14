# -*- coding: utf-8 -*-
#
#  File: __openerp__.py
#  Module: ons_productivity_hr_timesheet
#
#  Created by cyp@open-net.ch
#
#  Copyright (c) 2015-TODAY Open Net Sàrl <http://www.open-net.ch>
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2004-TODAY OpenERP S.A. <http://www.openerp.com>
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
    'name' : 'Open-Net Productivity: hr timesheet',
    'version' : '1.0.02',
    'author' : 'Open Net Ltd',
    'category' : 'Human Resources',
    'description' : """
Open Net Productivity : HR Timesheets module
--------------------------------------------

The 'productivity' modules is a complete family of modules offering improvement for OpenERP.
These modules are maintained by Open Net, Swiss Partner of OpenERP.
These modules are included in all our hosting solutions.

**Features list :**
 - Lets you use the employee (many linked to a same user) to manage the work time on an employee basis (instead of  the user)

**Author :** Open Net Sàrl   Industrie 59  1030 Bussigny  Suisse  http://www.open-net.ch

**Contact :** info@open-net.ch

**History :**

V1.0.02: 2015-07-14/Cyp
    - Employee in the timesheet lines

    """,
    'website': 'https://www.open-net.ch',
    'images' : [],
    'depends' : ['hr_timesheet','hr_timesheet_sheet'],
    'data': [
        'views/view_hr_timesheet.xml',
    ],
    'qweb' : [
    ],
    'demo': [
    ],
    'test': [
    ],
    'installable': True,
    'auto_install': False,
}
