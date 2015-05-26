# -*- coding: utf-8 -*-
#
#  File: res_config.py
#  Module: ons_productivity_accounting
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
from openerp.tools.translate import _

class onsp_absl_config_settings(osv.osv_memory):
    _inherit = 'account.config.settings'

    _columns = {
        'default_onsp_use_bnk_stmt_date': fields.boolean("The line uses the date of the bank statement instead of today's date",
            default_model='account.bank.statement.line'),
    }

    def ons_tools_recomp_acc_hierarchy(self, cr, uid, ids, context=None):
        return self.pool.get('account.account')._parent_store_compute(cr)

onsp_absl_config_settings()
