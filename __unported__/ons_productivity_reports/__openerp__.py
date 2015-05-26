# -*- coding: utf-8 -*-
#
#  File: __openerp__.py
#  Module: ons_productivity_reports
#
#  Created by cyp@open-net.ch
#
#  Copyright (c) 2014 Open Net Sàrl. All rights reserved.
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
    'name' : 'Open-Net Productivity: reports',
    'version' : '1.0.0',
    'author' : 'Open Net Sarl',
    'category' : 'Open-Net customizations',
    'description' : """
Open Net Productivity : Reports
-------------------------------

The 'productivity' modules is a complete family of modules offering improvement for OpenERP.
These modules are maintained by Open Net, Swiss Partner of OpenERP.
These modules are included in all our hosting solutions.

To be used, this module requires that the following "print" service exist:
        - 'ons.sale.order'
        - 'ons.purchase.order'
        - 'ons.account.invoice'
        - 'ons.stock.picking.out'
Please, note that this module doesn't contain any report.

**Features list :**
 - Remaps some default reports to customized version:
        - sale orders
        - purchase orders
        - account invoices
        - picking out

**Author :** Open Net Sàrl   Industrie 59  1030 Bussigny  Suisse  http://www.open-net.ch

**Contact :** info@open-net.ch

**History :**
V1.0: 2014-02-04/Cyp
    - Scratch writing
Contact: 
    info@open-net.ch
    """,
    'website': 'http://www.open-net.ch',
    'images' : [],
    'depends' : ['account','sale','purchase','stock','delivery'],
    'data': [
        'pickings_view.xml',
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
