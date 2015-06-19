# -*- coding: utf-8 -*-
#
#  File: __openerp__.py
#  Module: ons_productivity_discount
#
#  Created by cyp@open-net.ch
#
#  Copyright (c) 2014-TODAY Open Net Sàrl. <http://www.open-net.ch>
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
    'name' : 'Open-Net Productivity: sale and invoice discount management',
    'version' : '1.0.03',
    'author' : 'Open Net Sàrl',
    'category' : 'Base',
    'description' : """
Open Net Productivity : Discount module
---------------------------------------

The 'productivity' modules is a complete family of modules offering improvement for OpenERP.
These modules are maintained by Open Net, Swiss Partner of OpenERP.
These modules are included in all our hosting solutions.

**Features list :**
 - Lets you manage a fixed discount

**Author :** Open Net Sàrl   Industrie 59  1030 Bussigny  Suisse  http://www.open-net.ch

**Contact :** info@open-net.ch

**History :**

V1.0.0: 2015-03-10/Cyp
    - Fixed discount in sales and invoices

V1.0.02: 2015-03-18/Cyp
    - Total of HT amounts, without any taxes, without any discount, in the sale orders as well as in the invoices

V1.0.023 2015-06-19/Cyp
    - An invoice line's product, when a discount-type, may have a quantity different from 1
    """,
    'website': 'https://www.open-net.ch',
    'images' : [],
    'depends' : ['account', 'sale'],
    'data': [
        'views/sale_view.xml',
        'views/invoice_view.xml',
        'views/product_view.xml',
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
