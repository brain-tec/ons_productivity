# -*- coding: utf-8 -*-
#
#  File: __manifest__.py
#  Module: ons_productivity_dummies
#
#  Created by cyp@open-net.ch
#
#  Copyright (c) 2017-TODAY Open-Net Ltd. All rights reserved.

{
    'name' : 'Open Net productivity: dummies tools',
    'version' : '1.',
    'summary': 'Open Net productivity: dummies tools',
    'author':'Open Net Sàrl',
    'sequence': 30,
    'category': 'Tools',
    'website': 'https://www.open-net.ch',
    'images' : [],
    'depends' : [],
    'data': [
        'views/templates.xml',
        'security/dummies_security.xml'
    ],
    'demo': [],
    'qweb': [],
    'installable': True,
    'auto_install': False,
}
