# -*- coding: utf-8 -*-
#
#  File: models/__init__.py
#  Module: ons_productivity_bac
#
#  Created by cyp@open-net.ch
#
#  Copyright (c) 2015-TODAY Open Net Sàrl. <http://www.open-net.ch>
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

from openerp.osv import osv, fields
import openerp.addons.decimal_precision as dp

class stock_picking(osv.osv):
    _inherit = "stock.picking"

    _columns = {
        'cost_imputed': fields.boolean('Cost Imputed', help="This box indicate if you already have imputed the cost \
                of that picking on the given analytical account", readonly="True"),
     }
    _defaults = {
        'cost_imputed': lambda *a: False,
    }

    def copy(self, cr, uid, id, default=None, context=None):
        if default is None:
            default = {}
        default = default.copy()
        default.update({'cost_imputed':False})

        return super(stock_picking, self).copy(cr, uid, id, default, context=context)

class stock_move(osv.osv):
    _inherit = 'stock.move'
    
    _columns = {
        'ons_pu': fields.float('Unit Price', digits_compute=dp.get_precision('Account')),
    }
    
    defaults = {
        'ons_pu': lambda *a: 0.0,
    }

