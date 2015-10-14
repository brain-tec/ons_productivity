# -*- coding: utf-8 -*-
#
#  File: __openerp__.py
#  Module: ons_productivity_auto_split
#
#  Created by cyp@open-net.ch
#
#  Copyright (c) 2015-TODAY Open Net Sarl. <http://www.open-net.ch>
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
    'name' : 'Open-Net Productivity: automatic splitting of stock moves',
    'version' : '8.0.1',
    'author' : 'Open Net Sarl',
    'summary': 'Automatic splitting of stock moves',
    'category' : 'Warehouse Management',
    'description' : """
Open Net Productivity : Auto Split module
-----------------------------------------

The 'productivity' modules is a complete family of modules offering improvement for OpenERP.
These modules are maintained by Open Net, Swiss Partner of OpenERP.
These modules are included in all our hosting solutions.

**Features list :**
 - V1 lets you automatically split stock moves into smaller pieces, depending on the first packing defined in the product's form
   Note that the moves that are in draft state, done or cancelled are ignored.

**Author :** Open Net Sarl   Industrie 59  1030 Bussigny  Suisse  http://www.open-net.ch

**Contact :** info@open-net.ch

**History :**

V8.0.1: 2015-10-14/Cyp
    - Automatic stock moves splitting
    """,
    'website': 'https://www.open-net.ch',
    'images' : [],
    'depends' : [
        'stock'
    ],
    'data': [
        'views/stock_view.xml',
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
