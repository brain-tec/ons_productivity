# -*- coding: utf-8 -*-
#
#  File: __openerp__.py
#  Module: ons_productivity_invoice
#
#  Created by cyp@open-net.ch
#
#  Copyright (c) 2014-TODAY Open Net Sàrl <http://www.open-net.ch>
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
    'name' : 'Open-Net Productivity: invoice',
    'version' : '1.0.07',
    'author' : 'Open Net S\rl',
    'category' : 'Base',
    'description' : """
Open Net Productivity : Invoice
 module
----------------------------------------

The 'productivity' modules is a complete family of modules offering improvement for OpenERP.
These modules are maintained by Open Net, Swiss Partner of OpenERP.
These modules are included in all our hosting solutions.

**Features list :**
 - Invoice lines regrouped by sale order

**Author :** Open Net Sàrl   Industrie 59  1030 Bussigny  Suisse  http://www.open-net.ch

**Contact :** info@open-net.ch

**History :**

V1.0.03: 2014-12-23/Cyp
    - Scratch writing

V1.0.05: 2015-01-05/Cyp
    - New format for the invoice report: lines are grouped by sale order.

V1.0.05: 2015-01-13/Cyp
    - New repport nammed Invoices by SO (ons_productivity_invoice.report_invoice_grouped_by_so)
    """,
    'website': 'https://www.open-net.ch',
    'images' : [],
    'depends' : ['account', 'report', 'sale'],
    'data': [
        'views/report_invoice_by_so.xml',
        'views/view_invoice_by_so.xml',
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
