# -*- coding: utf-8 -*-
#
#  File: __openerp__.py
#  Module: ons_productivity_accounting
#
#  dco@open-net.ch & cyp@open-net.ch
#
#  Copyright (c) 2016-TODAY Open-Net Ltd. All rights reserved.
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    'name' : 'Open Net Productivity: Accounting TVA',
    'version' : '2.0',
    'author' : 'Open Net Sàrl',
    'category' : 'Accounting',
    'website': 'http://www.open-net.ch',
    'images' : [],
    'depends' : [
        'account',
    ],
    'data': [
        'data/get_tags_from_tax.xml',
        'views/view_account_move_line.xml',
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
