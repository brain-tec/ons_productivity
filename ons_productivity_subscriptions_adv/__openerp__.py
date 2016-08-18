# -*- coding: utf-8 -*-
# © 2016 Open Net Sarl
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    'name' : 'Open Net productivity: subscriptions advanced',
    'version' : '1.0.0.0',
    'author' : 'Open Net Sarl',
    'category' : 'Extra Tools',
    'website': 'https://www.open-net.ch',
    'depends' : [
        'sale',
        'sale_contract',
        'sale_order_dates',
        'ons_productivity_sol_req'
    ],
    'data': [
        'views/onsp_base.xml',
        'views/onsp_subscriptions_adv.xml',
        'views/view_sale_subscription.xml',
        'views/view_sales.xml',
        'views/view_products.xml',
    ],
    'installable': True,
    'auto_install': False,
}
