# -*- coding: utf-8 -*-
#
#  File: __openerp__.py
#  Module: ons_productivity_sale
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
    'name' : 'Open-Net Productivity: sale',
    'version' : '7.4.0',
    'author' : 'Open Net Sarl',
    'category' : 'Sales Management',
    'summary': 'More for your sales',
    'description' : """
Open Net Productivity : Sale
----------------------------

The 'productivity' modules is a complete family of modules offering improvement for OpenERP.
These modules are maintained by Open Net, Swiss Partner of OpenERP.
These modules are included in all our hosting solutions.

**Features list :**
    - a product's form now displays the quantity of this product that are involved in draft sales

**Author :** Open Net Sàrl   Industrie 59  1030 Bussigny  Suisse  http://www.open-net.ch

**Contact :** info@open-net.ch

**History :**

V7.0: 2013-10-04/Cyp
    - Scratch writing

V7.1: 2013-10-10/Cyp
    - A sale's pricelist may use another partner, it's no more mandatory to use the supplierinfo's

V7.1.03: 2013-10-11/Cyp
    - Pricelist management: behavior controlled through the Settings interface

V7.1.04: 2013-10-30/Cyp
    - At creation, invoices may inherit from the sale ID or the picking ID, depending on the origin

V7.2: 2013-12-11/Cyp
    - the module depends on sale_stock, too
    - at sale order lines editing time:
        - product in MTO: the biggest supplier delay is systematically added to the product's sale delay
        - product in MTS: the same value is also added if the stock is not enough

V7.3.03: 2013-12-27/Cyp
    - At sale order editing: force partner relationship for invoice and delivery address

V7.4.0: 2013-12-29/Cyp
    - At sale order editing: filter partner on companies (depending on the configuration)
""",
    'website': 'http://www.open-net.ch',
    'images' : [],
    'depends' : ['product','sale','stock'],
    'data': [
        'product_view.xml',
        'sale_view.xml',
        'res_config_view.xml',
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
