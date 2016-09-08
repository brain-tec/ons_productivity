 # -*- coding: utf-8 -*-
#
#  File: __openerp__.py
#  Module: ons_productivity_pos
#
#  Created by cyp@open-net.ch
#
#  Copyright (c) 2015-TODAY Open-Net Ltd. <http://www.open-net.ch>
##############################################################################
#
# Part of Odoo. See LICENSE file for full copyright and licensing details.
#
##############################################################################
{
    'name' : 'Open-Net productivity: Point of Sale',
    'version' : '1.0',
    'author' : 'Open Net Sarl',
    'category' : 'Point of Sale',
    'summary': 'Complementary functions for the Points of Sale',
    'website': 'https://www.open-net.ch',
    'depends' : [
        'sale',
        'point_of_sale',
    ],
    'data': [
        'views/templates.xml',
        'views/view_pos_order_report.xml',
        'views/view_pos.xml'
    ],
    'installable': True,
    'auto_install': False,
}
