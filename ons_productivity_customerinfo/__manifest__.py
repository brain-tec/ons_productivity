# -*- coding: utf-8 -*-
# © 2018 Open Net Sarl
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    'name': 'Open-Net Customerinfo',
    'summary': 'Open-Net Customerinfo',
    'description': 'Add a model customerinfo to product similar to supplierinfo',
    'category': 'Open Net customizations',
    'author': 'Open Net Sàrl',
    'version': '11.0.1.0.2',
    'auto_install': False,
    'website': 'http://open-net.ch',
    'license': 'AGPL-3',
    'depends': [
        'sale',
        'product',
    ],
    'data': [
        'views/product_supplierinfo_view.xml',
        'security/ir.model.access.csv'
    ],
    'installable': True
}
