# -*- coding: utf-8 -*-
#
#  File: __openerp__.py
#  Module: ons_productivity_sale_assets
#
#  Created by cyp@open-net.ch
#
#  Copyright (c) 2015-TODAY Open Net Ltd. <http://www.open-net.ch>
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
    'name' : 'Open-Net Productivity: sale assets',
    'version' : '1.1.02',
    'author' : 'Open Net Sàrl',
    'category' : 'Base',
    'description' : """
Open Net Productivity : sale assets module
------------------------------------------

The 'productivity' modules is a complete family of modules offering improvement for OpenERP.
These modules are maintained by Open Net, Swiss Partner of OpenERP.
These modules are included in all our hosting solutions.

**Features list :**
 - Lets you manage the equipment renewals of the customers

**Author :** Open Net Sàrl   Industrie 59  1030 Bussigny  Suisse  http://www.open-net.ch

**Contact :** info@open-net.ch

**History :**

V1.0.0: 2015-03-18/Cyp
    - Customers' equipment renewals management

V1.0.02: 2015-03-30/Cyp
    - Cron to search for assets that need to be checked
    - The corresponding assets list
    - wizard to create a new sale quotation from an asset

V1.0.03: 2015-04-08/Cyp
    - New button: "Show the asset" in the sale order line form, in which the "Create an asset" is hidden whenever one active already exists

V1.0.04: 2015-05-13/Cyp
    - Assets may be created with any sort of products, not only the stockables.

V1.0.05: 2015-07-03/Cyp
    - Assets may be created with products and consomables, not with services
    - When an asset creates a sale, it first checks if there's a draft sale before creating a new one

V1.0.06: 2015-07-06/Cyp
    - More than one asset for each sale line
    - Sale form displays the number of products valid for assets and the number of assets

V1.1: 2015-08-13/Cyp
    - Product info: free line on the asset => in list & search as well

V1.1.02: 2015-08-14/Cyp
    - Product info can be edited at creation, within the corr. wizard
    """,
    'website': 'https://www.open-net.ch',
    'images' : [],
    'depends' : ['sale','stock'],
    'data': [
        'data/ir.model.access.csv',
        'wizards/sale_line_make_asset.xml',
        'wizards/asset_make_quotation_view.xml',
        'views/asset_view.xml',
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
