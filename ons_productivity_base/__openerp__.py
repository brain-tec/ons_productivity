# -*- coding: utf-8 -*-
#
#  File: __openerp__.py
#  Module: ons_productivity_base
#
#  Created by cyp@open-net.ch
#
#  Copyright (c) 2015-TODAY Open-Net Ltd. All rights reserved.
##############################################################################
#
# Part of Odoo. See LICENSE file for full copyright and licensing details.
#
##############################################################################
{
    'name' : 'Open-Net Productivity: base',
    'version' : '1.0',
    'author' : 'Open Net Sarl',
    'category' : 'Base',
    'summary': 'Complementary functions for Odoo V9',
    'website': 'http://www.open-net.ch',
    'depends' : [
        'hr',
    ],
    'data': [
        'views/view_res_users.xml',
        'views/onsp_base.xml'
    ],
    'installable': True,
    'auto_install': False,
}
