# -*- coding: utf-8 -*-
# © 2017 Open Net Sarl
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    'name' : 'Open Net productivity: Layout',
    'version' : '1.0.0.0',
    'author' : 'Open Net Sàrl',
    'category' : 'Extra Tools',
    'website': 'https://www.open-net.ch',
    'depends' : [
        'sale',
        'sale_contract',
        'account'
    ],
    'data': [
        'views/sale_views.xml',
        'views/invoice_views.xml'
    ],
    'installable': True,
    'auto_install': False,
}
