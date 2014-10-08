# -*- coding: utf-8 -*-
#
#  File: __openerp__.py
#  Module: ons_productivity_packaging
#
#  Created by cyp@open-net.ch
#
#  Copyright (c) 2014 Open-Net Ltd. All rights reserved.
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
    'name' : 'Open-Net Productivity: packaging',
    'version' : '7.0.0',
    'author' : 'Open Net Sarl',
    'category' : 'Base',
    'description' : """
Open Net Productivity : Packaging module
----------------------------------------

The 'productivity' modules is a complete family of modules offering improvement for OpenERP.
These modules are maintained by Open Net, Swiss Partner of OpenERP.
These modules are included in all our hosting solutions.

**Features list :**
    - a new field: the price of a package
    - the sell price becomes a weighted average value, example:
        - if package = 50 units and the customer wants 52 units, 
        - then the unit price will be: (50*(unit price for 50) + 2*(unit price for 1))/52 

**Author :** Open Net Sàrl   Industrie 59  1030 Bussigny  Suisse  http://www.open-net.ch

**Contact :** info@open-net.ch

**History :**
V7.0: 2014-06-26/Cyp
    - scratch writing
    """,
    'website': 'http://www.open-net.ch',
    'images' : [],
    'depends' : ['product'],
    'data': [
        'products_view.xml'
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
