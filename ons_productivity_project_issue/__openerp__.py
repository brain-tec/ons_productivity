# -*- coding: utf-8 -*-
# © 2016 Coninckx David (Open Net Sarl)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    'name' : 'Open Net Productivity: Project Issue',
    'version' : '1.0.0.0',
    'author' : 'Open Net Sàrl',
    'category' : 'Open Net Productivity',
    'website': 'http://www.open-net.ch',
    'images' : [],
    'depends' : [
        'project_issue_sheet',
        'website_project_issue',
        'website_portal_sale',
    ],
    'data': [
        'views/project_issue_view.xml',
        'views/project_task_view.xml',
        'views/project_project_view.xml',
        'views/website_account_view.xml'
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
