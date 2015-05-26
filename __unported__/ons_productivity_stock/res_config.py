# -*- coding: utf-8 -*-
#
#  File: res_config.py
#  Module: ons_productivity_stock
#
#  Created by cyp@open-net.ch
#
#  Copyright (c) 2013 Open Net Sàrl. All rights reserved.
##############################################################################
#
#    OpenERP, Open Source Business Applications
#    Copyright (C) 2004-2012 OpenERP S.A. (<http://openerp.com>).
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

from openerp.osv import fields, osv
from openerp import pooler
from openerp.tools.translate import _

class repair_config_settings(osv.osv_memory):
    _inherit = 'stock.config.settings'

    _columns = {
        
        # 
        'default_onsp_stk_split_move_by_file': fields.boolean("Split the stock moves by file containing serial numbers (and opt. packaging)",
            default_model='ons.wiz.move_splitter'),
    }

repair_config_settings()
