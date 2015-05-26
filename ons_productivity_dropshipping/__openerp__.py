# -*- coding: utf-8 -*-
#
#  File: __openerp__.py
#  Module: ons_prouctivity_dropshipping
#
#  Created by sge@open-net.ch
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
    'name' : 'Open Net Productivity : Drop shipping',
    'version' : '0.0.1',
    'author' : 'Open Net Sarl',
    'category' : 'Base',
    'description' : """
Open Net Productivity : Drop shipping
-------------------------------------

The 'productivity' modules is a complete family of modules offering improvement for OpenERP.
These modules are maintained by Open Net, Swiss Partner of OpenERP.
These modules are included in all our hosting solutions


**Features list :**
    - Add 'Destination' field to Purchase Order.
    - Add two methods in Purchase Order needed for field 'Destination'.

**Author :** Open Net Sàrl   Industrie 59  1030 Bussigny  Suisse  http://www.open-net.ch

**Contact :** info@open-net.ch

**History :**

V0.0.1: 2015-03-02/Sge
    - Add 'Destination' field to Purchase Order.
    - Add two methods in Purchase Order needed for field 'Destination'.    

""",
    'website': 'https://www.open-net.ch',
    'images' : [],
    'depends' : ['stock_dropshipping'],
    'data': [
        'views/purchases_view.xml',
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

