# -*- coding: utf-8 -*-
#
#  File: __openerp__.py
#  Module: ons_productivity_soap
#
#  Created by cyp@open-net.ch
#
#  Copyright (c) 2013-TODAY Open-Net Ltd. All rights reserved.

{
    'name': 'Open-Net Productivity Add-ons: SOAP connector',
    'version': '2.0',
    'category': 'Generic Modules/Open-Net',
    'description': """This module implements a basic SOAP client connection system.
It is based on an external library: SUDS >>> https://fedorahosted.org/suds/

**Author :** Open Net Sàrl   Industrie 59  1030 Bussigny  Suisse  http://www.open-net.ch

**Contact :** info@open-net.ch

**History :**

V 1.0: 2013-01-15
    - scratch writing

V 1.01: 2013-08-12
    - products fields mapping system

V 1.02.02: 2014-01-27
    - log entries for the external server

V 1.02.03: 2014-01-28
    - new field in the log entries: doing

V 1.02.07: 2014-04-03
    - automatic pub. field present in servers list, too
    - handles Magento atribute creation in cases in which the label contains a punctuation sign

V 2.0: 2016-10-04
    - ported to Odoo V9
""",
    'website': 'http://www.open-net.ch',
    'images' : [],
    'depends': ['product'],
    'data': [
        'security/security.xml',
        'security/ir.model.access.csv',
        'views/soap_servers_view.xml',
	],
    'qweb' : [
    ],
    'demo': [
    ],
    'test': [
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
}
