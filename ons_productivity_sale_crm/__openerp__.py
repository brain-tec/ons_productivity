# -*- coding: utf-8 -*-
#
# File: __openerp__.py
# Module: ons_productivity_sale_crm
#
# Created by cyp@open-net.ch
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    'name' : 'Open Net Productivity: Sale CRM',
    'version' : '1.0',
    'author' : 'Open Net Sàrl',
    'category' : 'CRM',
    'website': 'http://www.open-net.ch',
    'images' : [],
    'depends' : [
        'account',
        'sale',
        'sale_crm',
        'sales_team'
    ],
    'data': [
        'views/view_sale_crm.xml',
        'views/view_users.xml',
        'views/view_sale_crm_dashboard.xml',
        'views/view_sale_team.xml',
        'views/view_invoice.xml'
    ],
    'qweb': [
        "static/src/xml/onsp_sales_crm_dashboard.xml",
    ],
    'installable': False,
    'auto_install': False,
}
