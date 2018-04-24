# -*- coding: utf-8 -*-
#
#  File: __manifest__.py
#  Module: ons_productivity_procurement_adv
#
#  Created by: cyp@open-net.ch
#
#  Copyright (c) 2018-TODAY Open-Net Sarl. All rights reserved.
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    'name' : 'Open Net Productivity: Advanced Procurement Management',
    'version' : '11.0',
    'author' : 'Open Net Sarl',
    'category' : 'Warehouse',
    'website': 'http://www.open-net.ch',
    'images' : [],
    'depends' : [
        'stock'
    ],
    'data': [
        'views/view_procurements.xml',
    ],
    'installable': True,
    'auto_install': False,
}
