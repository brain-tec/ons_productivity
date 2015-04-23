# -*- coding: utf-8 -*-
#
#  File: __openerp__.py
#  Module: ons_productivity_sale_stock
#
#  Created by cyp@open-net.ch
#
#  Copyright (c) 2015-TODAY Open-Net Ltd. <http://www.open-net.ch>
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
    'name' : 'Open-Net Productivity: sale stock',
    'version' : '1.0.02',
    'author' : 'Open Net Sarl',
    'category' : 'Base',
    'description' : """
Open Net Productivity : sale stock module
-----------------------------------------

The 'productivity' modules is a complete family of modules offering improvement for OpenERP.
These modules are maintained by Open Net, Swiss Partner of OpenERP.
These modules are included in all our hosting solutions.

**Features list :**
 - Lets you manage the order of the stock moves with a sequence, inherited from the sale order line

**Author :** Open Net Sàrl   Industrie 59  1030 Bussigny  Suisse  http://www.open-net.ch

**Contact :** info@open-net.ch

**History :**

V1.0.0: 2015-03-18/Cyp
    - Scratch writing

V1.0.03: 2015-04-23/Cyp
    - Changing the stock moves' order to: pick + sequence + id
    """,
    'website': 'https://www.open-net.ch',
    'images' : [],
    'depends' : ['sale_stock','stock'],
    'data': [
        'views/view_stock.xml',
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
