# -*- coding: utf-8 -*-
#
#  File: __openerp__.py
#  Module: ons_productivity_stats
#
#  Created by cyp@open-net.ch
#
#  Copyright (c) 2013 Open-Net Ltd. All rights reserved.
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2004-2010 Tiny SPRL (<http://tiny.be>).
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
    'name': 'Open-Net Productivity Add-ons: stats tools',
    'version': '1.0.20',
    'category': 'Generic Modules/Open-Net',
    'description': """This module implements a basic object to facilitate some stats

V 1.0   2013-06-14/Cyp
    - sales stats
""",
    'author': 'cyp@open-net.ch',
    'website': 'http://www.open-net.ch',
    'depends': ['account','sale','ons_productivity_messaging'],
    'init_xml': [
		],
    'update_xml': [
        'datas/ir.model.access.csv',
        'wizard/wiz_gen_stats_view.xml',
        'stats_view.xml',
	],
    'demo_xml': [],
    'test': [],
    'installable': False,
    'active': False,
}
