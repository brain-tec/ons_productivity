# -*- coding: utf-8 -*-
#
#  File: __openerp__.py
#  Module: ons_productivity_sale_layout
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
    'name' : 'Open-Net Productivity: sale and invoice layouts',
    'version' : '7.03.02',
    'author' : 'Open Net Sarl',
    'category' : 'Sales Management',
    'summary': 'Layout management for Sales Orders and Invoices',
    'description' : """
Open Net Productivity : Sale  and Invoice layout
------------------------------------------------

The 'productivity' modules is a complete family of modules offering improvement for OpenERP.
These modules are maintained by Open Net, Swiss Partner of OpenERP.
These modules are included in all our hosting solutions.

**Features list :**
    - A sale.order.line or an invoice.order.line can be defined to be of 5 different types:
       - Product
       - Title
       - Note
       - Sun Total
       - Separator line
       - Page break
       - Discount

Sale order lines as well as Invoice order line have a sequence number to manage the sub total
The 'type' of line is herited by the invoice when created from the sale
When the type 'discount' is selected in a sale order line, the quantity is set to 1.0.

Our module 'ons_webkit_report' offer the corresponding reports for sales and invoices


**Author :** Open Net Sàrl   Industrie 59  1030 Bussigny  Suisse  http://www.open-net.ch

**Contact :** info@open-net.ch

**History :**

V1.0: 2013-05-08/Cyp
    - Scratch writing

V7.01.02: 2014-01-30/Cyp
    - Official version number, according to OpenERP server's version
    - Renumbering assistant for the sequence of sale order lines and invoice order lines

V7.02.0: 2014-03-18/Cyp
    - New sub-type: discount
    - sale.orders and account.invoice have the corresponding total in a computed field: total_discount

V7.03.0: 2014-06-16/Cyp
    - New wizard in the sale order form: it lets you copy lines from another sale order
      price adapted using the new sale order's pricelist

V7.03.02: 2014-06-19/Cyp
    - While duplicating lines from another sale order, the user may choose the position
    - Translations for this wizard
""",
    'website': 'http://www.open-net.ch',
    'images' : [],
    'depends' : ['sale'],
    'data': [
        'wizard/wiz_rebuild_pos_seq.xml',
        'wizard/wiz_copy_so_lines_view.xml',
        'layout_view.xml',
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
