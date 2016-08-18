# -*- coding: utf-8 -*-
# © 2016 Coninckx David (Open Net Sarl)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    'name' : 'Open-Net Productivity: Project Issue',
    'version' : '0.0.04',
    'author' : 'Open Net Sarl',
    'category' : 'Issue Management',
    'description' : """
Open Net Productivity : Project Issue
----------------------------------------------

The 'productivity' modules is a complete family of modules offering improvement for OpenERP.
These modules are maintained by Open Net, Swiss Partner of OpenERP.
These modules are included in all our hosting solutions.

**Features list :**
    - When create a new issu, add its ID on its name
    - new field for issues: short_name: the name without the [id]

**Author :** Open Net Sarl   Industrie 59  1030 Bussigny  Suisse  http://www.open-net.ch

**Contact :** info@open-net.ch

**History :**

V0.3: 2014-10-14/Sge
    - Add the feature #1

V0.4: 2014-10-14/Cyp
    - Add the feature #2

""",
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
