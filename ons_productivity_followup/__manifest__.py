# -*- coding: utf-8 -*-
# © 2018 Cousinet Eloi (Open Net Sarl)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    'name': 'Open-Net Payment Follow-up',
    'summary': 'Open Net Payment Follow-up management',
    'description': 'Open Net Payment Follow-up management',
    'category': 'Accounting & Finance',
    'author': 'Open Net Sàrl',
    'depends' : ['account', 'mail'],
    'data' : [
        # security
        'security/ir.model.access.csv',
        # data
        'data/followup_data.xml',
        # views
        'views/view_followup.xml',
        'views/view_account_statement.xml',
        # reports
        'report/followup_report_views.xml',
        'report/report_followup.xml',
        'report/account_statement_report_views.xml',
        'report/report_account_statement.xml',
        # wizards
        'wizard/followup_followup.xml',
        'wizard/account_statement.xml',
    ],
    'auto_install': False,
    'installable': True
}
