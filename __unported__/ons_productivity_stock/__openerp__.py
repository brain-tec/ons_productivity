# -*- coding: utf-8 -*-
#
#  File: __openerp__.py
#  Module: ons_productivity_stock
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
    'name' : 'Open-Net Productivity: stock',
    'version' : '1.4.05',
    'author' : 'Open Net Sarl',
    'category' : 'Stock Management',
    'description' : """
Open Net Productivity : Stock management
----------------------------------------------

The 'productivity' modules is a complete family of modules offering improvement for OpenERP.
These modules are maintained by Open Net, Swiss Partner of OpenERP.
These modules are included in all our hosting solutions.

**Features list :**
    - A link to 'IN' pickings from the partner's form
    - A link to 'OUT' pickings from the partner's form
    - A wizard to split a picking into individual moves
    - A serial number keeps track of the current location (stored computed field). This corresponds to the destination location of the most recent stock move

**Author :** Open Net Sàrl   Industrie 59  1030 Bussigny  Suisse  http://www.open-net.ch

**Contact :** info@open-net.ch

**History :**

V1.0: 2013-04-07/Cyp
    - link to 'IN' pickings from the partner's form
    - link to 'OUT' pickings from the partner's form

V1.2: 2013-04-17/Cyp
    - Move splitting

V1.2.20: 2013-04-25/Cyp
    - Cosmetic in the serial numbers formular
    - A serial number keeps track of the current location (stored computed field)
      This corresponds to the destination location of the most recent stock move

V1.3.10 2013-07-10/Cyp
     - "Products by location" now displays only the existing products, those with the real quantity = 0 won't show up anymore. 

V1.4.05: 2013-12-02/Cyp
    - 'Split by serial number wizard': ability to import a file
      1st column: the serial number, mandatory (field: prodlot_id)
      2nd column: the packaging, optional (field: tracking_id)

""",
    'website': 'http://www.open-net.ch',
    'images' : [],
    'depends' : ['stock','purchase'],
    'data': [
        'stock_view.xml',
        'res_config_view.xml',
        'wizard/wiz_move_splitter_view.xml',
        'wizard/stock_location_product_view.xml',
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
