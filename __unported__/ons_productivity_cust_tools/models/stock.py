# -*- encoding: utf-8 -*-
#
#  File: models/stock.py
#  Module: ons_productivity_cust_tools
#
#  Created by cyp@open-net.ch
#
#  Copyright (c) 2016-TODAY Open-Net Ltd. All rights reserved.

from openerp.osv import fields
from openerp import models


class stock_picking(models.Model):
    _inherit = 'stock.picking'

    _columns = {
        'client_order_ref': fields.related('sale_id', 'client_order_ref', type='char', string='Customer Reference')
    }
