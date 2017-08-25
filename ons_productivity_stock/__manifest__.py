# -*- coding: utf-8 -*-
# Copyright 2017 Open Net Sàrl
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
{
    'name' : 'Open Net productivity: Stock',
    'version' : '1.1.0',
    'author' : 'Open Net Sàrl',
    'category' : 'Extra Tools',
    'website': 'https://www.open-net.ch',
    'depends' : [
        'delivery',
        'stock'
    ],
    'data': [
        'views/product_views.xml',
        'views/report_deliveryslip.xml',
        'views/stock_view.xml'
    ],
    'installable': True,
    'auto_install': False,
}
