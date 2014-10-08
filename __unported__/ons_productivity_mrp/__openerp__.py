# -*- coding: utf-8 -*-
#
#  File: __openerp__.py
#  Module: ons_productivity_mrp
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
    'name' : 'Open-Net Productivity MRP',
    'version' : '1.1.07',
    'author' : 'Open Net Sarl',
    'category' : 'Manufacturing',
    'description' : """
Open Net Productivity : MRP
---------------------------

The 'productivity' modules is a complete family of modules offering improvement for OpenERP.
These modules are maintained by Open Net, Swiss Partner of OpenERP.
These modules are included in our hosting solutions.

**Features list :**
    - Compute the product's standard price as the sum of the BOM components standard price. In the product form, if you check the box 'Compute standard price' a new button will be displayed in the form 'Compute standard price'. This button will compute the sum of all BOM components standard price and display the result in the 'Cost price'.
    - Add a new menu Manufacturing/Products/Bill of Materials Structure for a direct access to the hierarchical view of the BoMs
 
**Author :** Open Net Sàrl   Industrie 59  1030 Bussigny  Suisse  http://www.open-net.ch

**Contact :** info@open-net.ch

**History :**

V 1.0: 2013-04-21
    - Scratch writing

V 1.1: 2013-04-22
    - BoM-based product's standard price computing
    
""",
    'website': 'http://www.open-net.ch',
    'images' : [],
    'depends' : ['mrp'],
    'data': [
        'mrp_view.xml',
        'product_view.xml',
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
