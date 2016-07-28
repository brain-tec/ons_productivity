# -*- coding: utf-8 -*-
#
#  File: models/sale.py
#  Module: ons_productivity_sale_assets
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

from openerp import models, fields
from datetime import datetime
from dateutil.relativedelta import relativedelta
import time

class SaleOrder(models.Model):
    _inherit = 'sale.order'

    def action_wait(self, cr, uid, ids, context=None):
        ret = super(SaleOrder, self).action_wait(cr, uid, ids, context=context)

        SaleAsset = self.pool.get('sale.asset')
        # Silent check, as we are in the middle of a workflow and it's not mandatory
        if SaleAsset.check_access_rights(cr, uid, 'create', raise_exception=False):
            for so in self.browse(cr, uid, ids, context=context):
                for line in so.order_line:
                    if not line.product_id.generate_asset:
                        continue
                    
                    date_ref = datetime.now()
                    date_start = date_ref + relativedelta(days=7)
                    date_end = date_start + relativedelta(months=int(line.product_id.warranty))
                    values = {
                        'date_start': date_start.strftime('%Y-%m-%d'),
                        'date_end': date_end.strftime('%Y-%m-%d'),
                        'note': line.product_id.description_sale or line.product_id.name, 
                            'partner_id': so.partner_id.id, 
                        'product_id': line.product_id.id, 
                        'product_info': line.product_id.name,
                        'sale_id': so.id,
                        'sale_line_id': line.id,
                        'name': line.id
                    }
                    SaleAsset.create(cr, uid, values, context=context)
        
        return ret
