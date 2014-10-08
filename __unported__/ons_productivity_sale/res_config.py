# -*- coding: utf-8 -*-
#
#  File: res_config.py
#  Module: ons_productivity_sale
#
#  Created by cyp@open-net.ch
#
#  Copyright (c) 2013 Open-Net Ltd. All rights reserved.
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

class sale_config_settings(osv.osv_memory):
    _inherit = 'sale.config.settings'

    _columns = {
        'default_onsp_sale_pricelist_vs_supplier': fields.boolean("Do not link a sale pricelist to the supplier info", default_model='product.pricelist'),
        'default_onsp_sale_force_partner_relationship': fields.boolean("Force partner relationship for invoice and delivery address", default_model='sale.order'),
        'default_onsp_sale_partner_companies_only': fields.boolean("Partner are only companies", default_model='sale.order'),
    }

sale_config_settings()
