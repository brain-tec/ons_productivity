# -*- coding: utf-8 -*-
#
#  File: wizard/stock_transfer_details.py
#  Module: ons_productivity_auto_split
#
#  Created by cyp@open-net.ch
#
#  Copyright (c) 2015-TODAY Open Net Sàrl. <http://www.open-net.ch>
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2004-TODAY OpenERP S.A. <http://www.odoo.com>
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

from openerp import models, api


class stock_transfer_details_items(models.TransientModel):
    _inherit = 'stock.transfer_details_items'

    @api.multi
    def split_quantities(self):
        for det in self:
            qty = (det.product_id.packaging_ids and det.product_id.packaging_ids[0].qty) or 0
            if not qty:
                qty = 1
            while(det.quantity > qty):
                det.quantity = (det.quantity-qty)
                new_id = det.copy(context=self.env.context)
                new_id.quantity = qty
                new_id.packop_id = False
        if self and self[0]:
            return self[0].transfer_id.wizard_view()
