# -*- coding: utf-8 -*-
# © 2016 Coninckx David (Open Net Sarl)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    'name' : 'Open Net Productivity: Payment',
    'version' : '1.0.0.0',
    'author' : 'Open Net Sàrl',
    'category' : 'Accounting',
    'website': 'http://www.open-net.ch',
    'images' : [],
    'depends' : [
        'account_banking_pain_base',
        'account_payment_order',
    ],
    'data': [
        'views/bank_statement_view.xml'
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