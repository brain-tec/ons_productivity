# -*- coding: utf-8 -*-
#
#  File: __openerp__.py
#  Module: ons_productivity_product_ean
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
    'name' : 'Open-Net Productivity: product EAN barcodes',
    'version' : '1.0.0',
    'author' : 'Open Net Sarl',
    'category' : 'Base',
    'description' : """
Open Net Productivity : Product's EAN Barcodes module
-----------------------------------------------------

The 'productivity' modules is a complete family of modules offering improvement for OpenERP.
These modules are maintained by Open Net, Swiss Partner of OpenERP.
These modules are included in all our hosting solutions.

**Features list :**
 - Allows the use of EAN8, EAN12, EAN13, EAN14 and GLN(UPC) at the same time
   Note that if 13 digits (checksum included) are given, a first test is used with EAN13, than if it fails GLN is used
 - EAN code may be used to search products, too

**Author :** Open Net Sàrl   Industrie 59  1030 Bussigny  Suisse  http://www.open-net.ch

**Contact :** info@open-net.ch

**History :**

V1.0.0: 2015-04-16/Cyp
    - Scratch writing, inspired by the "product_gtn" module (by ChriCar Beteiligungs- und Beratungs- GmbH)
    """,
    'website': 'https://www.open-net.ch',
    'images' : [],
    'depends' : ['product'],
    'data': [
        'views/view_product.xml',
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