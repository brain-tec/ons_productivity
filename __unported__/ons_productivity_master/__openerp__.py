# -*- coding: utf-8 -*-
#
#  File: __openerp__.py
#  Module: ons_productivity_master
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
    'name' : 'Open-Net Productivity: master',
    'version' : '7.0.05',
    'author' : 'Open Net Sarl',
    'category' : 'Base',
    'description' : """
Open Net Productivity : Masdter Base module
-------------------------------------------

The 'productivity' modules is a complete family of modules offering improvement for OpenERP.
These modules are maintained by Open Net, Swiss Partner of OpenERP.
These modules are included in all our hosting solutions.

**Features list :**
    - "Marketing" menu entry --> under "Sales"
    - "Events" menu enty --> under "Messaging > Organizer"
    - "knowledge" entry menu --> under "Tools"
    - "Settings > Tehnical > Email" entry menu --> "Settings > Configuration"
    - The standard users have the simplified form for their profil

**Author :** Open Net Sàrl   Industrie 59  1030 Bussigny  Suisse  http://www.open-net.ch

**Contact :** info@open-net.ch

**History :**

V7.0: 2013-12-23/Cyp
    - Scratch writing
    """,
    'website': 'http://www.open-net.ch',
    'images' : [],
    'depends' : ['marketing','sale','event','mail','knowledge','survey'],
    'data': [
        'ui_view.xml'
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
