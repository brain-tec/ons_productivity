 # -*- coding: utf-8 -*-
#
#  File: __openerp__.py
#  Module: ons_prod_sales
#
#  Created by dco@open-net.ch
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
    'name' : 'Open-Net Productivity: sales',
    'version' : '1.0',
    'author' : 'Open Net Sarl',
    'category' : 'Open-Net customizations',
    'description' : """
Open Net Productivity : Sales
----------------------------------------

**Features list :**
    - Enable confirm sale for team leader only

**Author :** Open Net Sàrl   Industrie 59  1030 Bussigny  Suisse  http://www.open-net.ch

**Contact :** info@open-net.ch

    """,
    'website': 'https://www.open-net.ch',
    'images' : [],
    'depends' : [
        'sale'
    ],
    'data': [
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
