# -*- coding: utf-8 -*-
#
#  File: __openerp__.py
#  Module: ons_productivity_base
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
    'name' : 'Open-Net Productivity: base',
    'version' : '1.0.04',
    'author' : 'Open Net Sarl',
    'category' : 'Base',
    'description' : """
Open Net Productivity : Base module
-----------------------------------

The 'productivity' modules is a complete family of modules offering improvement for OpenERP.
These modules are maintained by Open Net, Swiss Partner of OpenERP.
These modules are included in all our hosting solutions.

**Features list :**
 - Separated menu entries for the companies and the contacts as in V 6.x versions
 - CSS definition to enlarge the formulars to full screen
 - CSS definition to hide the announce stating that there is no support contract

**Author :** Open Net Sàrl   Industrie 59  1030 Bussigny  Suisse  http://www.open-net.ch

**Contact :** info@open-net.ch

**History :**

V1.0: 2013-04-09/Cyp
    - Menu entries and CSS to enlarge the form

V1.0.02: 2013-12-16/Cyp
    - Hide the announce stating that there is no support contract

V1.0.03: 2013-12-26/Cyp
    - Separated companies/contacts menu entries under "Purchase Management"

V1.0.04: 2013-12-27/Cyp
    - Checkbox in the config: let the user select a parent for the companies, too
    """,
    'website': 'http://www.open-net.ch',
    'images' : [],
    'depends' : ['base','base_setup'],
    'data': [
        'partners_view.xml',
        'res_config_view.xml'
    ],
    'js': [
    ],
    'qweb' : [
    ],
    'css':[
        'static/src/css/onsp_base.css',
    ],
    'demo': [
    ],
    'test': [
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
}
