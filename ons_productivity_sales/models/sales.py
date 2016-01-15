# -*- coding: utf-8 -*-
#
#  File: models/sales.py
#  Module: ons_prod_sales
#
#  Created by cyp@open-net.ch
#
#  Copyright (c) 2015-TODAY Open-Net Ltd. All rights reserved.
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
from openerp.exceptions import  Warning
from openerp import models, fields, api, _
from openerp.tools import float_compare

import logging
_logger = logging.getLogger(__name__)


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    @api.multi
    def action_confirm(self):
        #Check if the current user is the teamleader of the sale
        if (self.team_id.user_id.id != self.env.uid):
            msg = _("You are not allowed to confirm a sale\nContact the team leader : ")+self.team_id.user_id.name
            _logger.info(msg)
            raise Warning(msg)
        else:
            return super(SaleOrder, self).action_confirm()
