# -*- coding: utf-8 -*-
# © 2016 Open Net Sarl
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    'name' : 'Open Net Productivity: Employee Barcode',
    'version' : '1.0.0.0',
    'author' : 'Open Net Sàrl',
    'category' : 'Human Ressources',
    'website': 'http://www.open-net.ch',
    'images' : [],
    'depends' : [
        'barcodes',
        'web',
        'hr'
    ],
    'data': [
        'views/backend_assets.xml',
        'views/employee_view.xml',
        'views/res_users_view.xml'
    ],
    'qweb' : [
        'static/src/xml/employee.xml',
    ],
    'installable': False,
    'auto_install': False,
}
