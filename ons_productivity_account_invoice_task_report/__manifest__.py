# -*- coding: utf-8 -*-
# © 2018 Open Net Sarl
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    'name' : 'Open Net Productivity: Account invoice task report',
    'version' : '1.0',
    'author' : 'Open Net Sàrl',
    'category' : 'Accounting',
    'website': 'http://www.open-net.ch',
    'images' : [],
    'depends' : [
        'account',
        'sale'
    ],
    'data': [
        'report/report_account_invoice_task.xml',
        'views/view_account_invoice.xml'
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
