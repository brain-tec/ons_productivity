# -*- coding: utf-8 -*-
#
#  File: __openerp__.py
#  Module: ons_productivity_purchase
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
    'name' : 'Open-Net Productivity: purchase',
    'version' : '7.2.0',
    'author' : 'Open Net Sarl',
    'category' : 'Purchase Management',
    'summary': 'More for your purchases',
    'description' : """
Open Net Productivity : Purchase
--------------------------------

The 'productivity' modules is a complete family of modules offering improvement for OpenERP.
These modules are maintained by Open Net, Swiss Partner of OpenERP.
These modules are included in all our hosting solutions.

**Features list :**
    - A supplier's discount (product's supplier info + procurements) 

**Author :** Open Net Sàrl   Industrie 59  1030 Bussigny  Suisse  http://www.open-net.ch

**Contact :** info@open-net.ch

**History :**

V7.0: 2013-11-12/Cyp
    - Scratch writing

V7.1: 2013-11-12/Cyp
    - Supplier discount in procurements, too.

V7.2: 2013-12-12/Cyp
    - Depends also from the 'stock' and the 'sale_stock' modules
    - When a picking create an invoice, the purchase line discount is reported
    - When a purchase creates an invoice, the line discount is reported

""",
    'website': 'http://www.open-net.ch',
    'images' : [],
    'depends' : ['product','purchase','procurement','stock','sale_stock'],
    'data': [
        'product_view.xml',
        'purchase_view.xml',
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
