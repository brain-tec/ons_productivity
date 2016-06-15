 # -*- coding: utf-8 -*-
#
#  File: __openerp__.py
#  Module: ons_productivity_cust_tools
#
#  Created by cyp@open-net.ch
#
#  Copyright (c) 2016-TODAY Open-Net Ltd. <http://www.open-net.ch>
##############################################################################
{
    'name' : 'Open-Net productivity: customer-related tools',
    'version' : '1.0',
    'author' : 'Open Net Sarl',
    'category' : 'Sale',
    'summary': 'Complementary functions for the sale system, related to the customer',
    'website': 'https://www.open-net.ch',
    'depends' : [
        'stock',
        'sale',
        'sale_stock',
    ],
    'data': [
        'views/view_stock.xml'
    ],
    'installable': True,
    'auto_install': False,
}
