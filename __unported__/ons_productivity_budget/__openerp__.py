# -*- coding: utf-8 -*-
#
#  File: __openerp__.py
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
{
    'name' : 'Open-Net Productivity: budget',
    'version' : '7.2.10',
    'author' : 'Open Net Sarl',
    'category' : 'Accounting & Finance',
    'description' : """
More for your OpenERP analytic and budgets, by Open Net
-------------------------------------------------------

The 'productivity' modules is a complete family of modules offering improvement for OpenERP.
These modules are maintained by Open Net, Swiss Partner of OpenERP.
These modules are included in all our hosting solutions.

**Author :** Open Net Sàrl   Industrie 59  1030 Bussigny  Suisse  http://www.open-net.ch

**Contact :** info@open-net.ch

**History :**

V7.0: 2013-10-08/Cyp
    - Scratch writing: crossovered budgets complements

V7.1: 2013-10-22/Cyp
    - Budget positions

V7.1.12: 2013-10-30/Cyp
    - Budget positions in reports

V7.1.25: 2013-11-13/Cyp
    - Defining access rights
    - Nb of periods defaults to 12 in the reports

V7.2.07: 2013-11-22/Cyp
    - New report: opened invoices with a layout for the customers
    - New report: simplifed report for the trial balance

V7.2.09: 2013-11-24/Cyp
    - New budget report

V7.2.10: 2013-11-26/Cyp
    - 3 budget report at disposal:
        - simplified (1 column: balance)
        - simplified budget (balance + budget + ratio)
        - full budget (debit + credit + balance + budget + ratio)
    """,
    'website': 'http://www.open-net.ch',
    'images' : [],
    'depends' : ['account_budget','account', 'account_financial_report_webkit'],
    'data': [
        'security/ir.model.access.csv',
        'wizard/setup_budget_periods_view.xml',
        'wizard/trial_balance_wizard_view.xml',
        'wizard/open_invoices_wizard_view.xml',
        'budget_view.xml',
        'res_config_view.xml',
        'budget_report.xml',
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
    'application': True,
    'auto_install': False,
}
