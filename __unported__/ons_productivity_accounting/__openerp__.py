# -*- coding: utf-8 -*-
#
#  File: __openerp__.py
#  Module: ons_productivity_accounting
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
    'name' : 'Open-Net Productivity: accounting',
    'version' : '1.3.02',
    'author' : 'Open Net Sarl',
    'category' : 'Base',
    'description' : """
Open Net Productivity : Accounting module
-----------------------------------------

The 'productivity' modules is a complete family of modules offering improvement for OpenERP.
These modules are maintained by Open Net, Swiss Partner of OpenERP.
These modules are included in all our hosting solutions.

**Features list :**
    - Allow to cancel and delete an invoice, even if has been confirmed before
    - Option to use the bank statement date in the lines instead of today's date. This can be configured in the Settings > Configuration > Accounting menu.

**Author :** Open Net Sàrl   Industrie 59  1030 Bussigny  Suisse  http://www.open-net.ch

**Contact :** info@open-net.ch

**History :**
V1.0: 2013-05-07/Cyp
    - Delete an cancelled invoice

V1.1.04: 2013-10-14/Cyp
    - Bank statements: line may automatically use the statement's date

V1.2.0: 2013-12-27/Cyp
    - Ability to recompute the accounts hierarchy (Settings > accounting)

V1.3.0: 2014-01-17/Cyp
    - Accounts hierarchy inconsistencies management
""",
    'website': 'http://www.open-net.ch',
    'images' : [],
    'depends' : ['account','l10n_ch_base_bank'],
    'data': [
        'res_config_view.xml',
        'accounts_view.xml',
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
