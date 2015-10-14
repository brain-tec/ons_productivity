# -*- coding: utf-8 -*-
#
#  File: models/__init__.py
#  Module: ons_productivity_auto_split
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

from openerp import models, api

import logging
_logger = logging.getLogger(__name__)


class StockPicking(models.Model):
    _inherit = 'stock.picking'

    @api.multi
    def action_split_moves(self):
        cr, uid, context = self.env.args
        StockMove = self.pool.get('stock.move')
        for pick in self:
            for move in pick.move_lines:
                if move.state in ('draft', 'done', 'cancel'):
                    continue
                pack = move.product_packaging or \
                    (move.product_id.packaging_ids and move.product_id.packaging_ids[0]) or \
                    False
                if not pack:
                    _logger.info("No defined packaging for '%'" % move.product_id.name)
                    continue

                new_qty = pack.qty
                while(True):
                    if move.product_uom_qty <= new_qty:
                        break
                    StockMove.split(cr, uid, move, new_qty, context=context)

        return True
