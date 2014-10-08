# -*- coding: utf-8 -*-
#
#  File: __openerp__.py
#  Module: ons_productivity_discount
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
    'name' : 'Open-Net Productivity: discount on payments',
    'version' : '7.1.08',
    'author' : 'Open Net Sarl',
    'category' : 'Base',
    'description' : """
More for your discount management, by Open Net
----------------------------------------------

The 'productivity' modules is a complete family of modules offering improvement for OpenERP.
These modules are maintained by Open Net, Swiss Partner of OpenERP.
These modules are included in all our hosting solutions.

** Features list :**
    - You may manage a cash discount (% and delay) on any payement (customers and suppliers)

**Author :** Open Net Sàrl   Industrie 59  1030 Bussigny  Suisse  http://www.open-net.ch

**Contact :** info@open-net.ch

**History :**

V7.0        2013-11-18/Cyp
    - Scratch writing

V7.0.10     2013-11-18/Cyp
    - The "Import Invoices" button will remain hidden in the bank statement formular.

V7.1.06: 2013-11-25/Cyp
    - New DTA wizard

V7.1.07: 2013-11-26/Cyp
    - The "Import Invoices" button is visible again in the bank statement formular.

V7.1.08: 2013-11-27/Cyp
    - Each tax has a specific account for cash discount management
    - Cash discount management on multiple taxes in invoices

    """,
    'website': 'http://www.open-net.ch',
    'images' : [],
    'depends' : ['account','account_payment','account_voucher'],
    'data': [
        'accounting_view.xml',
        'vouchers_view.xml',
        'wizard/account_payment_order_view.xml',
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
