# -*- coding: utf-8 -*-
# Copyright 2017 Open Net Sàrl
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
{
    'name' : 'Open-Net productivity: Point of Sale Categories',
    'version' : '1.0',
    'author' : 'Open Net Sàrl',
    'category' : 'Point of Sale',
    'summary': 'Complementary functions for the Points of Sale',
    'website': 'https://www.open-net.ch',
    'depends' : [
        'point_of_sale',
    ],
    'data': [
        # server actions
        'data/server_actions/product_template.xml',
        'data/server_actions/product_category.xml',
    ],
    'installable': True,
    'auto_install': False,
}