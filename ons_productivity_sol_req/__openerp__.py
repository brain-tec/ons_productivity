 # -*- coding: utf-8 -*-
#
#  File: __openerp__.py
#  Module: ons_productivity_sol_req
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
    'name' : 'Open-Net productivity: requested date for S.O.L.',
    'version' : '1.0.05',
    'author' : 'Open Net Sarl',
    'category' : 'Sale',
    'summary': 'Complementary functions for the sale order lines',
    'website': 'https://www.open-net.ch',
    'depends' : [
        'sale',
        'sale_stock',
        'sale_order_dates'
    ],
    'data': [
        'views/view_sales.xml'
    ],
    'installable': True,
    'auto_install': False,
}
