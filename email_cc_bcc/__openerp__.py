# -*- coding: utf-8 -*-
#
#  File: __openerp__.py
#  Module: email_cc_bcc
#
#  Created by cyp@open-net.ch
#
#  Copyright (c) 2015-TODAY Open-Net Ltd. <http://www.open-net.ch>
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2004-TODAY OpenERP S.A. <http://www.openerp.com>
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################
{
    'name' : 'Email CC',
    'version' : '1.0.0',
    'author' : 'Open Net Sarl',
    'category' : 'Social Networking',
    'description' : """
Email templating add-ons: adds a CC field
-----------------------------------------


**Features list :**
 - Adds a CC field to email templates

**Author :** Open Net Sàrl   Industrie 59  1030 Bussigny  Suisse  http://www.open-net.ch

**Contact :** info@open-net.ch

**History :**

V1.0.0: 2015-04-01/Cyp
    - Scratch writing
    """,
    'website': 'https://www.open-net.ch',
    'images' : [],
    'depends' : ['email_template'],
    'data': [
        'views/view_mail_message.xml',
        'views/view_mail_compose_message.xml',
    ],
    'qweb' : [
    ],
    'demo': [
    ],
    'test': [
    ],
    'installable': True,
    'auto_install': False,
}
