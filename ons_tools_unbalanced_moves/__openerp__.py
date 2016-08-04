 # -*- coding: utf-8 -*-
#
#  File: __openerp__.py
#  Module: ons_tools_unbalanced_moves
#
#  Created by cyp@open-net.ch
#
#  Copyright (c) 2016-TODAY Open-Net Ltd. <http://www.open-net.ch>
##############################################################################
{
    'name' : 'Open-Net tools: helps closing POS session',
    'version' : '1.0',
    'author' : 'Open Net Sarl',
    'category' : 'Open-Net customizations',
    'description' : """
Customizations for ChezDef, by Open Net
---------------------------------------

**Features list :**
    - Removes the "Balanced moves only" requirement, used mainly when closing a POS session with a small difference

**Author :** Open Net Sàrl   Industrie 59  1030 Bussigny  Suisse  http://www.open-net.ch

**Contact :** info@open-net.ch

**History :**

V1.0: 2016-01-17/Cyp
    - Removes the "Balanced moves only" requirement, used mainly when closing a POS session with a small difference
    """,
    'website': 'https://www.open-net.ch',
    'images' : [],
    'depends' : [
        'account'
    ],
    'data': [],
    'qweb' : [
    ],
    'demo': [
    ],
    'test': [
    ],
    'installable': True,
    'auto_install': False,
}
