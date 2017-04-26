# -*- coding: utf-8 -*-
# © 2016 Open Net Sarl
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    'name': 'Open Net Productivity: Payroll Cancel',
    'category': 'Sales',
    'author': "Open Net Sàrl",
    'depends': [
        'hr_payroll'
    ],
    'version': '1.0.0.0',
    'auto_install': False,
    'website': 'http://open-net.ch',
    'license': 'AGPL-3',
    'images': [],
    'data': [
        'data/hr_payroll_workflow.xml',
        'views/view_hr_payslip.xml'
    ],
    'installable': False
}
