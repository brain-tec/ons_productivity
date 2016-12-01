# -*- coding: utf-8 -*-
# © 2016 Coninckx David (Open Net Sarl)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    'name' : 'Open Net Productivity: Impot à la source',
    'version' : '1.0.0.0',
    'author' : 'Open Net Sàrl',
    'category' : 'Project',
    'website': 'http://www.open-net.ch',
    'images' : [],
    'depends' : [
        'l10n_ch_hr_payroll',
    ],
    'data': [
        'views/hr_employee_view.xml',
        'data/hr_payslip_rule.xml',
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
