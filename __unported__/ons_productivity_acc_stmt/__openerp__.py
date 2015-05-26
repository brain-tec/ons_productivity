# -*- coding: utf-8 -*-
#
#  File: __openerp__.py
#  Module: ons_productivity_acc_stmt
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
    'name' : 'Open-Net Productivity: account statement management',
    'version' : '7.1.10',
    'author' : 'Open Net Sarl',
    'category' : 'Open-Net customizations',
    'description' : """
More for your account statements, by Open Net
--------------------------------------------

The 'productivity' modules is a complete family of modules offering improvement for OpenERP.
These modules are maintained by Open Net, Swiss Partner of OpenERP.
These modules are included in all our hosting solutions.

**Author :** Open Net Sàrl   Industrie 59  1030 Bussigny  Suisse  http://www.open-net.ch

**Contact :** info@open-net.ch

**History :**

V7.0: 2013-08-23
    - Introducing a new object that reflects the account statements given by a bank
      Currently, the recorgnized format is MT940
      Then, these objects may be used to reconcile account move lines 

V7.1.07: 2014-05-07/Cyp
    - Parameters: IN/OUT directories
    - Automating the import of the account statements
    - Automating the export of payment ordrers

V7.1.08: 2014-08-20/Cyp
    - Updated

V7.1.09: 2014-09-01/Cyp
    - Introducing the 'ref' field in the account statements (= last part of the :86: field, separator: spaces)

V7.1.10: 2014-09-08/Cyp
    - Regular expression available to find the ref field in the :86: record
    """,
    'website': 'http://www.open-net.ch',
    'images' : [],
    'depends' : ['account','l10n_ch_payment_slip'],
    'data': [
    	'config/security/security.xml',
    	'config/security/ir.model.access.csv',
        'config/data/account_data.xml',
        'account_statements_view.xml',
        'wizard/wiz_import_account_statements_view.xml',
        'wizard/wiz_acc_stmt_in_bnk_stmt_view.xml',
        'config/config_view.xml',
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
