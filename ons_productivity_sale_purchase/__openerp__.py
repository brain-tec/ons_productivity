# -*- coding: utf-8 -*-
#
#  File: __openerp__.py
#  Module: ons_productivity_sale_purchase
#
#  Created by cyp@open-net.ch
#
#  Copyright (c) 2016-TODAY Open-Net Ltd. <http://www.open-net.ch>

{
    'name' : 'Open Net Productivity: Sale Purchase',
    'version' : '1.0',
    'author' : 'Open Net Sàrl',
    'category' : 'Project',
    'website': 'http://www.open-net.ch',
    'images' : [],
    'depends' : [
        'sale',
        'purchase'
    ],
    'data': [
        'views/sale_order_view.xml'
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
