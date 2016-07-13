# -*- coding: utf-8 -*-
#
#  File: __openerp__.py
#  Module: ons_productivity_project_issue
#
#  Created by sge@open-net.ch
#
#  Copyright (c) 2014 Open Net Sarl. All rights reserved.
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
    'name' : 'Open-Net Productivity: Project Issue',
    'version' : '0.0.04',
    'author' : 'Open Net Sarl',
    'category' : 'Issue Management',
    'description' : """
Open Net Productivity : Project Issue
----------------------------------------------

The 'productivity' modules is a complete family of modules offering improvement for OpenERP.
These modules are maintained by Open Net, Swiss Partner of OpenERP.
These modules are included in all our hosting solutions.

**Features list :**
    - When create a new issu, add its ID on its name
    - new field for issues: short_name: the name without the [id]

**Author :** Open Net Sarl   Industrie 59  1030 Bussigny  Suisse  http://www.open-net.ch

**Contact :** info@open-net.ch

**History :**

V0.3: 2014-10-14/Sge
    - Add the feature #1

V0.4: 2014-10-14/Cyp
    - Add the feature #2

""",
    'website': 'http://www.open-net.ch',
    'images' : [],
    'depends' : ['project_issue'],
    'data': [
        'project_issue_view.xml'
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
