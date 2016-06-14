 # -*- coding: utf-8 -*-
#
#  File: __openerp__.py
#  Module: ons_productivity_subscriptions_adv
#
#  Created by cyp@open-net.ch
#
#  Copyright (c) 2016-TODAY Open-Net Ltd. <http://www.open-net.ch>
##############################################################################
#
# Part of Odoo. See LICENSE file for full copyright and licensing details.
#
##############################################################################
{
    'name' : 'Open-Net productivity: subscriptions advanced',
    'version' : '1.3',
    'author' : 'Open Net Sarl',
    'category' : 'Sale',
    'summary': 'Complementary functions for the subscriptions management',
    'website': 'https://www.open-net.ch',
    'depends' : [
        'sale',
        'sale_contract',
        'sale_order_dates',
        'ons_productivity_sol_req'
    ],
    'data': [
        'views/onsp_subscriptions_adv.xml',
        'views/view_sale_subscription.xml',
        'views/view_sales.xml',
        'views/view_products.xml',
    ],
    'installable': True,
    'auto_install': False,
}
